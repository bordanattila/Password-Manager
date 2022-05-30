from tkinter import *
from tkinter import messagebox
import json
from help_descriptions import Menubutton

BACKGROUND = "#87CEFA"
BUTTONCOLOUR = "#DCDCDC"
LABELCOLOUR = "#ADD8E6"
match = ""


class AccountsWindow:
    """Creates the main window for the password generator program. It has the functions to save, generate and search."""

    def __init__(self):

        self.accounts = Toplevel()

        self.accounts.title("Manage Accounts")
        self.accounts.config(padx=20, pady=20, bg=BACKGROUND)
        self.accounts.iconbitmap("Otherpython.ico")
        self.new_password_field = Entry(self.accounts, width=35)
        self.new_password_field.grid(column=2, row=3, sticky="EW", padx=10)

        self.listbox = Listbox(self.accounts, height=10)
        self.account_list = []
        self.load_content()

        self.scroll = Scrollbar(self.accounts, orient="vertical")
        self.listbox.config(yscrollcommand=self.scroll.set)
        self.scroll.grid(column=1, row=0, rowspan=10, sticky=N + S + W)
        self.scroll.config(command=self.listbox.yview)
        self.listbox.bind("<<ListboxSelect>>", self.selected_account)

        self.delete_button = Button(self.accounts, text="Delete Account", command=lambda: self.delete_account(match),
                                    bg=BUTTONCOLOUR)
        self.delete_button.grid(column=2, row=1)
        self.change_button = Button(self.accounts, text="Change Password", command=lambda: self.change_password(match),
                                    bg=BUTTONCOLOUR)
        self.change_button.grid(column=2, row=2)
        self.to_exit_button = Button(self.accounts, text="Exit", command=self.to_exit, width=13, bg=BUTTONCOLOUR)
        self.to_exit_button.grid(column=2, row=4)

        # ---------------------------- Menu ------------------------------- #

        self.menubutton = Menubutton(self.accounts)

        # ---------------------------- Select Account ------------------------------- #

    def selected_account(self, *args):
        global match
        account_index = self.listbox.curselection()
        user_select = account_index[0]
        match = self.account_list[user_select]

        # ---------------------------- Delete Account ------------------------------- #

    def delete_account(self, m):
        with open("data.json", mode="r") as f:
            data = json.load(f)
            del data[m]
            with open("data.json", mode="w") as file:
                json.dump(data, file, indent=4)
        self.load_content()

        # ---------------------------- Change Password ------------------------------- #

    def change_password(self, m):

        with open("data.json", mode="r") as c:
            data = json.load(c)
            website = m
            username = data[m]["username"]
            password = self.new_password_field.get()
            link = data[m]["link"]
            new_data = {
                website: {
                    "username": username,
                    "password": password,
                    "link": link,
                }
            }
            data.update(new_data)
            with open("data.json", mode="w") as file:
                json.dump(data, file, indent=4)

        # ---------------------------- Exit------------------------------- #

    def to_exit(self):
        self.accounts.destroy()

        # ---------------------------- Create Listbox Content ------------------------------- #

    def load_content(self):
        try:
            with open("data.json", mode="r") as file:
                data = json.load(file)
        except FileNotFoundError:
            messagebox.showinfo(title="Sorry!", message="I found no data file.")
        else:
            self.account_list = []
            for s in data.keys():
                self.account_list.append(s)
            string_list = ",".join(self.account_list).split(",")
            acc_names = StringVar(value=string_list)
        self.listbox = Listbox(self.accounts, listvariable=acc_names, height=10)
        self.listbox.grid(column=0, row=0, rowspan=6)
        for i in range(0, len(self.account_list), 2):
            self.listbox.itemconfigure(i, background="#66CDAA")
