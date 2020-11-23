from tkinter import *

#Form Routines
root = Tk()

lstServices = Listbox(root)
lstServices.grid(row=0, column=0)

lblUsername = Label(root, text="Username: ")
lblUsername.grid(row=0, column=1)


#General Routines


def init_form():
    root.mainloop()