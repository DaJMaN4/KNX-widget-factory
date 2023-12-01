from tkinter import *
from tkinter import ttk
from tkinter.font import Font
from tkinter.filedialog import askopenfile


class guiTabStructure:
    def __init__(self, main, root, tabStructure, guiUtilities):
        self.main = main
        self.root = root
        self.tabStructure = tabStructure
        self.guiUtilities = guiUtilities
        self.createTabStructure()

    def onItemDoubleClick(self, event, frame, tree):
        item = tree.focus()
        column = tree.identify_column(event.x)
        row = tree.identify_row(event.y)
        if row is None or row == "":
            return
        x, y, width, height = tree.bbox(item, column)
        entry = Entry(frame)
        entry.place(x=x, y=y + tree.winfo_y(), width=width, height=height)

        def save_edit(event):
            if (entry.get() == "" or entry.get().isspace()) and tree.get_children()[-1] != item:
                tree.delete(item)
                self.main.boxDataTabs[item].unlink()
                self.main.boxDataTabs[item].frame.destroy()
                self.main.boxDataTabs.pop(item)

            elif column == '#0':
                tree.item(item, text=entry.get())

            else:
                tree.set(item, column=column, value=entry.get())

            if tree.get_children()[-1] == row and not (entry.get() == "" or entry.get().isspace()):
                tree.insert("", "end", text="", values=("",))
                tree.yview_moveto(1.0)

                print("new tab created")

                newTabBoxData = ttk.Frame(self.tabControlBoxData)

                self.tabControlBoxData.add(newTabBoxData, text=entry.get())

                newTabBoxData.rowconfigure(1, weight=1)
                newTabBoxData.columnconfigure(1, weight=1)
                newTabBoxData.columnconfigure(2, weight=1)
                newTabBoxData.columnconfigure(3, weight=8)

                self.createBoxDataDefault(newTabBoxData, item, entry.get())

            entry.destroy()

        entry.bind("<Return>", save_edit)
        entry.bind("<FocusOut>", lambda e: entry.destroy())
        entry.focus()

    def onItemDoubleClickTabInfoCreated(self, event):
        self.onItemDoubleClick(event, self.tabStructureTreeBoxTypes, self.tabStructureTreeBoxTypes)

    def createTabStructure(self):
        self.tabStructureTreeBoxTypes = ttk.Treeview(master=self.tabStructure)
        self.tabStructureTreeBoxTypes.column("#0", width=100, minwidth=150, stretch=NO)
        self.tabStructureTreeBoxTypes.heading("#0", text="Box Types", anchor=W)

        self.tabStructureTreeBoxTypes.insert("", "end", text="")

        self.tabStructureTreeBoxTypes.bind("<Double-1>", self.onItemDoubleClickTabInfoCreated)
        self.tabStructureTreeBoxTypes.grid(row=1, column=1, sticky="nsew")

        self.tabControlBoxData = ttk.Notebook(self.tabStructure)

        self.tabBoxDataTest = ttk.Frame(self.tabControlBoxData)

        self.tabControlBoxData.add(self.tabBoxDataTest, text='info')
        self.tabControlBoxData.grid(column=2, row=1, sticky="nsew")

        self.tabBoxDataTest.rowconfigure(1, weight=1)
        self.tabBoxDataTest.columnconfigure(1, weight=1)
        self.tabBoxDataTest.columnconfigure(2, weight=1)
        self.tabBoxDataTest.columnconfigure(3, weight=8)
        self.tabStructure.rowconfigure(1, weight=1)
        self.tabStructure.columnconfigure(1, weight=1)
        self.tabStructure.columnconfigure(2, weight=5)

        self.createBoxDataDefault(self.tabBoxDataTest, "info ID", "info")

    def createBoxDataDefault(self, frame, item, name):
        self.main.createNewBoxDataTab(frame, item, name)
