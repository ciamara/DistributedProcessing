import socket
import threading
from datetime import datetime

HOST = '127.0.0.1'
PORT = 12345

clients = {}
clients_messages = {}


def handle_client(conn, addr):
    try:
        # first message -> take username
        username = conn.recv(1024).decode().strip()
        # add connection to clients
        clients[username] = conn
        # send queued messages
        if username in clients_messages.keys():
            for message in clients_messages.get(username):
                conn.send(message.encode())
        clients_messages[username] = []

        # log connection
        print(f"[+] {username} joined the chat from {addr}")

        # receive messages
        while True:
            message = conn.recv(1024)
            if not message:
                break

            split_message = message.decode().split(": ", 1)
            if len(split_message) == 1:
                formatted_message = f"[{timestamp()}] {username}: {split_message[0]}\n"
                # broadcast to other clients
                broadcast(formatted_message.encode(), conn)
            else:
                recipient = split_message[0]
                if recipient not in clients_messages.keys():
                    conn.send("User does not exist".encode())
                    continue

                formatted_message = f"[{timestamp()}] {username}: {split_message[1]}\n"
                recipient_conn = clients.get(recipient, None)
                if send_to_user(formatted_message, recipient_conn) is False:
                    # add message to the queue
                    clients_messages.get(recipient).append(formatted_message)

    except Exception as e:
        print(str(e))
    finally:
        # disconnecting
        print(f"[-] {username} left the chat")
        clients.pop(username)
        conn.close()


# send to the specified client
def send_to_user(message, recipient_conn):
    if recipient_conn is None:
        return False

    recipient_conn.send(message.encode())
    return True


# send message to clients
def broadcast(message, sender_conn):
    for username, client in clients.items():
        if client != sender_conn:
            try:
                client.send(message)
            except:
                pass

# timestamping messages


def timestamp():
    return datetime.now().strftime("%H:%M:%S")


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[*] Server started on {HOST}:{PORT}")

    # accept connections
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()


if __name__ == "__main__":
    main()
