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
        # initial random guess
        self.guessed = random.choices(self.possible_colors, k=4)
        print("Possible colors: ")
        print(self.possible_colors)
        return self.guessed
