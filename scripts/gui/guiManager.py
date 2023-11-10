import tkinter as tk
from tkinter.filedialog import askopenfile
from tkinter import filedialog

from time import sleep

window = tk.Tk()
window.columnconfigure([0, 1], weight=1, minsize=250)
window.rowconfigure([0, 1], weight=1, minsize=100)
window.geometry("500x500")
window.title('Config')


def importDatabase():
    file = askopenfile(mode='r', filetypes=[('Python Files', '*.zip')])
    if file is not None:
        content = file.read()
        print(content)





frame = tk.Frame(master=window, relief=tk.RAISED, borderwidth=1)

frame.grid(row=0, column=0, padx=5, pady=5)
label1 = tk.Label(master=frame, text="A")
label1.pack(padx=5, pady=5)

frame = tk.Frame(master=window, relief=tk.RAISED, borderwidth=1)

frame.grid(row=1, column=1, padx=5, pady=5)
label2 = tk.Label(master=frame, text="B")
label2.pack(padx=5, pady=5)

frame = tk.Frame(master=window, relief=tk.RAISED, borderwidth=1)
frame.grid(row=1, column=0, padx=5, pady=5)
button = tk.Button(master=frame, text ='import database', command = lambda:open_file())
button.pack()

window.mainloop()
