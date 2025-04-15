import socket
import threading
from datetime import datetime

HOST = '127.0.0.1'
PORT = 12345

clients = []
usernames = {}

def handle_client(conn, addr):
    try:
        # first message -> take username
        username = conn.recv(1024).decode().strip()
        usernames[conn] = username
        # add connection to clients
        clients.append(conn)
        
        # log connection
        print(f"[+] {username} joined the chat from {addr}")
        
        # receive messages
        while True:
            message = conn.recv(1024)
            if not message:
                break
            formatted = f"[{timestamp()}] {username}: {message.decode()}"
            # broadcast to other clients
            broadcast(formatted.encode(), conn)
    except:
        pass
    finally:
        # disconnecting
        print(f"[-] {usernames.get(conn, 'Unknown')} left the chat")
        clients.remove(conn)
        usernames.pop(conn, None)
        conn.close()

# send message to clients
def broadcast(message, sender_conn):
    for client in clients:
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
