from tkinter import *
from contextlib import suppress
import os

if os.name == 'nt':
    separator = '\\'
else:
    separator = '/'


class Duel_Helper:
    def __init__(self):
        self.c_id = 0

    def file_dialog_box(self):
        from tkinter import Tk
        from tkinter.filedialog import askopenfilename

        Tk().withdraw()
        self.file_path = askopenfilename()

        global var
        var.set(self.file_path)

    def separate_dir_file(self):
        dir_list = self.file_path.split(separator)
        self.dir = separator.join(dir_list[:-1])
        self.file = dir_list[-1]

    def update_scoreboard(self):
        client = get_client()
        client_command = client.Command()
        scoreboard = client_command.get_duel_scores()
        global contestant_var, opponent_var

        contestant_score, opponent_score = scoreboard.split('\n')
        contestant_var.set(contestant_score.replace('->', ''))
        opponent_var.set(opponent_score.replace('->', ''))

    def request_upload(self):
        self.separate_dir_file()
        client = get_client()
        #os.chdir(self.dir)
        client_command = client.Command()
        client_command.push_file(self.file)
        self.update_scoreboard()

duel_helper = Duel_Helper()

def get_client():
    try:
        import client
        return client
    except:
        with suppress(Exception):
            from Client import client
            return client

def validate_login():
    c_id = c_id_entry.get()
    password = password_entry.get()

    duel_helper.c_id = c_id

    client = get_client()
    client_command = client.Command()
    if client_command.validate_login(c_id, password):
        login_frame.destroy()
        home_frame.pack()
        home_frame.tkraise()

root = Tk()
root.title("CodeDuel")

login_frame = Frame(root, width=800, height=400)
home_frame = Frame(root, width=800, height=400)

login_frame.pack()

c_id_label = Label(login_frame, text="Contestant ID")
c_id_label.place(x=200, y=100, width=100, height=30)

c_id_entry = Entry(login_frame)
c_id_entry.place(x=450, y=100, width=200, height=30)

password_label = Label(login_frame, text="Password")
password_label.place(x=200, y=150, width=100, height=30)

password_entry = Entry(login_frame, show="*")
password_entry.place(x=450, y=150, width=200, height=30)

login_button = Button(login_frame, text="Login", command=validate_login)
login_button.place(x=325, y=250, width=200, height=50)

login_frame.tkraise()


# ********************* HOME PAGE ************************* #

scoreboard_label = Label(home_frame, text="Scoreboard")
scoreboard_label.place(x=250, y=30, width=300, height=20)

contestant_var = StringVar()
contestant_label = Label(home_frame, textvar=contestant_var, anchor=W, bg='light blue')
contestant_label.place(x=250, y=70, width=300, height=50)

opponent_var = StringVar()
opponent_label = Label(home_frame, textvar=opponent_var, anchor=W, bg='light green')
opponent_label.place(x=250, y=130, width=300, height=50)

refresh_button = Button(home_frame, text="Refresh", command=duel_helper.update_scoreboard)
refresh_button.place(x=250, y=180, width=300, height=50)

program_file_label = Label(home_frame, text="Program File")
program_file_label.place(x=50, y=300, width=150, height=50)

var = StringVar()
program_file_entry = Entry(home_frame, textvar=var)
program_file_entry.place(x=200, y=310, width=400, height=30)

program_file_button = Button(home_frame, text="Select File", command=duel_helper.file_dialog_box)
program_file_button.place(x=620, y=300, width=150, height=50)

push_file_button = Button(home_frame, text="Push File", command=duel_helper.request_upload)
push_file_button.place(x=200, y = 350, width=100, height=50)

root.mainloop()
