#include <stdio.h>
#include <pthread.h>
#include <stdlib.h>


struct node{
    int number;
    struct node *next;
};

typedef struct node Node;

typedef struct {
    Node *top;
} Stack;

void init(Stack *s) {
    s->top = NULL;
}

int count(Stack *s) {

    int count = 0;
    Node *current = s->top;

    while (current) {
        count++;
        current = current->next;
    }

    printf("Stack contains %d items\n", count);
}

void push(Stack *s, int value) {

    Node *newNode = (Node *)malloc(sizeof(Node));

    if (!newNode) {
        printf("Memory allocation failed\n");
        return;
    }

    newNode->number = value;
    newNode->next = s->top;
    s->top = newNode;
}

int pop(Stack *s) {

    if (s->top == NULL) {
        printf("Stack underflow\n");
        return -1;
    }

    Node *temp = s->top;
    int value = temp->number;
    s->top = s->top->next;
    free(temp);
    return value;
}

int isEmpty(Stack *s) {
    return s->top == NULL;
}

void printStack(Stack *s) {

    Node *current = s->top;

    while (current) {

        printf("%d -> ", current->number);
        current = current->next;
    }
    printf("NULL\n");
}

#define NUMS 1000

void *even(void *arg) {

    Stack *s = (Stack *)arg;

    for(int i=0; i<NUMS; i++){
        push(s, i*2);
    }
    
    return NULL;
}

void *odd(void *arg) {

    Stack *s = (Stack *)arg;

    for(int i=0; i<NUMS; i++){
        push(s, i*2+1);
    }
    
    return NULL;
}

int main() {

    pthread_t even_thread, odd_thread;

    Stack stack;
    init(&stack);

    pthread_create(&even_thread, NULL, even, (void *)&stack);
    pthread_create(&odd_thread, NULL, odd, (void *)&stack);

    pthread_join(even_thread, NULL);
    pthread_join(odd_thread, NULL);
    

    printStack(&stack);
    count(&stack);
    
    return 0;
}