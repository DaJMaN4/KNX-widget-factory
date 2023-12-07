from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfile
from tkinter.font import Font


class guiUtilities:
    def __init__(self, root):
        self.root = root

    """
    Creates a new tab in the notebook
    
    """
    def onItemDoubleClick(self, event, frame, tree, function=None):
        item = tree.focus()
        column = tree.identify_column(event.x)
        row = tree.identify_row(event.y)
        if row is None or row == "":
            return
        x, y, width, height = tree.bbox(item, column)
        entry_text = StringVar()
        # get text from tree from item

        entry_text.set(tree.item(item)["text"])
        entry = Entry(frame, textvariable=entry_text)
        entry.icursor(END)
        entry.place(x=x, y=y + tree.winfo_y(), width=width, height=height)

        def save_edit(event):
            if (entry.get() == "" or entry.get().isspace()) and tree.get_children()[-1] != item:
                tree.delete(item)

            elif column == '#0':
                tree.item(item, text=entry.get())

            else:
                tree.set(item, column=column, value=entry.get())

            if tree.get_children()[-1] == row and not (entry.get() == "" or entry.get().isspace()):
                tree.insert("", "end", text="", values=("",))
                tree.yview_moveto(1.0)

            if function is not None:
                function(entry.get())

            entry.destroy()

        entry.bind("<Return>", save_edit)
        entry.bind("<FocusOut>", lambda e: entry.destroy())
        entry.focus()
