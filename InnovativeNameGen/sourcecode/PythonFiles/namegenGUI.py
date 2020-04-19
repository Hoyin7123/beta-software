import random
import datetime
import time
import asyncio
from tkinter import *
from tkinter import messagebox

"""
Name generator
By --- HYWong
"""


class Namegen:
    current_amount = 0
    results = []

    def __init__(self, amount):
        self.amount = amount

    def gen_eng(self):
        while self.current_amount < self.amount:
            name_list = open("src/eng/name.txt").read().splitlines()
            name = random.choice(name_list)
            surname_list = open("src/eng/surname.txt").read().splitlines()
            surname = random.choice(surname_list)
            fullname = name + " " + surname
            self.results.append(fullname)
            self.current_amount += 1

    def gen_chi(self):
        while self.current_amount < self.amount:
            name_list_1 = open("src/chi/name1.txt").read().splitlines()
            name1 = random.choice(name_list_1)
            name_list_2 = open("src/chi/name2.txt").read().splitlines()
            name2 = random.choice(name_list_2)
            surname_list = open("src/chi/surname.txt").read().splitlines()
            surname = random.choice(surname_list)

            y = random.randint(1, 100)
            if y < 97:
                fullname = surname + name1 + name2
            else:
                combined_name_list = name_list_1 + name_list_2
                single_name = random.choice(combined_name_list)
                fullname = surname + single_name
            self.results.append(fullname)
            self.current_amount += 1

    def gen_comb(self):
        while self.current_amount < self.amount:
            name_list_1 = open("src/combined/name1.txt").read().splitlines()
            unsplitname1 = random.choice(name_list_1)
            name1_chi, name1_eng = unsplitname1.split(":")
            name_list_2 = open("src/combined/name2.txt").read().splitlines()
            unsplitname2 = random.choice(name_list_2)
            name2_chi, name2_eng = unsplitname2.split(":")
            surname_list = open("src/combined/surname.txt").read().splitlines()
            unsplitsurname = random.choice(surname_list)
            surname_chi, surname_eng = unsplitsurname.split(":")
            combined_name_list = name_list_1 + name_list_2
            unsplitname = random.choice(combined_name_list)
            single_name_chi, single_name_eng = unsplitname.split(":")

            y = random.randint(1, 100)
            if y < 97:
                fullname = surname_chi + name1_chi + name2_chi + " " + surname_eng + " " + name1_eng + " " + name2_eng
            else:
                fullname = surname_chi + single_name_chi + " " + surname_eng + " " + single_name_eng
            self.results.append(fullname)
            self.current_amount += 1

    def gen_eng_mixed(self):
        while self.current_amount < self.amount:
            name_list_1 = open("src/combined/name1.txt").read().splitlines()
            unsplitname1 = random.choice(name_list_1)
            splitname1 = unsplitname1.split(":")
            name1_eng = splitname1[1]
            name_list_2 = open("src/combined/name2.txt").read().splitlines()
            unsplitname2 = random.choice(name_list_2)
            splitname2 = unsplitname2.split(":")
            name2_eng = splitname2[1]
            surname_list = open("src/combined/surname.txt").read().splitlines()
            unsplitsurname = random.choice(surname_list)
            splitsurname = unsplitsurname.split(":")
            surname_eng = splitsurname[1]
            combined_name_list = name_list_1 + name_list_2
            unsplitname = random.choice(combined_name_list)
            splitsinglename = unsplitname.split(":")
            single_eng = splitsinglename[1]
            eng_name = random.choice(open("src/eng/name.txt").read().splitlines())
            surname = random.choice(open("src/eng/surname.txt").read().splitlines())
            y = random.randint(1, 100)
            if y < 60:
                fullname = eng_name + " " + surname
            elif y < 97:
                fullname = surname_eng + " " + name1_eng + " " + name2_eng
            else:
                fullname = surname_eng + " " + single_eng
            self.results.append(fullname)
            self.current_amount += 1

    def save(self):
        filename = datetime.datetime.now().strftime("%d-%m-%Y_%H:%M:%S")
        with open(f"results/{filename}.txt", "w") as result:
            result.write("\n".join(self.results))


def generate(number, mode):
    if number < 1:
        messagebox.showerror("Error", "Please input an amount of at least 1.")
    else:
        obj = Namegen(number)
        obj.results = []
        if mode == 1:
            obj.gen_eng()
        elif mode == 2:
            obj.gen_chi()
        elif mode == 3:
            obj.gen_comb()
        elif mode == 4:
            obj.gen_eng_mixed()

        results = Toplevel()
        results.title("Results")
        for item in obj.results:
            Label(results, text=item).pack()
        savebutton = Button(results, text="Save results", command=lambda: save(obj.results))
        savebutton.pack()


def save(results):
    filename = datetime.datetime.now().strftime("%d-%m-%Y|%H:%M:%S")
    with open(f"results/{filename}.txt", "w") as result:
        result.write("\n".join(results))
    messagebox.showinfo("Success!", "Results successfully saved!")


# Tkinter
root = Tk()
root.title("Innovative Name Generator (Beta)")
root.tk.call("tk", "scaling", 1.0)

amount = Entry(root, width=7, borderwidth=3)
amount.grid(row=0, column=0)

modetitle = Label(root, text="Please choose the mode.")
modetitle.grid(row=1, column=0)

r = IntVar()
r.set(1)
modes = ["English", "Chinese", "Chinese with translated English", "Combined"]

option1 = Radiobutton(root, text=modes[0], variable=r, value=1, command=lambda: choosemode(1))
option2 = Radiobutton(root, text=modes[1], variable=r, value=2, command=lambda: choosemode(2))
option3 = Radiobutton(root, text=modes[2], variable=r, value=3, command=lambda: choosemode(3))
option4 = Radiobutton(root, text=modes[3], variable=r, value=4, command=lambda: choosemode(4))
option1.grid(row=2, column=0, sticky=W)
option2.grid(row=3, column=0, sticky=W)
option3.grid(row=4, column=0, sticky=W)
option4.grid(row=5, column=0, sticky=W)

mode = 1
def choosemode(x):
    global mode
    mode = x


start = Button(root, text="START", width=5, height=1, command=lambda: generate(int(amount.get()), mode))
start.grid(row=7, column=0)

mainloop()
