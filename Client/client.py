import socket
from tkinter import *
import tkinter as tk
from tkinter import messagebox

IP_default = "127.0.0.1"
PORT = 64320
FORMAT = "utf8"

LOGIN_SUCCESS = "Login successfully"
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


class StartPage(tk.Frame):
    def __init__(self, frame, appController):
        Frame.__init__(self, frame)
        self.stt_Connect = False
        Label(self, text="COVID-19 IN THE WORLD", font=("Arial", 16), fg="blue").place(x=130, y=20)
        Label(self, text="Enter IP server to connect:", font=("Arial", 10)).place(x=40, y=80)

        self.entry_IP = Entry(self, width=25)
        self.entry_IP.insert(0, "127.0.0.1")
        self.entry_IP.place(x=220, y=80)
        self.btn_Connect = Button(self, text="Connect",
                                  command=lambda: self.Check_Connect(self, self.entry_IP.get()))
        self.btn_Connect.place(x=400, y=75)

        self.note = Label(self, text="Note: Please connect to server after login", font=("Arial", 8),
                          fg="red")
        self.note.place(x=40, y=140)

        self.btn_login = Button(self, text="Login", fg="blue", activebackground="blue", activeforeground="white",
                                height=2, width=10, underline=1, bd=3, command=lambda: appController.show_frame(Login))
        self.btn_login["state"] = DISABLED
        self.btn_login.place(x=90, y=200)

        self.btn_signUp = Button(self, text="Sign up", fg="green", activebackground="green", activeforeground="white",
                                 height=2,
                                 width=10, underline=1, bd=3, command=lambda: appController.show_frame(SignUp))
        self.btn_signUp["state"] = DISABLED
        self.btn_signUp.place(x=320, y=200)

    def Check_Connect(self, frame, IP_input):
        try:
            if not IP_input:
                IP_input = IP_default
            client.connect((IP_input, PORT))
            self.stt_Connect = True
        except:
            self.stt_Connect = False
        if self.stt_Connect:
            Label(frame, text="Connect successfully. You can login or sign up", fg="green").place(x=40, y=110)
            self.entry_IP["state"] = DISABLED
            self.btn_Connect["state"] = DISABLED
            self.btn_signUp["state"] = NORMAL
            self.btn_login["state"] = NORMAL
            self.note.configure(text="")
        else:
            Label(frame, text="Failed to connect to server. Please check again", fg="red").place(x=40, y=110)


class Login(tk.Frame):
    def __init__(self, frame, appController):
        Frame.__init__(self, frame)
        self.account = ["", ""]

        Label(self, text="LOGIN", font=("Arial", 15)).place(x=220, y=50)

        Label(self, text="Username:", font=("Arial", 10)).place(x=70, y=110)
        self.txt_user = Entry(self, width=40)
        self.txt_user.place(x=150, y=110)
        Label(self, text="Password:", font=("Arial", 10)).place(x=70, y=170)
        self.txt_pass = Entry(self, width=40, show="*")
        self.txt_pass.place(x=150, y=170)
        self.btn_Login = Button(self, text="Go back", fg="black", activebackground="blue", activeforeground="white",
                                height=2, width=10, underline=1, bd=3,
                                command=lambda: appController.show_frame(StartPage))
        self.btn_Login.place(x=10, y=10)
        self.btn_Login = Button(self, text="Login", fg="blue", activebackground="blue", activeforeground="white",
                                height=2, width=10, underline=1, bd=3, command=lambda: self.CheckLogin())
        self.btn_Login.place(x=210, y=230)
        self.Status = Label(self, text="", font=("Arial", 10), fg="red")
        self.Status.place(x=150, y=200)

    def setAccount(self):
        self.account[0] = self.txt_user.get()
        self.account[1] = self.txt_pass.get()

    def CheckLogin(self):
        self.setAccount()
        if not self.account[0]:
            self.Status.configure(text="Username cannot be empty")
        elif not self.account[1]:
            self.Status.configure(text="Password cannot be empty")
        else:
            self.sendList()
            status = client.recv(1024).decode(FORMAT)
            self.Status.configure(text=status)
            # if self.Status == LOGIN_SUCCESS:
            #     appController.show_frame(Lookup_Covid19)

    def sendList(self):
        client.sendall("login".encode(FORMAT))
        for items in self.account:
            client.sendall(items.encode(FORMAT))
            client.recv(1024)
        msg = "end"
        client.send(msg.encode(FORMAT))


class SignUp(tk.Frame):
    def __init__(self, frame, appController):
        Frame.__init__(self, frame)
        self.account = ["", ""]

        Label(self, text="SIGN UP", font=("Arial", 15)).place(x=220, y=50)
        Label(self, text="Username:", font=("Arial", 10)).place(x=50, y=110)
        Label(self, text="Password:", font=("Arial", 10)).place(x=50, y=150)
        Label(self, text="Confirm password: ", font=("Arial", 10)).place(x=50, y=190)

        self.txt_user = Entry(self, width=40)
        self.txt_user.place(x=170, y=110)

        self.txt_pass = Entry(self, width=40, show="*")
        self.txt_pass.place(x=170, y=150)

        self.txt_confirm = Entry(self, width=40, show="*")
        self.txt_confirm.place(x=170, y=190)
        self.btn_Login = Button(self, text="Trang chủ", fg="black", activebackground="blue", activeforeground="white",
                                height=2, width=10, underline=1, bd=3,
                                command=lambda: appController.show_frame(StartPage))
        self.btn_Login.place(x=10, y=10)
        self.btn_Login = Button(self, text="Đăng kí", fg="blue", activebackground="blue", activeforeground="white",
                                height=2,
                                width=10, underline=1, bd=3, command=self.CheckSignUp)
        self.btn_Login.place(x=210, y=240)
        self.Status = Label(self, text="", font=("Arial", 10), fg="red")
        self.Status.place(x=150, y=210)

    def setAccount(self):
        self.account[0] = self.txt_user.get()
        self.account[1] = self.txt_pass.get()

    def CheckSignUp(self):
        self.setAccount()
        if not self.account[0]:
            self.Status.configure(text="Username cannot be empty")
        elif not self.account[1]:
            self.Status.configure(text="Password cannot be empty")
        elif self.txt_pass.get() != self.txt_confirm.get():
            self.Status.configure(text="Confirm password is incorrect")
            return
        else:
            self.sendList()
            status = client.recv(1024).decode(FORMAT)
            self.Status.configure(text=status)

    def sendList(self):
        client.sendall("signup".encode(FORMAT))
        for items in self.account:
            client.sendall(items.encode(FORMAT))
            client.recv(1024)
        msg = "end"
        client.send(msg.encode(FORMAT))




def recvList():
    items = client.recv(1024).decode(FORMAT)
    listRevc = []
    while items != "end":
        listRevc.append(items)
        client.sendall(items.encode(FORMAT))
        items = client.recv(1024).decode(FORMAT)

    return listRevc


def ReceiveDataCovid19():
    list = recvList(client)
    if list[0] == "empty":
        print(f"Country is not exist, Please check again")
        return
    print(f"Số ca nhiễm: {list[1]}")
    print(f"Số ca tử vong: {list[3]}")
    print(f"Số hồi phục: {list[5]}")


class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.geometry("500x300")
        self.title("COVID SEARCH ENGINE CLIENT")
        self.resizable(width=False, height=False)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        container = Frame()
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (Login, SignUp, StartPage):
            frame = F(container, self)
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[F] = frame

    # close-programe function
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            global client
            client.close()
            self.destroy()

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


try:
    app = App()
    app.mainloop()
except:
    print("Error")
