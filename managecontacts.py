from tkinter import *
from tkinter.ttk import *
from tkinter import filedialog
from PIL import Image, ImageTk
from sqlite3 import *
from tkinter import messagebox

class Managecontactsframe(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        self.pack(fill = BOTH, expand = TRUE)

        self.style = Style()

        self.style.configure('TFrame', background = 'Aqua')

        self.con = connect('myclients.db')
        self.cur = self.con.cursor()

        self.create_view_all_contacts_frame()

        self.profile_pic_path = ""

    def create_view_all_contacts_frame(self):
        self.view_all_contacts_frame = Frame(self)
        self.view_all_contacts_frame.place(relx = .5,rely = .5, anchor = CENTER)

        self.style.configure('TButton', font = (NONE, 15), width = 20)

        self.add_new_contact_button = Button(self.view_all_contacts_frame,
        text = "Add New Client", command = self.create_add_new_contact_frame)
        self.add_new_contact_button.grid(row = 0, column = 1, sticky = E, pady = 10)

        self.style.configure('TLabel', background = 'Aqua', font = (NONE, 15))

        self.name_label = Label(self.view_all_contacts_frame, text = "Name: ")
        self.name_label.grid(row = 1, column = 0, pady = 10, sticky = W)

        self.name_entry = Entry(self.view_all_contacts_frame, font = (NONE, 15), width = 62)
        self.name_entry.grid(row = 1, column = 1, sticky = W)
        self.name_entry.bind('<KeyRelease>', self.name_entry_key_released)

        self.style.configure('Treeview.Heading', font = (NONE, 15))
        self.style.configure('Treeview', font = (NONE, 14), rowheight = 25)

        self.contacts_treeview = Treeview(self.view_all_contacts_frame,
        columns = ('name', 'phone_no', 'email_id', 'city'), show = 'headings')
        self.contacts_treeview.heading('name', text = "Name", anchor = W)
        self.contacts_treeview.heading('phone_no', text = "Phone No", anchor = W)
        self.contacts_treeview.heading('email_id', text = "Email Id", anchor = W)
        self.contacts_treeview.heading('city', text = "City", anchor = W)
        self.contacts_treeview.column('name', width = 250)
        self.contacts_treeview.column('phone_no', width = 150)
        self.contacts_treeview.column('email_id', width = 200)
        self.contacts_treeview.column('city', width = 150)
        self.contacts_treeview.grid(row = 2, column = 0, columnspan = 2, pady = 10)
        self.contacts_treeview.bind('<<TreeviewSelect>>', self.create_update_delete_contact_frame)

        self.cur.execute("select * from contact")
        self.fill_contacts_treeview()

    def fill_contacts_treeview(self):
        for contact in self.contacts_treeview.get_children():
            self.contacts_treeview.delete(contact)

        contacts = self.cur.fetchall()
        for contact in contacts:
            self.contacts_treeview.insert("", END, values = contact)

    def create_add_new_contact_frame(self):
        self.view_all_contacts_frame.destroy()

        self.add_new_contact_frame = Frame(self)
        self.add_new_contact_frame.place(relx = .5, rely = .5, anchor = CENTER)

        self.style.configure('TLabel', background = 'Aqua', font = (NONE,15))

        self.name_label = Label(self.add_new_contact_frame, text = "Name: ")
        self.name_label.grid(row = 0, column = 0, sticky = W)

        self.name_entry = Entry(self.add_new_contact_frame, font = (NONE, 15), width = 20)
        self.name_entry.grid(row = 0, column = 1, pady = 10)

        self.phone_no_label = Label(self.add_new_contact_frame, text = "Phone No: ")
        self.phone_no_label.grid(row = 1, column = 0, sticky = W)

        self.phone_no_entry = Entry(self.add_new_contact_frame, font = (NONE, 15), width = 20)
        self.phone_no_entry.grid(row = 1, column = 1, pady = 10)

        self.email_id_label = Label(self.add_new_contact_frame, text = "Email Id: ")
        self.email_id_label.grid(row = 2, column = 0, sticky = W)

        self.email_id_entry = Entry(self.add_new_contact_frame, font = (NONE, 15), width = 20)
        self.email_id_entry.grid(row = 2, column = 1, pady = 10)

        self.city_label = Label(self.add_new_contact_frame, text = "City: ")
        self.city_label.grid(row = 3, column = 0, sticky = W)

        self.city_combobox = Combobox(self.add_new_contact_frame, font = (NONE, 15), width = 20, values = ('Greater Noida', 'Noida', 'Delhi', 'Gurgaon', 'bangloure','Gorakhpur'))
        self.city_combobox.grid(row = 3, column = 1, pady = 10)
        self.city_combobox.current(5)

        self.profile_pic_label = Label(self.add_new_contact_frame, text = "Profile Pic: ")
        self.profile_pic_label.grid(row = 4, column = 0)

        self.profile_pic_button = Button(self.add_new_contact_frame,
        text = "Choose your profile pic", command = self.profile_pic_button_click)
        self.profile_pic_button.grid(row = 4, column = 1)

        self.style.configure('TButton', font = (NONE, 15), width = 20)

        self.add_button = Button(self.add_new_contact_frame, text = "Add",
        command = self.add_button_click)
        self.add_button.grid(row = 5, column = 1, pady = 10)

    def profile_pic_button_click(self):
        profile_pic = Image.open(filedialog.askopenfilename())
        self.profile_pic_path = "profile_pics/" + self.email_id_entry.get() + "." + profile_pic.format
        profile_pic.save(self.profile_pic_path)

    def add_button_click(self):
        self.cur.execute("select * from contact where emailid = ?", (self.email_id_entry.get(),))
        contact = self.cur.fetchone()
        if contact is None:
            self.cur.execute("""insert into contact values(?, ?, ?, ?, ?)
            """, (
                self.name_entry.get(),
                self.phone_no_entry.get(),
                self.email_id_entry.get(),
                self.city_combobox.get(),
                self.profile_pic_path
            ))
            self.con.commit()
            messagebox.showinfo('success message', 'contact details are added successfully')
            self.add_new_contact_frame.destroy()
            self.create_view_all_contacts_frame()
        else:
            messagebox.showerror('error message',
            'contact of ' + self.email_id_entry.get() + ' email id is already added')

    def create_update_delete_contact_frame(self, event):
        contact = self.contacts_treeview.item(self.contacts_treeview.selection())['values']

        self.view_all_contacts_frame.destroy()

        self.update_delete_contact_frame = Frame(self)
        self.update_delete_contact_frame.place(relx = .5, rely = .5, anchor = CENTER)

        self.style.configure('TLabel', background = 'Aqua', font = (NONE, 15))

        self.name_label = Label(self.update_delete_contact_frame, text = "Name: ")
        self.name_label.grid(row = 0, column = 0, sticky = W)

        self.name_entry = Entry(self.update_delete_contact_frame, font = (NONE, 15), width = 20)
        self.name_entry.grid(row = 0, column = 1, pady = 5)
        self.name_entry.insert(END, contact[0])

        self.phone_no_label = Label(self.update_delete_contact_frame, text = "Phone No: ")
        self.phone_no_label.grid(row = 1, column = 0, sticky = W)

        self.phone_no_entry = Entry(self.update_delete_contact_frame, font = (NONE, 15), width = 20)
        self.phone_no_entry.grid(row = 1, column = 1, pady = 5)
        self.phone_no_entry.insert(END, contact[1])

        self.email_id_label = Label(self.update_delete_contact_frame, text = "Email Id: ")
        self.email_id_label.grid(row = 2, column = 0, sticky = W)

        self.email_id_entry = Entry(self.update_delete_contact_frame, font = (NONE, 15), width = 20)
        self.email_id_entry.grid(row = 2, column = 1, pady = 5)
        self.email_id_entry.insert(END, contact[2])
        self.old_email_id = contact[2]

        self.city_label = Label(self.update_delete_contact_frame, text = "City: ")
        self.city_label.grid(row = 3, column = 0, sticky = W)

        self.city_combobox = Combobox(self.update_delete_contact_frame, font = (NONE, 15), width = 20, values = ('Greater Noida', 'Noida', 'Delhi', 'Gurgaon', 'bangloure','Gorakhpur'))
        self.city_combobox.grid(row = 3, column = 1, pady = 5)
        self.city_combobox.set(contact[3])

        self.profile_pic_label = Label(self.update_delete_contact_frame, text = "Profile: ")
        self.profile_pic_label.grid(row = 4, column = 0)
        try:

            self.update_delete_contact_frame.image = ImageTk.PhotoImage(Image.open(contact[4]))
            self.profile_pic = Label(self.update_delete_contact_frame,
            image = self.update_delete_contact_frame.image, text = "Here we will display image")
            self.profile_pic.grid(row = 4, column = 1)
        except Exception as e:
            print(e)
        finally :
               self.profile_pic_button = Button(self.update_delete_contact_frame,
               text = "Choose new profile pic", command = self.profile_pic_button_click)
               self.profile_pic_button.grid(row = 5, column = 1, pady = 5)

               self.style.configure('TButton', font = (NONE, 15), width = 20)

               self.update_button = Button(self.update_delete_contact_frame,
               text = "Update", command = self.update_button_click)
               self.update_button.grid(row = 6, column = 1, pady = 5)

               self.delete_button = Button(self.update_delete_contact_frame,
               text = "Delete", command = self.delete_button_click)
               self.delete_button.grid(row = 7, column = 1, pady = 5)

    def update_button_click(self):
        if self.profile_pic_path != "":
            self.cur.execute("""update contact set name = ?, phonenumber = ?, 
            emailid = ?, city = ?, profilepicpath = ? where emailid = ?
            """, (
                self.name_entry.get(),
                self.phone_no_entry.get(),
                self.email_id_entry.get(),
                self.city_combobox.get(),
                self.profile_pic_path,
                self.old_email_id
            ))
        else:
            self.cur.execute("""update contact set name = ?, phonenumber = ?, 
            emailid = ?, city = ? where emailid = ?
            """, (
                self.name_entry.get(),
                self.phone_no_entry.get(),
                self.email_id_entry.get(),
                self.city_combobox.get(),
                self.old_email_id
            ))
        self.con.commit()
        messagebox.showinfo("success message", "contact details are updated successfully")
        self.update_delete_contact_frame.destroy()
        self.create_view_all_contacts_frame()

    def delete_button_click(self):
        if messagebox.askquestion('confirmation message', 'are you sure to delete?') == 'yes':
            self.cur.execute("delete from contact where emailid = ?", (self.old_email_id,))
            self.con.commit()
            messagebox.showinfo('success message', 'contact details are deleted successfully')
        self.update_delete_contact_frame.destroy()
        self.create_view_all_contacts_frame()

    def name_entry_key_released(self, event):
        self.cur.execute("select * from contact where name like ?",("%"+ self.name_entry.get() +"%", ))
        self.fill_contacts_treeview()
