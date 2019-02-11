from tkinter import *
from contextlib import suppress
import os
from PIL import ImageTk, Image

if os.name == 'nt':
    separator = '\\'
else:
    separator = '/'


class Duel_Helper:
    def __init__(self):
        self.c_id = 0

    def validate_login(self):
        c_id = c_id_entry.get()
        password = password_entry.get()

        self.c_id = c_id

        client = get_client()
        client_command = client.Command()
        if client_command.validate_login(c_id, password):
            login_frame.destroy()
            home_frame.pack()
            home_frame.tkraise()

    def file_dialog_box(self):
        from tkinter import Tk
        from tkinter.filedialog import askopenfilename

        Tk().withdraw()
        self.file_path = askopenfilename()

        program_file_var.set(self.file_path)

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

    def accept_challenge(self):
        client = get_client()
        client_command = client.Command()
        p_title = challenge_key_entry.get() + ".txt"
        client_command.accept_challenge(p_title)
        try:
            question_spec = open(p_title, 'r')
            question = question_spec.read()
            question_text.insert(1.0, question)
            question_spec.close()
        except:
            question_text.insert(1.0, "No Such Challenge!")

duel_helper = Duel_Helper()

def get_client():
    try:
        import client
        return client
    except:
        with suppress(Exception):
            from Client import client
            return client

root = Tk()
root.title("CodeDuel")

login_background = ImageTk.PhotoImage(Image.open("/Users/ajayraj/Documents/CodeDuel/Resources/background.jpg"))
home_background = ImageTk.PhotoImage(Image.open("/Users/ajayraj/Documents/CodeDuel/Resources/background.jpg"))

login_frame = Frame(root, width=1366, height=768)
home_frame = Frame(root, width=1366, height=768)

login_background_label = Label(login_frame, image=login_background)
login_background_label.pack()

home_background_label = Label(home_frame, image=home_background)
home_background_label.pack()

login_frame.pack()

# ********************* LOGIN PAGE ************************* #

c_id_label = Label(login_frame, text="Contestant ID", bg='light blue', highlightbackground='#84BEEF')
c_id_label.place(x=200, y=100, width=100, height=30)

c_id_entry = Entry(login_frame, highlightbackground='#84BEEF')
c_id_entry.place(x=450, y=100, width=200, height=30)

password_label = Label(login_frame, text="Password", bg='light blue', highlightbackground='#84BEEF')
password_label.place(x=200, y=150, width=100, height=30)

password_entry = Entry(login_frame, show="*", highlightbackground='#84BEEF')
password_entry.place(x=450, y=150, width=200, height=30)

login_button = Button(login_frame, text="Login", command=duel_helper.validate_login, bg='light blue', highlightbackground='#84BEEF')
login_button.place(x=325, y=250, width=200, height=25)

login_frame.tkraise()


# ********************* HOME PAGE ************************* #

scoreboard_label = Label(home_frame, text="Scoreboard", bg="light blue")
scoreboard_label.place(x=900, y=40, width=200, height=20)

contestant_var = StringVar()
contestant_label = Label(home_frame, textvar=contestant_var, anchor=W, bg='light green')
contestant_label.place(x=900, y=80, width=200, height=50)

opponent_var = StringVar()
opponent_label = Label(home_frame, textvar=opponent_var, anchor=W, bg='red')
opponent_label.place(x=900, y=140, width=200, height=50)

refresh_button = Button(home_frame, text="Refresh", command=duel_helper.update_scoreboard, highlightbackground='#84BEEF')
refresh_button.place(x=900, y=200, width=200, height=25)

challenge_key_label = Label(home_frame, text="Challenge Key", bg="light blue")
challenge_key_label.place(x=50, y=50)

challenge_key_entry = Entry(home_frame)
challenge_key_entry.place(x=200, y=50, width=300, height=30)

accept_challenge_button = Button(home_frame, text="Accept Challenge", command=duel_helper.accept_challenge, highlightbackground='#84BEEF')
accept_challenge_button.place(x=550, y=50, width=200, height=25)

question_text = Text(home_frame)
question_text.place(x=50, y=100, width = 700, height = 520)

program_file_label = Label(home_frame, text="Program File", bg="light blue")
program_file_label.place(x=50, y=650)

program_file_var = StringVar()
program_file_entry = Entry(home_frame, textvar=program_file_var, highlightbackground='#84BEEF')
program_file_entry.place(x=165, y=650, width=400, height=30)

program_file_button = Button(home_frame, text="Select File", command=duel_helper.file_dialog_box, highlightbackground='#84BEEF')
program_file_button.place(x=600, y=650, width=150, height=25)

push_file_button = Button(home_frame, text="Push File", command=duel_helper.request_upload, highlightbackground='#84BEEF')
push_file_button.place(x=165, y = 700, width=100, height=25)

root.mainloop()
