from tkinter import *
from tkinter import messagebox
from random import choice, shuffle
import pyperclip
import json
from help_descriptions import Menubutton
import webbrowser
from accounts_window import AccountsWindow
from generator_window import LookUp

BACKGROUND = "#87CEFA"
BUTTONCOLOUR = "#DCDCDC"
LABELCOLOUR = "#ADD8E6"

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's',
           't', 'u',
           'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
           'O', 'P',
           'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


class MainWindow:
    """Creates the main window for the password generator program. It has the functions to save, generate and search."""

    def __init__(self):

        self.window = Tk()
        self.window.geometry("650x500")
        self.window.eval('tk::PlaceWindow . center')
        self.window.title("Password Manager")
        self.window.config(padx=20, pady=20, bg=BACKGROUND)
        self.window.iconbitmap("Otherpython.ico")

        self.canvas = Canvas(width=200, height=175, bg=BACKGROUND, highlightthickness=0)
        self.logo = PhotoImage(file="mylogo.png")
        self.canvas.create_image(100, 100, image=self.logo)
        self.canvas.grid(column=1, row=0)

        self.site_label = Label(text="Website name:", font=("Courier", 12, "normal"), bg=LABELCOLOUR)
        self.site_label.grid(column=0, row=1, sticky="EW")
        self.link_label = Label(text="Website link:", font=("Courier", 12, "normal"), bg=LABELCOLOUR)
        self.link_label.grid(column=0, row=2, sticky="EW")
        self.username_label = Label(text="Email/Username:", font=("Courier", 12, "normal"), bg=LABELCOLOUR)
        self.username_label.grid(column=0, row=3, sticky="EW")
        self.password_label = Label(text="Password:", font=("Courier", 12, "normal"), bg=LABELCOLOUR)
        self.password_label.grid(column=0, row=4, sticky="EW")

        self.site_field = Entry(width=35)
        self.site_field.grid(column=1, row=1, sticky="EW")
        self.site_field.focus()
        self.link_field = Entry(width=35)
        self.link_field.grid(column=1, row=2, sticky="EW")
        self.username_field = Entry(width=35)
        self.username_field.grid(column=1, row=3, sticky="EW")
        self.username_field.config(fg="grey")
        self.username_field.insert(0, "example@email.com")
        self.password_field = Entry(width=35)
        self.password_field.grid(column=1, row=4, sticky="EW")

        self.generate_button = Button(text="Generate Password", command=self.generate_password, bg=BUTTONCOLOUR)
        self.generate_button.grid(column=2, row=4, pady=5, padx=10)
        self.add_button = Button(text="Add", width=10, command=self.save, bg=BUTTONCOLOUR)
        self.add_button.grid(column=2, row=5)
        self.search_button = Button(text="Search", width=13, command=self.search_database, bg=BUTTONCOLOUR)
        self.search_button.grid(column=2, row=1)
        self.look_up_button = Button(text="Saved passwords", command=self.the_list, bg=BUTTONCOLOUR)
        self.look_up_button.grid(column=1, row=5, pady=5, padx=5)
        self.close_button = Button(text="Exit", command=self.close, bg=BUTTONCOLOUR)
        self.close_button.grid(column=2, row=0)
        self.manage_button = Button(text="Manage accounts", command=self.make_list, bg=BUTTONCOLOUR)
        self.manage_button.grid(column=1, row=6)
        self.letter_num = ""
        self.symbol_num = ""
        self.number_num = ""

        self.spin_label = Label(text="For your password:", font=("Courier", 12, "normal"))
        self.spin_label.grid(column=0, row=7, sticky="EW")
        self.letter_label = Label(text="Select the number of letters", font=("Courier", 12, "normal"), bg=LABELCOLOUR)
        self.letter_label.grid(column=0, row=8)
        self.letter_value = StringVar()
        self.letter_spin = Spinbox(from_=1.0, to=100.0, width=10, textvariable=self.letter_value, wrap=True)
        self.letter_spin.grid(column=1, row=8)

        self.symbol_value = StringVar()
        self.symbol_label = Label(text="Select the number of symbols", font=("Courier", 12, "normal"), bg=LABELCOLOUR)
        self.symbol_label.grid(column=0, row=9)
        self.symbol_spin = Spinbox(from_=1.0, to=100.0, textvariable=self.symbol_value, width=10, wrap=True)
        self.symbol_spin.grid(column=1, row=9)

        self.number_value = StringVar()
        self.number_label = Label(text="Select the number of numbers", font=("Courier", 12, "normal"), bg=LABELCOLOUR)
        self.number_label.grid(column=0, row=10)
        self.number_spin = Spinbox(from_=1.0, to=100.0, width=10, textvariable=self.number_value, wrap=True)
        self.number_spin.grid(column=1, row=10)

        # ---------------------------- Event tracking ------------------------------- #

        self.username_field.bind("<Button-1>", self.in_field)

        # ---------------------------- Menu ------------------------------- #

        self.menubutton = Menubutton(self.window)

        # ---------------------------- Event tracking ------------------------------- #

    def in_field(self, event):
        self.username_field.delete(0, END)
        self.username_field.config(fg="black")

    # ---------------------------- SAVE PASSWORD ------------------------------- #

    def save(self):
        """Saves the password in a json file. """
        website = self.site_field.get()
        username = self.username_field.get()
        password = self.password_field.get()
        link = self.link_field.get()
        new_data = {
            website: {
                "username": username,
                "password": password,
                "link": link,
            }
        }
        if len(website) == 0 or len(password) == 0:
            messagebox.showinfo(title="Oops", message="You left a field empty")
        else:
            is_ok = messagebox.askokcancel(title=website, message=f"This is what you entered for {website}: \nEmail \\ "
                                                                  f"Username: {username}\nPassword: {password}\nLink to"
                                                                  f"site: {link}\nIs this ok to save?")
            if is_ok:
                try:
                    with open("data.json", mode="r") as file:
                        # Read old data
                        data = json.load(file)
                except FileNotFoundError:
                    with open("data.json", mode="w") as file:
                        # Save data
                        json.dump(new_data, file, indent=4)
                else:
                    # Update data
                    data.update(new_data)

                    with open("data.json", mode="w") as file:
                        # Save data
                        json.dump(data, file, indent=4)

                finally:
                    pyperclip.copy(password)
                    self.site_field.delete(0, END)
                    self.password_field.delete(0, "end")
                    self.site_field.focus()
                    messagebox.showinfo(title="Yay", message="Information saved.")

    # ---------------------------- Search ------------------------------- #

    def search_database(self):
        """Search the json file for existing entries when search button is clicked. """
        match = self.site_field.get()
        website = match.capitalize()
        try:
            with open("data.json", mode="r") as file:
                # Read old data
                data = json.load(file)
        except FileNotFoundError:
            messagebox.showinfo(title="Sorry!", message="I found no data file.")
        else:
            if website in data:
                reply = messagebox.askyesno(title=website, message=f"Email \\ Username: {data[website]['username']}\n"
                                                                   f"Password: {data[website]['password']}\n\n"
                                                                   f"Would you like to go to this website?\nYour "
                                                                   f"password is copied ot the clipboard.")
                pyperclip.copy(data[website]['password'])
                if reply:
                    webbrowser.open(data[website]["link"])
                else:
                    pass
            elif website not in data:
                messagebox.showinfo(title="Sorry!", message=f"I found no data for {website}.")

    # ---------------------------- PASSWORD GENERATOR ------------------------------- #

    def generate_password(self):
        """Generates the password based on the given number of letters, symbols, and numbers needed in it. """
        letter_num = self.letter_spin.get()
        symbol_num = self.symbol_spin.get()
        number_num = self.number_spin.get()
        password_letter = [choice(letters) for _ in range(0, int(letter_num))]
        password_symbol = [choice(symbols) for _ in range(0, int(symbol_num))]
        password_number = [choice(numbers) for _ in range(0, int(number_num))]

        password_list = password_number + password_symbol + password_letter

        shuffle(password_list)
        password = "".join(password_list)
        self.password_field.insert(0, password)
        pyperclip.copy(password)

    # ---------------------------- Look up window ------------------------------- #

    def the_list(self):
        """Creates a window that diplay all the data in json"""
        window2 = LookUp()

    # ---------------------------- Manage Accounts Window ------------------------------- #

    def make_list(self):

        wacc = AccountsWindow()

    # ---------------------------- Close the program ------------------------------- #

    def close(self):
        self.window.destroy()


w = MainWindow()
w.window.mainloop()

