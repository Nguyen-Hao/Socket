import socket

IP = "127.0.0.1"
PORT = 64320
FORMAT = "utf8"


# ------------------------ function -------------------------------
def sendList(client, list):
    for items in list:
        client.sendall(items.encode(FORMAT))
        client.recv(1024)
    msg = "end"
    client.send(msg.encode(FORMAT))


def login(client):
    account = []
    user = input("user:")
    passw = input("password:")
    account.append(user)
    account.append(passw)
    sendList(client, account)
    status = client.recv(1024).decode(FORMAT)
    print(status)


# --------------------------- main ---------------------------------
def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((IP, PORT))
        print("Client address", client.getsockname())

        ClientMsg = None
        ServerMsg = None
        while ClientMsg != "x" and ClientMsg != " ":
            ClientMsg = input("Client: ")
            client.sendall(ClientMsg.encode(FORMAT))
            if ClientMsg == "login":
                login(client)
    except:
        print("Error")
    finally:
        client.close()


try:
    main()
except:
    print("Error")

