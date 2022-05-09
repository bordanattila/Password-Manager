import tkinter
from tkinter import *
from tkinter import messagebox
from random import choice, shuffle
import pyperclip
import json
from help_descriptions import Menubutton


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
        self.window.geometry("520x350")
        self.window.eval('tk::PlaceWindow . center')
        self.window.title("Password Manager")
        self.window.config(padx=20, pady=20, bg=BACKGROUND)
        self.window.iconbitmap("Otherpython.ico")

        self.canvas = Canvas(width=200, height=200, bg=BACKGROUND, highlightthickness=0)
        self.logo = PhotoImage(file="mylogo.png")
        self.canvas.create_image(100, 100, image=self.logo)
        self.canvas.grid(column=1, row=0)

        self.site_label = Label(text="Website:", font=("Courier", 12, "normal"), bg=LABELCOLOUR)
        self.site_label.grid(column=0, row=1, sticky="EW")
        self.username_label = Label(text="Email/Username:", font=("Courier", 12, "normal"), bg=LABELCOLOUR)
        self.username_label.grid(column=0, row=2, sticky="EW")
        self.password_label = Label(text="Password:", font=("Courier", 12, "normal"), bg=LABELCOLOUR)
        self.password_label.grid(column=0, row=3, sticky="EW")

        self.site_field = Entry(width=35)
        self.site_field.grid(column=1, row=1, sticky="EW")
        self.site_field.focus()
        self.username_field = Entry(width=35)
        self.username_field.grid(column=1, row=2, sticky="EW")
        self.username_field.config(fg="grey")
        self.username_field.insert(0, "example@email.com")
        self.password_field = Entry(width=35)
        self.password_field.grid(column=1, row=3, sticky="EW")

        self.generate_button = Button(text="Generate Password", command=self.create_spin_window, bg=BUTTONCOLOUR)
        self.generate_button.grid(column=2, row=3)
        self.add_button = Button(text="Add", width=10, command=self.save, bg=BUTTONCOLOUR)
        self.add_button.grid(column=1, row=4)
        self.search_button = Button(text="Search", width=13, command=self.search_database, bg=BUTTONCOLOUR)
        self.search_button.grid(column=2, row=1)
        self.look_up_button = Button(text="Saved passwords", command=self.the_list, bg=BUTTONCOLOUR)
        self.look_up_button.grid(column=2, row=4)
        self.letter_num = ""
        self.symbol_num = ""
        self.number_num = ""

        # ---------------------------- Event tracking ------------------------------- #

        self.username_field.bind("<Button-1>", self.in_field)

        # ---------------------------- Menu and main loop ------------------------------- #

        self.menubutton = Menubutton(self.window)
        self.window.mainloop()
        # ---------------------------- Event tracking ------------------------------- #

    def in_field(self, event):
        self.username_field.delete(0, END)
        self.username_field.config(fg="black")

    # ---------------------------- PASSWORD GENERATOR ------------------------------- #
    def generate_password(self, letter, symbol, number):
        """Generates the password based on the given number of letters, symbols, and numbers needed in it. """

        self.password_field.delete(0, "end")

        password_letter = [choice(letters) for _ in range(0, int(letter))]
        password_symbol = [choice(symbols) for _ in range(0, int(symbol))]
        password_number = [choice(numbers) for _ in range(0, int(number))]

        password_list = password_number + password_symbol + password_letter

        shuffle(password_list)
        password = "".join(password_list)
        self.password_field.insert(0, password)
        pyperclip.copy(password)

    # ---------------------------- SAVE PASSWORD ------------------------------- #

    def save(self):
        """Saves the password in a json file. """
        website = self.site_field.get()
        username = self.username_field.get()
        password = self.password_field.get()
        new_data = {
            website: {
                "username": username,
                "password": password,
            }
        }
        if len(website) == 0 or len(password) == 0:
            messagebox.showinfo(title="Oops", message="You left a field empty")
        else:
            is_ok = messagebox.askokcancel(title=website, message=f"This is what you entered for {website}: \nEmail \\ "
                                                                  f"Username: "f"{username}\nPassword: {password}\nIs "
                                                                  f"this ok to save?")
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
        website = self.site_field.get()

        try:
            with open("data.json", mode="r") as file:
                # Read old data
                data = json.load(file)
        except FileNotFoundError:
            messagebox.showinfo(title="Sorry!", message="I found no data file.")
        else:
            if website in data:
                messagebox.showinfo(title=website, message=f"Email \\ Username: {data[website]['username']}\nPassword: "
                                                           f"{data[website]['password']}")
            elif website not in data:
                messagebox.showinfo(title="Sorry!", message=f"I found no data for {website}.")

    # ---------------------------- Spinbox window ------------------------------- #

    def create_spin_window(self):
        """Creates a separate window with spin boxes to set parameters of the password. """
        self.spin = Tk()

        self.spin.title("For your password")
        self.spin.config(padx=20, pady=20, bg=BACKGROUND)
        self.spin.iconbitmap("Otherpython.ico")

        self.letter_label = Label(self.spin, text="Select the number of letters", font=("Courier", 12, "normal"),
                                  bg=LABELCOLOUR)
        self.letter_label.grid(column=0, row=0)
        self.letter_value = StringVar()
        self.letter_spin = tkinter.Spinbox(self.spin, from_=1.0, to=100.0, width=10, textvariable=self.letter_value,
                                           wrap=True)
        self.letter_spin.grid(column=1, row=0)

        self.symbol_value = StringVar()
        self.symbol_label = Label(self.spin, text="Select the number of symbols", font=("Courier", 12, "normal"),
                                  bg=LABELCOLOUR)
        self.symbol_label.grid(column=0, row=1)
        self.symbol_spin = tkinter.Spinbox(self.spin, from_=1.0, to=100.0, textvariable=self.symbol_value, width=10,
                                           wrap=True)
        self.symbol_spin.grid(column=1, row=1)

        self.number_value = StringVar()
        self.number_label = Label(self.spin, text="Select the number of numbers", font=("Courier", 12, "normal"),
                                  bg=LABELCOLOUR)
        self.number_label.grid(column=0, row=2)
        self.number_spin = tkinter.Spinbox(self.spin, from_=1.0, to=100.0, width=10, textvariable=self.number_value,
                                           wrap=True)
        self.number_spin.grid(column=1, row=2)

        self.gen_button = Button(self.spin, text="Generate", command=self.get_it)
        self.gen_button.grid(column=2, row=4)

    def get_it(self):
        letter_num = self.letter_spin.get()
        symbol_num = self.symbol_spin.get()
        number_num = self.number_spin.get()
        self.generate_password(letter_num, symbol_num, number_num)
        self.spin.destroy()

    # ---------------------------- Look up window ------------------------------- #
    def the_list(self):
        """Creates a window that diplay all the data in json"""
        self.the_list = Tk()

        self.the_list.title("Previously saved sites and passwords")
        self.the_list.config(padx=20, pady=20, bg=BACKGROUND)
        self.the_list.iconbitmap("Otherpython.ico")

        self.the_list_label = Label(self.the_list, text="Here is your list", font=("Courier", 12, "normal"),
                                    bg=LABELCOLOUR)
        self.the_list_label.grid(column=0, row=0)

        self.sb = Scrollbar(self.the_list)
        self.sb.grid(column=1, row=1, sticky=N+S+W)

        self.output = Text(self.the_list, width=50, height=10)

        self.output.config(yscrollcommand=self.sb.set)
        self.output.grid(column=0, row=1)
        self.sb.config(command=self.output.yview)

        self.output.tag_add("highlight_even", 1.0, 2.0)
        self.output.tag_configure("highlight_even", background="#B0E0E6")
        self.output.tag_configure("highlight_odd", background="white")

        with open("data.json", mode="r") as file:
            data = json.load(file)
        colour_tag = 0
        for k, v in data.items():
            site = k
            uname = v
            for u, p in uname.items():
                user = u
                pswd = p
                if colour_tag % 2 == 0:
                    self.output.insert(END, site + "  " + user + "  " + pswd + "\n", ("highlight_even"))
                else:
                    self.output.insert(END, site + "  " + user + "  " + pswd + "\n", ("highlight_odd"))
                colour_tag += 1
