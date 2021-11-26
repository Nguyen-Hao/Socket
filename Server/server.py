import socket
import threading
import pyodbc
import requests
import json

# Database
response_API = requests.get('https://coronavirus-19-api.herokuapp.com/countries')
data = response_API.text
parse_json = json.loads(data)

IP = "127.0.0.1"
PORT = 64320
FORMAT = "utf8"

# SQL Server
conxLogin = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};\
                                    SERVER=LAPTOP-HGNG4440\SQLEXPRESS;\
                                    Database=account;\
                                    UID=dh; PWD=1234; Trusted_Connection=yes')

conxDatabase = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};\
                                    SERVER=LAPTOP-HGNG4440\SQLEXPRESS;\
                                    Database=CoronaData;\
                                    UID=dh; PWD=1234; Trusted_Connection=yes')

# Status Login
LOGINSUCESS = "Login successfully"
LOGINFAILED = "Invalid password"
NOTREGISTRATION = "Username is not registration"
SIGNUPSUCESS = "Sign in success"


# ------------------------ function -------------------------------
def recvList(conn):
    items = conn.recv(1024).decode(FORMAT)
    listRevc = []
    while items != "end":
        listRevc.append(items)
        conn.sendall(items.encode(FORMAT))
        items = conn.recv(1024).decode(FORMAT)

    return listRevc


def sendList(conn, listItems):
    for items in listItems:
        conn.sendall(items.encode(FORMAT))
        conn.recv(1024)
    msg = "end"
    conn.send(msg.encode(FORMAT))


def handleClient(conn, addr):
    print("Client ", addr, "connect")
    ClientMsg = None
    while ClientMsg != "x":
        ClientMsg = conn.recv(1024).decode(FORMAT)
        print("Client: ", ClientMsg)

        if ClientMsg == "login":
            account = recvList(conn)
            checkLogin(conn, account)
        if ClientMsg == "signup":
            newAccount = recvList(conn)
            CheckSignUp(conn, newAccount)
        if ClientMsg == "search":
            conn.sendall("Which country do you want to search ?".encode(FORMAT))
            country = conn.recv(1024).decode(FORMAT)
            Search(conn, country)

    print(f"Client {addr} disconnect")
    conn.close()


def checkLogin(conn, account):
    cursor = conxLogin.cursor()
    cursor.execute("select pass from account where username = ?", account[0])
    passData = cursor.fetchone()
    if passData is None:
        print(NOTREGISTRATION)
        conn.sendall(NOTREGISTRATION.encode(FORMAT))
        return False
    elif account[1] == passData[0].replace(' ', ''):
        print(LOGINSUCESS)
        conn.sendall(LOGINSUCESS.encode(FORMAT))
        return True
    else:
        print(LOGINFAILED)
        conn.sendall(LOGINFAILED.encode(FORMAT))
        return False


def CheckSignUp(conn, account):
    cursor = conxLogin.cursor()
    cursor.execute("Select * from account where username=?", account[0])
    data = cursor.fetchall()
    if data is None:
        cursor.execute("INSERT INTO account(username, pass) values (?, ?)", account[0], account[1])
        conxLogin.commit()
        conn.sendall(SIGNUPSUCESS.encode(FORMAT))
    else:
        conn.sendall("Username has been registration.. please change another username".encode(FORMAT))


def UpdateDatabaseFromAPI():
    cursor = conxDatabase.cursor()
    for i in range(len(parse_json)):
        cursor.execute("UPDATE CoronaData set cases=?, todayCases=?, deaths=?, todayDeaths=?, recovered=?, active=?,\
                    critical=?, casesPerOneMillion=?, deathsPerOneMillion=?, totalTests=?, testsPerOneMillion=?\
                    where country=?;",
                       parse_json[i]["cases"], parse_json[i]["todayCases"],
                       parse_json[i]["deaths"],
                       parse_json[i]["todayDeaths"], parse_json[i]["recovered"], parse_json[i]["active"],
                       parse_json[i]["critical"], parse_json[i]["casesPerOneMillion"],
                       parse_json[i]["deathsPerOneMillion"], parse_json[i]["totalTests"],
                       parse_json[i]["testsPerOneMillion"], parse_json[i]["country"])
        conxDatabase.commit()


def Search(conn, country):
    cursor = conxDatabase.cursor()
    cursor.execute("Select * from CoronaData where country = ?", country)
    data = cursor.fetchall()
    sendList(conn, data[0])


# --------------------------- main ---------------------------------
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((IP, PORT))
    UpdateDatabaseFromAPI()
    clientNum = int(input("Enter number of client connect: "))
    if clientNum <= 0:
        return
    s.listen(5)
    print("Waiting for Client")
    nClient = 0
    while nClient < clientNum:
        try:
            conn, addr = s.accept()
            thr = threading.Thread(target=handleClient, args=(conn, addr))
            thr.daemon = False
            thr.start()
        except:
            print("Error")
        finally:
            nClient += 1

    s.close()


try:
    main()
except:
    print("Something Wrong")
