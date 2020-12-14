from tkinter import *
from tkinter.ttk import *
from sqlite3 import *
from tkinter import messagebox
import home

class Loginwindow(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)

        self.title("ClientBook")
        self.geometry('700x550')
        self.resizable(FALSE, FALSE)

        style = Style()

        style.configure('Header.TFrame', background = 'DarkSlateGray',relief='raised')
        header_frame = Frame(self, style = 'Header.TFrame')
        header_frame.pack(fill = X)

        style.configure('Header.TLabel', background = 'DarkSlateGray', foreground = 'GhostWhite', font = (NONE, 25))

        header_label = Label(header_frame, text = "User Login", style = 'Header.TLabel')

        header_label.pack(pady = 10)


        style.configure('Content.TFrame', background = 'LightSkyBlue')

        content_frame = Frame(self, style = 'Content.TFrame')
        content_frame.pack(fill = BOTH, expand = TRUE)

        login_frame = Frame(content_frame, style = 'Content.TFrame')
        login_frame.place(relx = .5, rely = .5, anchor = CENTER)

        style.configure('Login.TLabel', background = 'LightSkyBlue', font = (NONE, 15))

        username_label = Label(login_frame, text = "Username: ", style = 'Login.TLabel')
        username_label.grid(row = 0, column = 0)

        password_label = Label(login_frame, text = "Password: ", style = 'Login.TLabel')
        password_label.grid(row = 1, column = 0)




        self.username_entry = Entry(login_frame, font = (NONE, 15), width = 15,background='LightSkyBlue',foreground = 'blue')
        self.username_entry.grid(row = 0, column = 1, pady = 5)
        self.username_entry.focus()

        self.password_entry = Entry(login_frame, font = (NONE, 15), width = 15, show = '*',background='LightSkyBlue',foreground = 'blue')
        self.password_entry.grid(row = 1, column = 1, pady = 5)

        style.configure('Login.TButton', font = (NONE, 15))

        login_button = Button(login_frame, text = "Login", width = 15,
        style = 'Login.TButton', command = self.login_button_click)
        login_button.grid(row = 2, column = 1, pady = 5)
        login_button.bind('<Return>', self.login_button_click)

    def login_button_click(self, event = None):
        con = connect('myclients.db')
        cur = con.cursor()
        cur.execute("""select * from Login where Username = ? and Password = ?
        """, (self.username_entry.get(), self.password_entry.get()))
        row = cur.fetchone()
        if row is not None:
            self.destroy()
            home.Homewindow()
        else:
            messagebox.showerror("error message", "invalid username/password")

if __name__ == '__main__':
    login_window = Loginwindow()
    login_window.mainloop()

