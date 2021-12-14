import socket
import threading
import pyodbc
import requests
import json
import sys

from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *

from tkinter import scrolledtext

# Database
response_API = requests.get('https://coronavirus-19-api.herokuapp.com/countries')
data = response_API.text
parse_json = json.loads(data)

IP = "127.0.0.1"
PORT = 64320
FORMAT = "utf8"

LARGE_FONT = ("Consolas", 13, "bold")

BG = "light blue"

# SQL Server
conxLogin = pyodbc.connect('DRIVER={SQL Server};\
                            SERVER=113.166.143.111;PORT=1434;\
                            Database=account;\
                            UID=dh; PWD=1234;')

conxDatabase = pyodbc.connect(' DRIVER={SQL Server};\
                                SERVER=113.166.143.111;PORT=1434;\
                                Database=CoronaData;\
                                UID=dh; PWD=1234;')

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


Live_Account = []
HISTORY = []



def Remove_LiveAccount(username):
    for i in Live_Account:
        if i == username:
            Live_Account.remove(i)
            return


Live_Account = []


def Check_LiveAccount(username):
    for row in Live_Account:
        parse = row.find("-")
        parse_check = row[(parse + 1):]
        if parse_check == username:
            return False
    return True


def Remove_LiveAccount(username):
    for i in Live_Account:
        if i == username:
            Live_Account.remove(i)
            return

nClient = 0
def handleClient(conn, addr):
    global nClient
    print("Client ", addr, "connect")
    now = datetime.now()
    timenow = now.strftime("%d/%m/%Y %H:%M:%S")
    text = str(timenow) + " Client " + str(addr) + " connect"
    HISTORY.append(text)
    ClientMsg = None
    while ClientMsg != "x":
        ClientMsg = conn.recv(1024).decode(FORMAT)
        print("Client: ", ClientMsg)
        if ClientMsg == "login":
            conn.send("Dont care".encode(FORMAT))
            account = recvList(conn)
            checkLogin(conn, account)
        if ClientMsg == "signup":
            conn.send("Dont care".encode(FORMAT))
            newAccount = recvList(conn)
            CheckSignUp(conn, newAccount)
        if ClientMsg == "search":
            conn.sendall("Which country do you want to search ?".encode(FORMAT))
            country = conn.recv(1024).decode(FORMAT)
            Search(conn, country)
        if not ClientMsg:
            break

    Remove_LiveAccount(account[0])
    now = datetime.now()
    timenow = now.strftime("%d/%m/%Y %H:%M:%S")
    text = str(timenow) + " Client " + str(addr) + " disconnect"
    HISTORY.append(text)
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
        Live_Account.append(account[0])
        return True
    else:
        print(LOGINFAILED)
        conn.sendall(LOGINFAILED.encode(FORMAT))
        return False


def CheckSignUp(conn, account):
    cursor = conxLogin.cursor()
    cursor.execute("Select * from account where username=?", account[0])
    data = cursor.fetchall()
    if not data:
        cursor.execute("INSERT INTO account(username, pass) values (?, ?)", account[0], account[1])
        conxLogin.commit()
        conn.sendall(SIGNUPSUCESS.encode(FORMAT))
    else:
        conn.sendall("Username has been registration".encode(FORMAT))


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
    lst = []
    lst_Empty = ["empty"]
    cursor.execute("Select * from CoronaData where country = ?", country)
    lst = cursor.fetchall()
    if not lst:
        sendList(conn, lst_Empty)
    else:
        sendList(conn, lst[0])


# --------------------------- main ---------------------------------
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((IP, PORT))
s.listen(5)
# UpdateDatabaseFromAPI()
conn, addr=(None, None)
clientNum = -1

def runServer():
    print("Sever is running...")
    global s
    clientNum = app.numberofClients
    if clientNum <= 0:
        print("Sever ended because number of clients = 0")
        sys.exit(1)
    print("Waiting for Client")
    global nClient
    while nClient < clientNum:
        try:
            conn, addr = s.accept()
            thr = threading.Thread(target=handleClient, args=(conn, addr))
            thr.daemon = False
            thr.start()
        except:
            exit(1)
        finally:
            nClient=nClient+1

    s.close()


class Admin(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # self.iconbitmap('soccer-ball.ico')
        self.title("COVID SEARCH ENGINE SERVER")
        self.geometry("500x300")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.resizable(width=False, height=False)
        self.numberofClients = 0
        self.checkThread = False
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.page = container
        self.close=False

        self.frames = {}
        for F in (StartPage, NextPage, HomePage):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.showFrame(StartPage)

    def showFrame(self, container):

        frame = self.frames[container]
        self.page = container
        if container == StartPage:
            self.geometry("500x200")
        elif container == NextPage:
            self.geometry("500x200")
        else:
            self.geometry("550x650")
        frame.tkraise()

    # close-program function
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.close=True
            global s
            s.close()
            self.destroy()

    def logIn(self, curFrame):
        if self.page != StartPage:
            return None
        user = curFrame.entry_user.get()
        pswd = curFrame.entry_pswd.get()

        if pswd == "":
            curFrame.label_notice["text"] = "password cannot be empty"
            return

        if user == "admin" and pswd == "server":
            self.showFrame(NextPage)
            curFrame.label_notice["text"] = ""
        else:
            curFrame.label_notice["text"] = "invalid username or password"

    def Setting(self, curFrame):
        if self.page != NextPage:
            return None
        self.numberofClients = int(curFrame.entry_nClient.get())
        if self.numberofClients<=0:
            curFrame.label_notice["text"]="You must type a positive integer"
            return
        self.showFrame(HomePage)

        if self.checkThread == False:
            Thread.start()
            self.checkThread = True


class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg=BG)

        label_title = tk.Label(self, text="\nLOG IN FOR SEVER\n", font=LARGE_FONT, fg='#209b93', bg=BG).grid(
            row=0, column=1)

        label_user = tk.Label(self, text="\tUSERNAME ", fg='#209b93', bg=BG, font='consolas 12 bold').grid(row=1,
                                                                                                           column=0)
        label_pswd = tk.Label(self, text="\tPASSWORD ", fg='#209b93', bg=BG, font='consolas 12 bold').grid(row=2,
                                                                                                           column=0)

        self.label_notice = tk.Label(self, text="", bg=BG, fg='red')
        self.entry_user = tk.Entry(self, width=30, bg='white')
        self.entry_pswd = tk.Entry(self, width=30, bg='white', show="*")

        button_log = tk.Button(self, text="LOG IN", bg="#209b93", fg='white',
                               command=lambda: controller.logIn(self))

        button_log.grid(row=4, column=1)
        button_log.configure(width=10)
        self.label_notice.grid(row=3, column=1)
        self.entry_pswd.grid(row=2, column=1)
        self.entry_user.grid(row=1, column=1)


class NextPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg=BG)
        label_title = tk.Label(self, text="\nSEVER SETTING\n", font=LARGE_FONT, fg='#209b93', bg=BG).grid(row=0, column=1)
        label_nClient = tk.Label(self, text="   NUMBER OF CLIENTS  ", fg='#209b93', bg=BG, font='consolas 11 bold').grid(row=2, column=0)
        self.label_notice = tk.Label(self, text="", bg=BG, fg='red')
        self.entry_nClient = tk.Entry(self, width=30, bg='white')

        button_log = tk.Button(self, text="NEXT", bg="#209b93", fg='white', command=lambda: controller.Setting(self))

        button_log.grid(row=4, column=1)
        button_log.configure(width=10)
        self.label_notice.grid(row=3, column=1)
        self.entry_nClient.grid(row=2, column=1)


class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.configure(bg=BG)
        label_title = tk.Label(self, text="\n ONLINE ACCOUNTS\n", font=LARGE_FONT, fg='#209b93', bg=BG).pack()
        label_title2 = tk.Label(self, text="\n HISTORY\n", font="consolas 14 bold", fg="#209b93", bg=BG).place(x=230,y=300)
        self.conent = tk.Frame(self)
        self.data = tk.Listbox(self.conent, height=10,
                               width=42,
                               bg="white",
                               activestyle='dotbox',
                               font="Helvetica",
                               fg='#20639b')
        self.data2 = scrolledtext.ScrolledText(self, width=58, height=15)
        self.data2.place(x=35, y=350)
        button_log = tk.Button(self, text="REFRESH", bg="#209b93", fg='white', command=self.Update_Client)
        button_back = tk.Button(self, text="CLOSE", bg="#209b93", fg='white',
                                command=lambda: controller.on_closing())
        button_back.pack(side=BOTTOM)
        button_back.configure(width=10)
        button_log.pack(side=BOTTOM)
        button_log.configure(width=10)

        self.conent.pack_configure()
        self.scroll = tk.Scrollbar(self.conent)
        self.scroll.pack(side=RIGHT, fill=BOTH)
        self.data.config(yscrollcommand=self.scroll.set)

        self.scroll.config(command=self.data.yview)
        self.data.pack()

    def Update_Client(self):
        self.data.delete(0, len(Live_Account))
        for i in range(len(Live_Account)):
            self.data.insert(i, Live_Account[i])
        self.data2.delete('1.0', END)
        for i in HISTORY:
            self.data2.insert(INSERT, i + "\n")


app = Admin()

Thread = threading.Thread(target=runServer)
Thread.daemon = False

app.mainloop()

# app=Admin()
# app.mainloop()


# runSever()
