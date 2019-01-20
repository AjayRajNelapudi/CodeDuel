from tkinter import *
from contextlib import suppress

def validate_login():
    c_id = c_id_entry.get()
    password = password_entry.get()

    try:
        import client
        if client.validate_login(c_id, password):
            login_frame.destroy()
            home_frame.pack()
            home_frame.tkraise()
    except:
        with suppress(Exception):
            from Client import client
            if client.validate_login(c_id, password):
                login_frame.destroy()
                home_frame.pack()
                home_frame.tkraise()

root = Tk()
root.title("CodeDuel")

login_frame = Frame(root, width=800, height=600)
home_frame = Frame(root, width=800, height=600)

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

text = Label(home_frame, text = "Logged In")
text.pack()

root.mainloop()
