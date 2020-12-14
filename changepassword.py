from tkinter import *
from tkinter.ttk import *
from sqlite3 import *
from tkinter import messagebox

class Changepasswordframe(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.style = Style()

        self.style.configure('TFrame', background = 'Aqua')

        self.place(relx = .5, rely = .5, anchor = CENTER)

        self.style.configure('TLabel', background = 'Aqua', font = (NONE, 15))

        self.old_password_label = Label(self, text = "Old Password: ")
        self.old_password_label.grid(row = 0, column = 0, sticky = W)

        self.old_password_entry = Entry(self, font = (NONE, 15), show = '*')
        self.old_password_entry.grid(row = 0, column = 1, pady = 10)

        self.new_password_label = Label(self, text = "New Password: ")
        self.new_password_label.grid(row = 1, column = 0, sticky = W)

        self.new_password_entry = Entry(self, font = (NONE, 15), show = '*')
        self.new_password_entry.grid(row = 1, column = 1)

        self.confirm_password_label = Label(self, text = "Confirm Password: ")
        self.confirm_password_label.grid(row = 2, column = 0, sticky = W)

        self.confirm_password_entry = Entry(self, font = (NONE, 15), show = '*')
        self.confirm_password_entry.grid(row = 2, column = 1, pady = 10)

        self.style.configure('TButton', font = (NONE, 15))

        self.change_password_button = Button(self, text = "Change Password",
        width = 20, command = self.change_password_button_click)
        self.change_password_button.grid(row = 3, column = 1, pady = 10)

    def change_password_button_click(self):
        con = connect('myclients.db')
        cur = con.cursor()
        cur.execute("select * from Login where Password = ?", (self.old_password_entry.get(),))
        row = cur.fetchone()
        if row is not None:
            new_password = self.new_password_entry.get()
            confirm_password = self.confirm_password_entry.get()
            if new_password == confirm_password:
                cur.execute("""update login set password = ? where password = ?
                """, (
                    self.new_password_entry.get(),
                    self.old_password_entry.get()
                ))
                con.commit()
                messagebox.showinfo("success message", "password is changed successfully")
            else:
                messagebox.showerror("error message", "new and confirm passwords didn't match")
        else:
            messagebox.showerror("error message", "incorrect old password")
