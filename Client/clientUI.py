from tkinter import *
from contextlib import suppress
import os
from PIL import ImageTk, Image

separator = '/'

def get_client():
    try:
        import client
        return client
    except:
        with suppress(Exception):
            from Client import client
            return client

class GUI:
    def __init__(self):
        self.root = Tk()
        self.root.title("CodeDuel")

    # ********************* LOGIN PAGE ************************* #

    def create_login_page(self):
        self.login_frame = Frame(self.root, width=1366, height=768)

        self.login_background = ImageTk.PhotoImage(Image.open("background.jpg"))
        self.login_background_label = Label(self.login_frame, image=self.login_background)
        self.login_background_label.pack()

        self.c_id_label = Label(self.login_frame, text="Contestant ID", bg='light blue', highlightbackground='#84BEEF')
        self.c_id_label.place(x=200, y=100, width=100, height=30)

        self.c_id_entry = Entry(self.login_frame, highlightbackground='#84BEEF')
        self.c_id_entry.place(x=450, y=100, width=200, height=30)

        self.password_label = Label(self.login_frame, text="Password", bg='light blue', highlightbackground='#84BEEF')
        self.password_label.place(x=200, y=150, width=100, height=30)

        self.password_entry = Entry(self.login_frame, show="*", highlightbackground='#84BEEF')
        self.password_entry.place(x=450, y=150, width=200, height=30)

        self.login_button = Button(self.login_frame, text="Login", command=self.validate_login, bg='light blue', highlightbackground='#84BEEF')
        self.login_button.place(x=325, y=250, width=200, height=25)

    # ********************* HOME PAGE ************************* #

    def create_home_page(self):
        self.home_frame = Frame(self.root, width=1366, height=768)

        self.home_background = ImageTk.PhotoImage(Image.open("background.jpg"))
        self.home_background_label = Label(self.home_frame, image=self.home_background)
        self.home_background_label.pack()

        self.scoreboard_label = Label(self.home_frame, text="Scoreboard", bg="light blue")
        self.scoreboard_label.place(x=900, y=40, width=200, height=20)

        self.contestant_var = StringVar()
        self.contestant_label = Label(self.home_frame, textvar=self.contestant_var, anchor=W, bg='light green')
        self.contestant_label.place(x=900, y=80, width=200, height=50)

        self.opponent_var = StringVar()
        self.opponent_label = Label(self.home_frame, textvar=self.opponent_var, anchor=W, bg='red')
        self.opponent_label.place(x=900, y=140, width=200, height=50)

        self.refresh_button = Button(self.home_frame, text="Refresh", command=self.update_scoreboard, highlightbackground='#84BEEF')
        self.refresh_button.place(x=900, y=200, width=200, height=25)

        self.challenge_key_label = Label(self.home_frame, text="Challenge Key", bg="light blue")
        self.challenge_key_label.place(x=50, y=50)

        self.challenge_key_entry = Entry(self.home_frame, highlightbackground='#84BEEF')
        self.challenge_key_entry.place(x=200, y=50, width=300, height=30)

        self.accept_challenge_button = Button(self.home_frame, text="Accept Challenge", command=self.accept_challenge, highlightbackground='#84BEEF')
        self.accept_challenge_button.place(x=550, y=50, width=200, height=25)

        self.question_text = Text(self.home_frame)
        self.question_text.place(x=50, y=100, width = 700, height = 480)

        self.program_file_label = Label(self.home_frame, text="Program File", bg="light blue")
        self.program_file_label.place(x=50, y=600)

        self.program_file_var = StringVar()
        self.program_file_entry = Entry(self.home_frame, textvar=self.program_file_var, highlightbackground='#84BEEF')
        self.program_file_entry.place(x=165, y=600, width=400, height=30)

        self.program_file_button = Button(self.home_frame, text="Select File", command=self.file_dialog_box, highlightbackground='#84BEEF')
        self.program_file_button.place(x=600, y=600, width=150, height=25)

        self.push_file_button = Button(self.home_frame, text="Push File", command=self.request_upload, highlightbackground='#84BEEF')
        self.push_file_button.place(x=165, y = 660, width=100, height=25)

        self.logout_button = Button(self.home_frame, text="Log Out", command=self.logout, highlightbackground='#84BEEF')
        self.logout_button.place(x=1200, y=40)

    def validate_login(self):
        c_id = self.c_id_entry.get()
        password = self.password_entry.get()

        self.c_id = c_id

        client = get_client()
        client_command = client.Command()
        if client_command.validate_login(c_id, password):
            self.create_home_page()
            self.login_frame.destroy()
            self.home_frame.pack()
            self.home_frame.tkraise()

    def logout(self):
        self.create_login_page()
        self.home_frame.destroy()
        self.login_frame.pack()
        self.login_frame.tkraise()

    def file_dialog_box(self):
        from tkinter import Tk
        from tkinter.filedialog import askopenfilename

        Tk().withdraw()
        self.file_path = askopenfilename()

        self.program_file_var.set(self.file_path)

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
        self.contestant_var.set(contestant_score.replace('->', ''))
        self.opponent_var.set(opponent_score.replace('->', ''))

    def request_upload(self):
        self.separate_dir_file()
        client = get_client()
        client_command = client.Command()
        client_command.push_file(self.file)
        self.update_scoreboard()

    def accept_challenge(self):
        client = get_client()
        client_command = client.Command()
        p_title = self.challenge_key_entry.get() + ".txt"
        client_command.accept_challenge(p_title)
        try:
            question_spec = open(p_title, 'r')
            question = question_spec.read()
            self.question_text.insert(1.0, question)
            question_spec.close()
        except:
            self.question_text.insert(1.0, "No Such Challenge!")

user_interface = GUI()
user_interface.create_login_page()
user_interface.login_frame.pack()
user_interface.login_frame.tkraise()
user_interface.root.mainloop()
