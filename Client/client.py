import socket
from tkinter import *
import tkinter as tk
import tkinter
from tkinter import messagebox
from datetime import datetime

IP_default = "127.0.0.1"
PORT = 64320
FORMAT = "utf8"

LOGIN_SUCCESS = "Login successfully"

# Time
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def receiveList():
    items = client.recv(1024).decode(FORMAT)
    listRevc = []
    while items != "end":
        listRevc.append(items)
        client.sendall(items.encode(FORMAT))
        items = client.recv(1024).decode(FORMAT)

    return listRevc


class StartPage(tk.Frame):
    def __init__(self, frame, appController):
        Frame.__init__(self, frame)
        self.stt_Connect = False
        Label(self, text="COVID-19 IN THE WORLD", font=("Arial", 16), fg="blue").place(x=130, y=20)
        Label(self, text="Enter IP server to connect:", font=("Arial", 10)).place(x=40, y=80)

        self.entry_IP = Entry(self, width=25)
        self.entry_IP.insert(0, "127.0.0.1")
        self.entry_IP.place(x=220, y=80)
        self.btn_Connect = Button(self, text="Connect", bg="#66FF66",
                                  command=lambda: self.Check_Connect(self, self.entry_IP.get()))
        self.btn_Connect.place(x=400, y=75)

        self.note = Label(self, text="Note: Please connect to server before login", font=("Arial", 8),
                          fg="red")
        self.note.place(x=40, y=140)

        self.btn_login = Button(self, text="Login", fg="blue", bg="white", activebackground="blue",
                                activeforeground="white", height=2, width=10, underline=1, bd=3,
                                command=lambda: appController.show_frame(Login))
        self.btn_login["state"] = DISABLED
        self.btn_login.place(x=90, y=200)

        self.btn_signUp = Button(self, text="Sign up", fg="green", bg="white", activebackground="white",
                                 activeforeground="green", height=2, width=10, underline=1, bd=3,
                                 command=lambda: appController.show_frame(SignUp))
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

    # def Logout(self, appController):
    #     global client
    #     client.close()
    #     client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     appController.show_frame(StartPage)
    #     self.entry_IP["state"] = NORMAL
    #     self.btn_Connect["state"] = NORMAL
    #     self.btn_signUp["state"] = DISABLED
    #     self.btn_login["state"] = DISABLED


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
        self.btn_goBack = Button(self, text="Go back", fg="black", bg="gray", activebackground="#CCCC99",
                                 activeforeground="black", height=2, width=10, underline=1, bd=3,
                                 command=lambda: appController.show_frame(StartPage))
        self.btn_goBack.place(x=10, y=10)
        self.btn_Login = Button(self, text="Login", fg="white", bg="blue", activebackground="white",
                                activeforeground="blue", height=2, width=10, underline=1, bd=3,
                                command=lambda: self.CheckLogin(appController))
        self.btn_Login.place(x=210, y=230)
        self.Status = Label(self, text="", font=("Arial", 10), fg="red")
        self.Status.place(x=150, y=200)

    def setAccount(self):
        self.account[0] = self.txt_user.get()
        self.account[1] = self.txt_pass.get()

    def CheckLogin(self, appController):
        self.setAccount()
        if not self.account[0]:
            self.Status.configure(text="Username cannot be empty")
        elif not self.account[1]:
            self.Status.configure(text="Password cannot be empty")
        else:
            self.sendList()
            status = client.recv(1024).decode(FORMAT)
            if status == "exit":
                messagebox.showerror("Error", "Sever closed")
                client.close()
                self.destroy()
            self.Status.configure(text=status)
            if status == LOGIN_SUCCESS:
                appController.show_frame(SearchPage)
                self.Status.configure(text="")

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
        self.btn_goBack = Button(self, text="Go back", fg="black", bg="gray", activebackground="#CCCC99",
                                 activeforeground="black", height=2, width=10, underline=1, bd=3,
                                 command=lambda: appController.show_frame(StartPage))
        self.btn_goBack.place(x=10, y=10)
        self.btn_signUp = Button(self, text="Sign up", fg="blue", activebackground="blue", activeforeground="white",
                                 height=2,
                                 width=10, underline=1, bd=3, command=self.CheckSignUp)
        self.btn_signUp.place(x=210, y=240)
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
            if status == "exit":
                messagebox.showerror("Error", "Sever closed")
                client.close()
                self.destroy()
            self.Status.configure(text=status)

    def sendList(self):
        client.sendall("signup".encode(FORMAT))
        client.recv(1024)
        for items in self.account:
            client.sendall(items.encode(FORMAT))
            client.recv(1024)
        msg = "end"
        client.send(msg.encode(FORMAT))


class SearchPage(tk.Frame):
    def __init__(self, frame, appController):
        Frame.__init__(self, frame)
        self.frame = frame
        # self.startPage = StartPage.__init__(frame, appController)
        self.covidData = []
        title = Label(self, text="COVID-19 WORLD", fg="blue", bd=0, bg="#ADD8E6",
                      font=("Transformers Movie", 20))
        title.pack(pady=5)
        Label(self, text="Find number of cases in the country in the world", font=("Arial", 10)).place(x=50, y=50)
        Label(self, text="Example: USA, Vietnam, Cambodia, ...", font=("Arial", 10)).place(x=50, y=70)
        Label(self, text="Regardless of uppercase or lowercase. Example: USA <-> usa, ...", font=("Arial", 10)).place(
            x=50, y=90)
        self.txt_Country = Entry(self, width=48, font=("Arial", 10))
        self.txt_Country.place(x=60, y=122)
        self.btn_Submit = Button(self, text='Search', command=self.divide_cast,
                                 fg="white", bg="green", activebackground="blue", activeforeground="white",
                                 width=5, underline=1, bd=3)
        self.btn_Submit.place(x=400, y=120)

        self.error = tkinter.Label(self, text="", fg="red")
        self.error.place(x=60, y=145)

        # self.btn_goBack = Button(self, text="Log out", fg="black", bg="gray", activebackground="#CCCC99",
        #                          activeforeground="black", height=2, width=10, underline=1, bd=3,
        #                          command=lambda: StartPage.Logout(self.startPage, appController))
        # self.btn_goBack.place(x=3, y=3)
        self.btn_today = Button(self, text='Today', command=self.show_today,
                                fg="black", activebackground="blue",
                                activeforeground="white", font=("Arial", 11),
                                width=5, underline=1, bd=3)
        self.btn_today.place(x=100, y=165)
        self.btn_today["state"] = DISABLED
        self.btn_total = Button(self, text='Total', command=self.show_total,
                                fg="black", activebackground="blue",
                                activeforeground="white", font=("Arial", 11),
                                width=5, underline=1, bd=3)
        self.btn_total.place(x=300, y=165)
        self.btn_total["state"] = DISABLED

        self.title = tk.Label(self)
        self.cases = tk.Label(self)
        self.deaths = tk.Label(self)
        self.recovered = tk.Label(self)

        self.casesTitle = tk.Label(self)
        self.deathsTitle = tk.Label(self)
        self.recoveredTitle = tk.Label(self)

    def CheckError(self, number):
        self.refresh_table()
        self.btn_today["state"] = DISABLED
        self.btn_total["state"] = DISABLED
        if number == 0:
            self.error.configure(text="Please input country to search")
        if number == -1:
            self.error.configure(text=f"{self.txt_Country.get()} does not exist")
        if number == 1:
            self.error.configure(text="")

    def ReceiveDataCovid19(self):
        self.covidData = receiveList()
        if self.covidData[0] == "empty":
            self.CheckError(-1)
        else:
            self.btn_today["state"] = NORMAL
            self.btn_total["state"] = NORMAL

    def refresh_table(self):
        self.title.configure(text="", width=0, borderwidth=0, bg="SystemButtonFace")
        self.title.place(x=0, y=0)
        self.cases.configure(text="", width=0, height=0, borderwidth=0, bg="SystemButtonFace")
        self.cases.place(x=0, y=0)
        self.deaths.configure(text="", width=0, height=0, borderwidth=0, bg="SystemButtonFace")
        self.deaths.place(x=0, y=0)
        self.recovered.configure(text="", width=0, height=0, borderwidth=0, bg="SystemButtonFace")
        self.recovered.place(x=0, y=0)

        self.casesTitle.configure(text="", width=0, borderwidth=0, bg="SystemButtonFace")
        self.casesTitle.place(x=0, y=0)
        self.deathsTitle.configure(text="", width=0, borderwidth=0, bg="SystemButtonFace")
        self.deathsTitle.place(x=0, y=0)
        self.recoveredTitle.configure(text="", width=0, borderwidth=0, bg="SystemButtonFace")
        self.recoveredTitle.place(x=0, y=0)

    def show_total(self):
        self.refresh_table()
        self.btn_total["state"] = DISABLED
        self.btn_today["state"] = NORMAL
        self.title.configure(text=f"{self.txt_Country.get().upper()}", width=30, fg="white", bg="#990000",
                             font=("Arial", 16), borderwidth=3, relief="solid")
        self.title.place(x=65, y=200)

        self.casesTitle.configure(text="Cases", width=17, fg="white", bg="blue", borderwidth=2, relief="solid")
        self.casesTitle.place(x=65, y=230)

        self.deathsTitle.configure(text="Deaths", width=17, fg="white", bg="blue", borderwidth=2, relief="solid")
        self.deathsTitle.place(x=190, y=230)
        self.recoveredTitle.configure(text="Recovered", width=16, fg="white", bg="blue", borderwidth=2,
                                      relief="solid")
        self.recoveredTitle.place(x=315, y=230)
        self.cases.configure(text=f'{int(self.covidData[1]):,d}', width=17, height=2, bg="#009999", borderwidth=2,
                             relief="solid")
        self.cases.place(x=65, y=250)
        self.deaths.configure(text=f'{int(self.covidData[3]):,d}', width=17, height=2, bg="#009999",
                              borderwidth=2,
                              relief="solid")
        self.deaths.place(x=190, y=250)
        self.recovered.configure(text=f'{int(self.covidData[5]):,d}', width=16, height=2, bg="#009999",
                                 borderwidth=2,
                                 relief="solid")
        self.recovered.place(x=315, y=250)

    def show_today(self):
        self.refresh_table()
        self.btn_today["state"] = DISABLED
        self.btn_total["state"] = NORMAL
        self.title.configure(text=f"{self.txt_Country.get().upper()} - {dt_string}", fg="white", width=22,
                             bg="#990000", font=("Arial", 14), borderwidth=3, relief="solid")
        self.title.place(x=110, y=200)
        self.casesTitle.configure(text="Cases", width=17, fg="white", bg="blue", borderwidth=2, relief="solid")
        self.casesTitle.place(x=110, y=230)
        self.deathsTitle.configure(text="Deaths", width=17, fg="white", bg="blue", borderwidth=2, relief="solid")
        self.deathsTitle.place(x=235, y=230)
        self.cases.configure(text=f'{int(self.covidData[2]):,d}', width=17, height=2, bg="#009999", borderwidth=2,
                             relief="solid")
        self.cases.place(x=110, y=250)
        self.deaths.configure(text=f'{int(self.covidData[4]):,d}', width=17, height=2, bg="#009999",
                              borderwidth=2,
                              relief="solid")
        self.deaths.place(x=235, y=250)

    def divide_cast(self):
        if len(self.txt_Country.get()) == 0:
            self.CheckError(0)
        else:
            self.CheckError(1)
            client.sendall("search".encode(FORMAT))
            client.recv(1024).decode(FORMAT)
            client.sendall(self.txt_Country.get().encode(FORMAT))
            self.ReceiveDataCovid19()


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

        for F in (SearchPage, Login, SignUp, StartPage):
            frame = F(container, self)
            frame.grid(row=0, column=0, sticky="nsew")
            self.frames[F] = frame
        self.show_frame(StartPage)

    # close-programe function
    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?\nYou will disconnect to server.."):
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
