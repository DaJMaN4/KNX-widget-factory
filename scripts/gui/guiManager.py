from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfile


root = Tk()
root.columnconfigure(1, weight=1)
root.rowconfigure(1, weight=1)
root.columnconfigure(2, weight=1)
root.rowconfigure(2, weight=1)
root.columnconfigure(3, weight=1)
root.rowconfigure(3, weight=1)
root.columnconfigure(4, weight=1)
root.rowconfigure(4, weight=1)
root.geometry("500x500")
root.title('Config')


# TODO Add button to import database

# TODO Add button to import level

# TODO Add button to import framework

# TODO Add button to import widgets

# TODO Add listbox to show imported files


# TODO treeview


def importDatabase():
    file = askopenfile(mode='r', filetypes=[('Python Files', '*.zip')])
    if file is not None:
        content = file.read()
        print(content)


def do_nothing():
    print("ok")


menu_bar = Menu(root)
root.config(menu=menu_bar)

file_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_command(label="Frameworks", command=do_nothing)
menu_bar.add_separator()
menu_bar.add_command(label="Widgets", command=do_nothing)
menu_bar.add_separator()
menu_bar.add_command(label="Levels", command=do_nothing)

frame = Frame(master=root, borderwidth=1)

edit_entry = Entry(frame)

def edit_item(event):
    # Get the index of the item to edit
    index = listbox.curselection()[0]
    selected_text = listbox.get(index)

    # Set the text in the entry and select it for editing
    edit_entry.delete(0, END)
    edit_entry.insert(0, selected_text)
    edit_entry.focus()

    def save_edit(event):
        listbox.delete(index)
        listbox.insert(index, edit_entry.get())
        edit_entry.delete(0, END)

    # Bind the Enter key to save the edited item
    edit_entry.bind("<Return>", save_edit)


def on_item_double_click(event):
    item = tree.focus()
    column = tree.identify_column(event.x)
    row = tree.identify_row(event.y)
    row += "l"
    if row[0] != "I":
        return
    x, y, width, height = tree.bbox(item, column)
    entry = Entry(frame)
    entry.place(x=x, y=y + tree.winfo_y(), width=width, height=height)

    def save_edit(event):
        if column == '#0':
            tree.item(item, text=entry.get())
        else:
            tree.set(item, column=column, value=entry.get())
        entry.destroy()

    entry.bind("<Return>", save_edit)
    entry.bind("<FocusOut>", lambda e: entry.destroy())
    entry.focus()


tree = ttk.Treeview(master=frame, columns=("knxName"))

tree.column("#0", width=80, minwidth=80)
tree.column("knxName", anchor=W, width=80, minwidth=80)

tree.heading("#0", text="Name", anchor=W)
tree.heading("knxName", text="Knx Name", anchor=W)

tree.insert("", "end", text="60", values=("Item 1",))
tree.insert("", "end", text="26", values=("Item 68",))

for x in range(0, 30):
    tree.insert("", "end", text=str(x), values=("Item " + str(x),))

tree.insert("", "end", text="", values=("",))

tree.bind("<Double-1>", on_item_double_click)

frame.grid_rowconfigure(1, weight=1)
frame.grid_rowconfigure(2, weight=1)

tree.grid(row=1, column=1, sticky="nsew", columnspan=2, rowspan=4)

# button = Button(master=frame, text='new')
# button.grid(row=2, column=2, sticky="se")

frame.grid(column=1, row=1, sticky="nsew")


button = Button(text='import database', command=lambda: importDatabase())
button.grid(row=1, column=3, sticky="n")


def add_item():
    item = entry.get()
    if item:
        listbox.insert(END, item)
        entry.delete(0, END)  # Clear the entry widget


frame2 = Frame(root)
frame2.grid(row=1, column=3, sticky="nsew")

scrollbar = Scrollbar(frame2, orient=VERTICAL)

listbox = Listbox(frame2, yscrollcommand=scrollbar.set)
scrollbar.config(command=listbox.yview)

listbox.grid(row=0, column=0, sticky="nsew")
scrollbar.grid(row=0, column=1, sticky="ns")

listbox.bind("<Double-1>", edit_item)

entry = Entry(frame2)
entry.grid(row=1, column=0, sticky="n")


add_button = Button(frame2, text="insert", command=add_item)
add_button.grid(row=1, column=0, sticky="ne")


radioBox = ttk.Radiobutton(root, text="One")
radioBox.grid(row=1, column=4, sticky="n")


root.mainloop()




# separator = ttk.Separator(frame,orient=HORIZONTAL)
# separator.pack(expand = True, fill=X)
