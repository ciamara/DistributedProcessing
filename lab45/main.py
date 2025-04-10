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
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()

        encoder = Encoder()
        print()
        encoder.generate_code()
        encoder.print_code()
        with conn:
            conn.sendall(bytearray("start", "utf-8"))
            while not encoder.game_over:
                encoder.attempts += 1
                print()
                print("           ROUND " + str(encoder.attempts))

                decoder_guessed = conn.recv(1024)

                if not decoder_guessed:
                    break

                verified_guess = encoder.verify_guess(decoder_guessed)
                encoder.check_if_game_over()
                if encoder.game_over:
                    conn.sendall(bytearray("finish", "utf-8"))
                else:
                    conn.sendall(bytearray(verified_guess))

    if (encoder.game_state == GUESSED):
        print("Decoder guessed the code!")
    else:
        print("Decoder did not guess the code...")
else:
    decoder = Decoder()
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
