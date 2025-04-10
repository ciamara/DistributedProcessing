from libdecoder import Decoder
from encoder import Encoder
import os
import socket

GUESSED = 1
HOST = "127.0.0.1"
PORT = 2137

pid = os.fork()
if pid != 0:
    encoder = Encoder()
    print()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            encoder.generate_code()
            encoder.print_code()

            while not encoder.game_over:
                encoder.attempts += 1
                decoder_guessed = conn.recv(1024)

                if not decoder_guessed:
                    break

                verified_guess = encoder.verify_guess(decoder_guessed)
                conn.sendall(bytearray(verified_guess))
                # decoder.attempts += 1

                # print()
                # print("           ROUND " + str(encoder.attempts))

                # decoder.guess()
                # decoder.feedback = encoder.verify_guess(decoder.guessed)
                encoder.check_if_game_over()

    if (encoder.game_state == GUESSED):
        print("Decoder guessed the code!")
    else:
        print("Decoder did not guess the code...")
else:
    decoder = Decoder()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        while True:
            decoder.attempts += 1
            decoder.guess()
            decoder.print_guessed()
            s.sendall(bytearray(decoder.guessed))
            # s.sendall(bytearray(input(), "utf-8"))
            verified_guess = s.recv(1024)
            decoder.feedback = verified_guess
            # print(f"Received {data!r}")
