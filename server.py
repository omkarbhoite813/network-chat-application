import socket
import threading
import json

HOST = "0.0.0.0"
PORT = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = {}
addresses = {}

print("Server started...")

with open("users.json") as f:
    users = json.load(f)


def broadcast(message):
    for client in clients.values():
        try:
            client.send(message.encode())
        except:
            pass


def send_user_list():
    user_list = ",".join(clients.keys())
    msg = "/users " + user_list

    for client in clients.values():
        client.send(msg.encode())


def handle_client(client, username):

    while True:

        try:
            message = client.recv(1024).decode()

            if message.startswith("@"):

                target = message.split(" ")[0][1:]
                msg = message[len(target) + 2:]

                if target in clients:
                    clients[target].send(
                        f"[PRIVATE] {username}: {msg}".encode()
                    )

            else:

                full_msg = f"{username}: {message}"

                print(full_msg)

                with open("chat_history.txt", "a") as f:
                    f.write(full_msg + "\n")

                broadcast(full_msg)

        except:

            print(username, "disconnected")

            clients.pop(username)

            send_user_list()

            broadcast(username + " left chat")

            break


def authenticate(client):

    client.send("USERNAME".encode())
    username = client.recv(1024).decode()

    client.send("PASSWORD".encode())
    password = client.recv(1024).decode()

    if username in users and users[username] == password:
        client.send("SUCCESS".encode())
        return username
    else:
        client.send("FAIL".encode())
        return None


def receive():

    while True:

        client, address = server.accept()

        print("Connected:", address)

        username = authenticate(client)

        if username:

            clients[username] = client

            send_user_list()

            broadcast(username + " joined chat")

            thread = threading.Thread(target=handle_client, args=(client, username))
            thread.start()

        else:

            client.close()


receive()