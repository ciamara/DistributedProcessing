import random
import socket


def run_decoder(HOST, PORT, decoder):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))

        if s.recv(1024):
            while True:
                decoder.attempts += 1
                decoder.guess()
                decoder.print_guessed()
                s.sendall(bytearray(decoder.guessed))
                verified_guess = s.recv(1024)
                if not verified_guess:
                    break
                if verified_guess == bytearray("finish", "utf-8"):
                    break

                decoder.feedback = verified_guess


class Decoder:

    def __init__(self, guessed=[], game_state=0, attempts=0, feedback=[], possible_colors=[]):
        self.guessed = guessed
        self.game_state = game_state
        self.attempts = attempts
        self.feedback = feedback
        self.possible_colors = [1, 2, 3, 4, 5, 6]

    def print_guessed(self):
        # red=1, green=2, yellow=3, blue=4, purple=5, cyan=6, white=7
        # colors = [31, 32, 33, 34, 35, 36, 37]
        colors = [31, 32, 33, 34, 35, 36]

        print("       Decoder guessed: ")
        for num in self.guessed:
            print("\033[1;" + str(colors[num - 1]) +
                  "m", end='')  # apply color
            print("     \u2B24", end=' ')  # print ball
        print("\033[0m")  # reset color
        print()

    def guess(self):

        if self.attempts == 1:
            # initial random guess
            self.guessed = random.choices(self.possible_colors, k=4)
        else:
            # guess refinement based on feedback
            new_guess = self.guessed.copy()

            # eliminate colors that are entirely wrong
            for i in range(len(self.feedback)):
                if self.feedback[i] == 0:
                    # Check if the guessed color is still valid in the possible colors
                    if self.guessed[i] in self.possible_colors:
                        self.possible_colors.remove(self.guessed[i])

            for i in range(len(self.feedback)):
                if self.feedback[i] == 2:  # keep exact match
                    continue
                elif self.feedback[i] == 1:  # correct color wrong pos
                    # try new pos for correct color
                    # //if self.guessed[i] not in self.possible_colors:
                    # self.possible_colors.append(self.guessed[i])
                    new_guess[i] = random.choice(
                        [x for x in self.possible_colors if x != self.guessed[i]])

                elif self.feedback[i] == 0:  # eliminate color from guesses
                    if self.guessed[i] in self.possible_colors:
                        self.possible_colors.remove(self.guessed[i])
                    new_guess[i] = random.choice(
                        [x for x in self.possible_colors if x != self.guessed[i]])

            print("Possible colors: ")
            print(self.possible_colors)
            self.guessed = new_guess
            return self.guessed
