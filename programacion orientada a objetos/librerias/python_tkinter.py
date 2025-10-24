from tkinter import *
from tkinter import ttk

root = Tk()

frm = ttk.Frame(root, padding=10)
frm.grid()
ttk.Label(frm, text="Hello World!").grid(column=0, row=0)
ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)
ttk.Notebook(frm, height=100, width=100,padding=5).grid(column=0, row=1)
ttk.Radiobutton(frm, text="Soy un selector", value=5).grid(column=0, row=2)
ttk.Entry(frm)

root.mainloop()