import random

ATTEMPTS = 5

class Encoder:

    def __init__(self, code = [], game_state = 0, attempts = 0, game_over = False):
        self.code = code
        self.game_state = game_state
        self.attempts = attempts
        self.game_over = game_over


    def generate_code(self):
        self.code = random.choices(range(1, 7), k=4)


    def check_if_game_over(self):
        if self.attempts >=ATTEMPTS:
            self.game_over = True
        elif self.game_state == 1:
            self.game_over = True
        else:
            self.game_over = False
        
    def print_code(self):

        # red=1, green=2, yellow=3, blue=4, purple=5, cyan=6, white=7
        #colors = [31, 32, 33, 34, 35, 36, 37]
        colors = [31, 32, 33, 34, 35, 36]

        print("         The code is: ")
        for num in self.code:
            print("\033[1;" + str(colors[num - 1]) + "m", end='')  # apply color
            print("     \u2B24", end=' ')  # print ball
        print("\033[0m")  # reset color
        print()

    def verify_guess(self, guessed):

        feedback = []

        # check for exact matches
        for i in range(len(self.code)):
            if self.code[i] == guessed[i]:
                feedback.append(2)  # correct color and pos
               
            else:
                feedback.append(None)  # none -> not matched spots

        # check for correct numbers in the wrong position
        for i in range(len(self.code)):
            if feedback[i] is None:  # check positions not matched yet
                for j in range(len(self.code)):
                    if self.code[j] == guessed[i]:
                        feedback[i] = 1  # correct color wrong pos
                        break

        # none -> 0 (not matched colors)
        feedback = [0 if x is None else x for x in feedback]

        if feedback == [2, 2, 2, 2]:
            self.game_state = 1
    
        print("         Feedback: ")
        print("       " + str(feedback))
        print()

        return feedback
    
            