import socket
from tkinter import *
import tkinter as tk


IP_default = "127.0.0.1"
PORT = 64320
FORMAT = "utf8"

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def Click_Login(frame):
    Login(frame).tkraise()


def Show_Frame(frame):
    frame.tkraise()


def Click_SignUp(frame):
    SignUp(frame)


class StartPage(tk.Frame):
    def __init__(self, frame, appController):
        Frame.__init__(self, frame)
        self.stt_Connect = False
        Label(self, text="COVID-19 IN THE WORLD", font=("Arial", 16), fg="blue").place(x=130, y=20)
        Label(self, text="Nhập địa chỉ IP Server:", font=("Arial", 10)).place(x=40, y=80)

        self.entry_IP = Entry(self, width=25)
        self.entry_IP.place(x=220, y=80)
        self.btn_Connect = Button(self, text="Kết nối",
                                  command=lambda: self.Check_Connect(self, self.entry_IP.get()))
        self.btn_Connect.place(x=400, y=75)

        self.note = Label(self, text="Chú ý: Vui lòng kết nối server trước khi đăng nhập", font=("Arial", 8),
                          fg="red")
        self.note.place(x=40, y=140)

        self.btn_login = Button(self, text="Đăng nhập", fg="blue", activebackground="blue", activeforeground="white",
                                height=2, width=10, underline=1, bd=3, command=lambda: appController.show_frame(Login))
        self.btn_login["state"] = DISABLED
        self.btn_login.place(x=90, y=200)

        self.btn_signUp = Button(self, text="Đăng kí", fg="green", activebackground="green", activeforeground="white",
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
            Label(frame, text="Kết nối thành công. Bạn có thể đăng nhập hoặc đăng kí", fg="green").place(x=40, y=110)
            self.entry_IP["state"] = DISABLED
            self.btn_Connect["state"] = DISABLED
            self.btn_signUp["state"] = NORMAL
            self.btn_login["state"] = NORMAL
            self.note.configure(text="")
        else:
            Label(frame, text="Kết nối thất bại", fg="red").place(x=40, y=110)


class Login(tk.Frame):
    def __init__(self, frame, appController):
        Frame.__init__(self, frame)
        self.account = ["", ""]

        Label(self, text="LOGIN", font=("Arial", 15)).place(x=220, y=50)

        Label(self, text="Username", font=("Arial", 10)).place(x=70, y=110)
        self.txt_user = Entry(self, width=40)
        self.txt_user.place(x=150, y=110)
        Label(self, text="Password ", font=("Arial", 10)).place(x=70, y=170)
        self.txt_pass = Entry(self, width=40, show="*")
        self.txt_pass.place(x=150, y=170)
        self.btn_Login = Button(self, text="Trang chủ", fg="black", activebackground="blue", activeforeground="white",
                                height=2, width=10, underline=1, bd=3, command=lambda: appController.show_frame(StartPage))
        self.btn_Login.place(x=0, y=0)
        self.btn_Login = Button(self, text="Đăng nhập", fg="blue", activebackground="blue", activeforeground="white",
                                height=2, width=10, underline=1, bd=3, command=self.CheckLogin)
        self.btn_Login.place(x=210, y=230)
        self.Status = Label(self, text="", font=("Arial", 10), fg="red")
        self.Status.place(x=150, y=200)

    def setAccount(self):
        self.account[0] = self.txt_user.get()
        self.account[1] = self.txt_pass.get()

    def CheckLogin(self):
        self.setAccount()
        self.sendList()
        status = client.recv(1024).decode(FORMAT)
        self.Status.configure(text=status)

    def sendList(self):
        client.sendall("login".encode(FORMAT))
        client.recv(1024)
        for items in self.account:
            client.sendall(items.encode(FORMAT))
            client.recv(1024)
        msg = "end"
        client.send(msg.encode(FORMAT))


class SignUp(tk.Frame):
    def __init__(self, frame, appController):
        Frame.__init__(self, frame)
        self.account = ["", ""]

        Label(self, text="SIGN UP", font=("Arial", 15)).place(x=220, y=20)
        Label(self, text="Username", font=("Arial", 10)).place(x=90, y=80)
        Label(self, text="Password ", font=("Arial", 10)).place(x=90, y=120)
        Label(self, text="Confirm pass ", font=("Arial", 10)).place(x=90, y=160)

        self.txt_user = Entry(self, width=40)
        self.txt_user.place(x=170, y=80)

        self.txt_pass = Entry(self, width=40)
        self.txt_pass.place(x=170, y=120)

        self.txt_confirm = Entry(self, width=40)
        self.txt_confirm.place(x=170, y=160)
        self.btn_Login = Button(self, text="Trang chủ", fg="black", activebackground="blue", activeforeground="white",
                                height=2, width=10, underline=1, bd=3,
                                command=lambda: appController.show_frame(StartPage))
        self.btn_Login.place(x=0, y=0)
        self.btn_Login = Button(self, text="Đăng kí", fg="blue", activebackground="blue", activeforeground="white",
                                height=2,
                                width=10, underline=1, bd=3, command=self.CheckSignUp)
        self.btn_Login.place(x=210, y=220)
        self.Status = Label(self, text="", font=("Arial", 10), fg="red")
        self.Status.place(x=150, y=200)

    def setAccount(self):
        self.account[0] = self.txt_user.get()
        self.account[1] = self.txt_pass.get()

    def CheckSignUp(self):
        self.setAccount()
        if self.txt_pass.get() != self.txt_confirm.get():
            self.Status.configure(text="Mật khẩu xác nhận không đúng")
            return
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


class App(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.geometry("500x300")
        self.title("Covid-19")
        self.resizable(width=False, height=False)

        container = Frame()
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (Login, SignUp, StartPage):
            frame = F(container, self)
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[F] = frame

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# ------------------------ function -------------------------------


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


# --------------------------- main ---------------------------------
# def main():
#     try:
#         client.connect((IP, PORT))
#
#
#         ClientMsg = None
#         ServerMsg = None
#         while ClientMsg != "x" and ClientMsg != " ":
#             ClientMsg = input("Client: ")
#             client.sendall(ClientMsg.encode(FORMAT))
#             if len(ClientMsg) <= 0:
#                 break
#             if ClientMsg == "login":
#                 login(client)
#             if ClientMsg == "signup":
#                 signUp(client)
#             if ClientMsg.lower() == "search":
#                 client.recv(1024).decode(FORMAT)
#                 country = input("Enter country you want to search: ")
#                 client.sendall(country.encode(FORMAT))
#                 ReceiveDataCovid19(client)
#
#     except:
#         print("Error")
#         client.close()
#     finally:
#         client.close()
try:
    app = App()
    app.mainloop()
except:
    print("Error")