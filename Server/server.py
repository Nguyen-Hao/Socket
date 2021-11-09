import socket
import threading
import pyodbc

IP = "127.0.0.1"
PORT = 64320
FORMAT = "utf8"

# Database
DRIVER = "SQL Server Native Client 11.0"
SERVER = "LAPTOP-HGNG4440\SQLEXPRESS"
DATABASE = "account"
UID = "dh"
PWD = "1234"

# Status Login
LOGINSUCESS = "Login successfully"
LOGINFAILED = "Invalid password"
NOTREGISTRATION = "Username is not registration"


# ------------------------ function -------------------------------
def recvList(conn):
    items = conn.recv(1024).decode(FORMAT)
    login = []
    while items != "end":
        login.append(items)
        conn.sendall(items.encode(FORMAT))
        items = conn.recv(1024).decode(FORMAT)

    return login


def handleClient(conn, addr):
    print("Client ", addr, "connect")
    ClientMsg = None
    while ClientMsg != "x":
        ClientMsg = conn.recv(1024).decode(FORMAT)
        print("Client: ", ClientMsg)

        if ClientMsg == "login":
            list = recvList(conn)
            checkLogin(conn, list)

    print(f"Client {addr} disconnect")
    conn.close()


def checkLogin(conn, list):
    conx = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};\
                                    SERVER=LAPTOP-HGNG4440\SQLEXPRESS;\
                                    Database=account;\
                                    UID=dh; PWD=1234; Trusted_Connection=yes')
    cursor = conx.cursor()
    cursor.execute("select pass from account where username = ?", list[0])
    passData = cursor.fetchone()
    if passData is None:
        print(NOTREGISTRATION)
        conn.sendall(NOTREGISTRATION.encode(FORMAT))
        return False
    elif list[1] == passData[0].replace(' ', ''):
        print(LOGINSUCESS)
        conn.sendall(LOGINSUCESS.encode(FORMAT))
        return True
    else:
        print(LOGINFAILED)
        conn.sendall(LOGINFAILED.encode(FORMAT))
        return False


# --------------------------- main ---------------------------------
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((IP, PORT))
    clientNum = int(input("Enter number of client connect: "))
    s.listen(5)
    print("Waiting for Client")
    nClient = 0
    while nClient < clientNum:
        try:
            conn, addr = s.accept()
            thr = threading.Thread(target=handleClient, args=(conn, addr))
            thr.daemon = False
            thr.start()
        except error:
            print("Error")
        finally:
            nClient += 1

    s.close()


try:
    main()
except:
    print("Something Wrong")
