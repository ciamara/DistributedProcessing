#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/wait.h>
#include <signal.h>

#define MAX_INPUT 512

void print_help(void) {

    printf("Available commands:\n");
    printf("  Help - Show this help message\n");
    printf("  Pwd - Show the current working directory\n");
    printf("  Run <program> <params> - Run a program in the foreground\n");
    printf("  Bg <program> <params> - Run a program in the background\n");
}

void print_pwd(void) {

    char cwd[MAX_INPUT];

    if (getcwd(cwd, sizeof(cwd)) != NULL) {
        printf("Current directory: %s\n", cwd);
    } else {
        perror("getcwd");
    }
}

void run_command(char *command, char *args[], int background) {

    //new process
    pid_t pid = fork();

    if (pid < 0) {

        perror("fork failed");

    } else if (pid == 0) { //child process

        execvp(command, args); //exec command
        perror("execvp failed");
        exit(1);

    } else {
        if (!background) {

            int status;
            waitpid(pid, &status, 0); //waits for foreground process to finish and exits
            printf("Foreground process exited with code %d\n", WEXITSTATUS(status));

        } else {
            printf("Background process started with PID %d\n", pid); //returns to the prompt
        }
    }
}

//signal handler, triggers when a child process terminates
void handle_sigchld(int sig) {

    (void)sig; // prevents a compiler warning about the unused parameter sig

    //cleans all terminated child processes
    // -1 -> check for child processes
    //WNOHANG -> return if no child exited, preventing shell getting stuck
    while (waitpid(-1, NULL, WNOHANG) > 0);
}

int main(void) {

    //struct to define how program handles SIGCHLD
    struct sigaction sa;

    //call handle_sigchld when SIGCHLD received
    sa.sa_handler = handle_sigchld;

    //SA_RESTART -> interrupted system calls auto resume instead of failing (ex. fgets)
    //SA_NOCLDSTOP -> prevents SIGCHLD from being sent when child processes are stopped, only when they terminate
    sa.sa_flags = SA_RESTART | SA_NOCLDSTOP;

    //handle_sigchld() -> handler for SIGCHLD
    sigaction(SIGCHLD, &sa, NULL);

    char input[MAX_INPUT];

    while (1) {

        printf("$ ");

        if (!fgets(input, MAX_INPUT, stdin)) {
            break;
        }
        
        input[strcspn(input, "\n")] = 0; //remove newline
        
        if (strcmp(input, "Help") == 0) {

            print_help();

        } else if (strcmp(input, "Pwd") == 0) {

            print_pwd();

        } else if (strncmp(input, "Run ", 4) == 0 || strncmp(input, "Bg ", 3) == 0) {

            int background = (input[0] == 'B');
            
            char *tokens[64];
            int i = 0;
            char *token = strtok(input + (background ? 3 : 4), " ");

            while (token) {

                tokens[i++] = token;
                token = strtok(NULL, " ");
            }

            tokens[i] = NULL;
            
            if (tokens[0]) {

                run_command(tokens[0], tokens, background);

            } else {

                printf("No program input\n");

            }
        } else {

            printf("Unknown command\n");
        }
    }
    return 0;
}