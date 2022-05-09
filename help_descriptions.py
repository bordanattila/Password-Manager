from tkinter import messagebox
from tkinter import *


class Menubutton:
    # ---------------------------- Submenus ------------------------------- #
    def __init__(self, menubar):

        menubar.option_add('*tearOff', FALSE)
        self.menu_bar = Menu(menubar)
        menubar['menu'] = self.menu_bar

        self.menu_file = Menu(self.menu_bar)
        self.menu_bar.add_cascade(menu=self.menu_file, label='Help')
        self.menu_file.add_command(label='About the program', command=self.about_the_program)
        self.menu_file.add_command(label='Generate Password', command=self.gen_password__button)
        self.menu_file.add_command(label='Add', command=self.add_btn)
        self.menu_file.add_command(label='Search', command=self.search_btn)
        self.menu_file.add_command(label='Saved Passwords', command=self.saved_btn)

    def about_the_program(self):
        messagebox.showinfo(title="About the program",
                            message="This program can store your passwords for all websites. "
                                    "You don't have to use the same password over and over "
                                    "again. Each time you sign up to a new website you can save "
                                    "a unique password for it and retrieve it later. The "
                                    "program also can help you generate secure passwords and "
                                    "avoid avoid the ones like '1234' or 'password1'.")

    def gen_password__button(self):
        messagebox.showinfo(title="Generate Password button",
                            message="The Generate Password button creates a secure password for "
                                    "you using upper and lowercase letters, numbers, and "
                                    "symbols. the generated password is automatically added to "
                                    "your clipboard and ready for you to paste it.")

    def add_btn(self):
        messagebox.showinfo(title="Add button",
                            message="Using the add button you can add the information (website, "
                                    "username, password) to a data.text file that is stored on "
                                    "your computer. If you typed in your own password is it "
                                    "added to your clipboard once you hit the 'Add' button. ")

    def search_btn(self):
        messagebox.showinfo(title="Search button",
                            message="Using the search button you can search for saved websites. The program will "
                                    "display the username and password created for previously saved website. ")
    def saved_btn(self):
        messagebox.showinfo(title="Saved passwords button",
                            message="A new window pops up to display a list of all the sites that are saved with the"
                                    "corresponding credentials.")
