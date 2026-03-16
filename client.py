import socket
import threading
import tkinter as tk

HOST = "127.0.0.1"   # Change to server IP when using WiFi
PORT = 5555

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))


# ---------------- RECEIVE MESSAGES ---------------- #

def receive():
    while True:
        try:
            message = client.recv(1024).decode()

            if message.startswith("/users"):

                users = message.split(" ")[1].split(",")

                users_list.delete(0, tk.END)

                unique_users = list(set(users))

                for user in unique_users:
                    users_list.insert(tk.END, user)

            else:
                chat_area.config(state=tk.NORMAL)
                chat_area.insert(tk.END, message + "\n")
                chat_area.config(state=tk.DISABLED)
                chat_area.see(tk.END)

        except:
            break


# ---------------- SEND MESSAGE ---------------- #

def send_message():

    message = message_entry.get()

    if message != "":
        client.send(message.encode())

    message_entry.delete(0, tk.END)


# ---------------- LOGIN ---------------- #

def login():

    username = username_entry.get()
    password = password_entry.get()

    client.recv(1024)
    client.send(username.encode())

    client.recv(1024)
    client.send(password.encode())

    response = client.recv(1024).decode()

    if response == "SUCCESS":

        login_frame.pack_forget()

        chat_frame.pack(fill=tk.BOTH, expand=True)

        threading.Thread(target=receive).start()

    else:

        status_label.config(text="Login Failed")


# ---------------- GUI ---------------- #

window = tk.Tk()
window.title("Network Chat Application")
window.geometry("850x550")
window.configure(bg="#2c2f33")


# LOGIN FRAME
login_frame = tk.Frame(window, bg="#2c2f33")
login_frame.pack(pady=120)

tk.Label(login_frame, text="Login", font=("Arial",20), bg="#2c2f33", fg="white").pack(pady=10)

username_entry = tk.Entry(login_frame, width=25)
username_entry.pack(pady=5)

password_entry = tk.Entry(login_frame, width=25, show="*")
password_entry.pack(pady=5)

tk.Button(login_frame, text="Login", command=login, bg="#7289da", fg="white").pack(pady=10)

status_label = tk.Label(login_frame, bg="#2c2f33", fg="red")
status_label.pack()


# CHAT FRAME
chat_frame = tk.Frame(window, bg="#2c2f33")


# LEFT PANEL (ONLINE USERS)
left_frame = tk.Frame(chat_frame, bg="#23272a")
left_frame.pack(side=tk.LEFT, fill=tk.Y)

tk.Label(left_frame, text="Online Users", bg="#23272a", fg="white", font=("Arial",12)).pack(pady=10)

users_list = tk.Listbox(left_frame, width=20, bg="#2f3136", fg="white")
users_list.pack(fill=tk.Y, padx=5, pady=5)


# RIGHT PANEL (CHAT)
right_frame = tk.Frame(chat_frame, bg="#2c2f33")
right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)


chat_area = tk.Text(right_frame, bg="#36393f", fg="white", state=tk.DISABLED)
chat_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)


# MESSAGE AREA
bottom_frame = tk.Frame(right_frame, bg="#2c2f33")
bottom_frame.pack(fill=tk.X)

message_entry = tk.Entry(bottom_frame)
message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=10, pady=10)

message_entry.bind("<Return>", lambda event: send_message())


send_btn = tk.Button(bottom_frame, text="Send", command=send_message, bg="#7289da", fg="white")
send_btn.pack(side=tk.RIGHT, padx=10)


window.mainloop()