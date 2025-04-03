from decoder import Decoder
from encoder import Encoder

GUESSED = 1

encoder = Encoder()
decoder = Decoder()

print()

encoder.generate_code()

encoder.print_code()


while not encoder.game_over:

    encoder.attempts += 1
    decoder.attempts += 1

    print()
    print("           ROUND " + str(encoder.attempts))

    decoder.guess()
    decoder.print_guessed()
    decoder.feedback = encoder.verify_guess(decoder.guessed)
    encoder.check_if_game_over()
   

if(encoder.game_state ==  GUESSED):
    print("Decoder guessed the code!")
else:
    print("Decoder did not guess the code...")