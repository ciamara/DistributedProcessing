import socket
import threading

HOST = '127.0.0.1'
PORT = 12345

# get messages from server


def receive_messages(sock):
    while True:
        try:
            message = sock.recv(1024).decode()
            if message:
                print("\n" + message)
        except:
            print("[!] Connection closed.")
            break


def main():
    # input username

    username = input("Choose your username: ")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    # log connection on client side
    print("[*] Connected to the server.")

    # send username (log in)
    client.send(username.encode())

    threading.Thread(target=receive_messages,
                     args=(client,), daemon=True).start()

    # take messages (or exit)
    while True:
        msg = input()
        if msg.lower() == 'exit':
            break
        client.send(msg.encode())

    client.close()


if __name__ == "__main__":
    main()
