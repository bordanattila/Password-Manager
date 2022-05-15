from tkinter import *
import json
BACKGROUND = "#87CEFA"
LABELCOLOUR = "#ADD8E6"
BUTTONCOLOUR = "#DCDCDC"


class LookUp:

    def __init__(self):
        self.the_list = Tk()
        self.the_list.geometry("500x400")
        self.the_list.title("Previously saved sites and passwords")
        self.the_list.config(padx=20, pady=20, bg=BACKGROUND)
        self.the_list.iconbitmap("Otherpython.ico")

        self.the_list_label = Label(self.the_list, text="Here is your list", font=("Courier", 12, "normal"),
                                    bg=LABELCOLOUR)
        self.the_list_label.grid(column=0, row=0)

        self.sb = Scrollbar(self.the_list, orient="vertical")
        self.sb.grid(column=1, row=1, sticky=N+S+W)

        self.output = Text(self.the_list, width=50, height=20)

        self.output.config(yscrollcommand=self.sb.set)
        self.output.grid(column=0, row=1)
        self.sb.config(command=self.output.yview)

        self.output.tag_add("highlight_even", 1.0, 2.0)
        self.output.tag_configure("highlight_even", background="#B0E0E6")
        self.output.tag_configure("highlight_odd", background="white")

        self.to_close = Button(self.the_list, text="Exit", command=self.to_exit, width=13, bg=BUTTONCOLOUR)
        self.to_close.grid(column=0, row=2, pady=10, padx=10)

        try:
            with open("data.json", mode="r") as file:
                data = json.load(file)
            colour_tag = 0
        except FileNotFoundError:
            pass
        else:
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

    def to_exit(self):
        self.the_list.destroy()
