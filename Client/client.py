import socket

IP = "127.0.0.1"
PORT = 64320
FORMAT = "utf8"


# ------------------------ function -------------------------------
def sendList(client, listItems):
    for items in listItems:
        client.sendall(items.encode(FORMAT))
        client.recv(1024)
    msg = "end"
    client.send(msg.encode(FORMAT))


def recvList(client):
    items = client.recv(1024).decode(FORMAT)
    listRevc = []
    while items != "end":
        listRevc.append(items)
        client.sendall(items.encode(FORMAT))
        items = client.recv(1024).decode(FORMAT)

    return listRevc


def login(client):
    account = []
    user = input("user:")
    passw = input("password:")
    account.append(user)
    account.append(passw)
    sendList(client, account)
    status = client.recv(1024).decode(FORMAT)
    print(status)


def signUp(client):
    account = []
    username = input("New user: ")
    pwd = input("Password: ")
    confirm_pwd = input("Confirm_pwd: ")
    if pwd != confirm_pwd:
        print("Mat khau xac nhan khong dung")
        return False
    else:
        account.append(username)
        account.append(pwd)

    sendList(client, account)
    status = client.recv(1024).decode(FORMAT)
    print(status)


def ReceiveDataCovid19(client):
    list = recvList(client)
    print(f"Số ca nhiễm: {list[1]}")
    print(f"Số ca tử vong: {list[3]}")
    print(f"Số hồi phục: {list[5]}")


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
            if len(ClientMsg) <= 0:
                break
            if ClientMsg == "login":
                login(client)
            if ClientMsg == "signup":
                signUp(client)
            if ClientMsg.lower() == "search":
                client.recv(1024).decode(FORMAT)
                country = input("Enter country you want to search: ")
                client.sendall(country.encode(FORMAT))
                ReceiveDataCovid19(client)

    except:
        print("Error")
        client.close()
    finally:
        client.close()


try:
    main()
except:
    print("Error")
