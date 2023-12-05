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

        self.boxDataTabsNames = {}

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
            deleted = False
            if (entry.get() == "" or entry.get().isspace()) and tree.get_children()[-1] != item:
                tree.delete(item)
                self.main.boxDataTabs[item].unlink()
                self.main.boxDataTabs[item].frame.destroy()
                self.main.boxDataTabs.pop(item)
                if item in self.boxDataTabsNames:
                    self.boxDataTabsNames.pop(item)
                deleted = True

            if entry.get() in self.boxDataTabsNames.values():
                self.main.log("This name already exists!")
                return

            if column == '#0' and not deleted:
                tree.item(item, text=entry.get())

            elif not deleted:
                tree.set(item, column=column, value=entry.get())

            if tree.get_children()[-1] == row and not (entry.get() == "" or entry.get().isspace()):
                self.createNewBoxDataTab(tree, item, entry.get())

            entry.destroy()

        entry.bind("<Return>", save_edit)
        entry.bind("<FocusOut>", lambda e: entry.destroy())
        entry.focus()

    def createNewBoxDataTab(self, tree, item, name, addName=False):
        if addName:
            tree.insert("", "end", text=name)
            tree.insert("", "end", text="")
        else:
            tree.insert("", "end", text="", values=("",))
        tree.yview_moveto(1.0)

        self.boxDataTabsNames[item] = name

        newTabBoxData = ttk.Frame(self.tabControlBoxData)
        self.tabControlBoxData.add(newTabBoxData, text=name)

        newTabBoxData.rowconfigure(1, weight=0)
        newTabBoxData.rowconfigure(2, weight=0)
        newTabBoxData.rowconfigure(3, weight=0)
        newTabBoxData.rowconfigure(4, weight=0)
        newTabBoxData.rowconfigure(5, weight=0)
        newTabBoxData.rowconfigure(6, weight=0)
        newTabBoxData.rowconfigure(7, weight=0)
        newTabBoxData.rowconfigure(8, weight=0)
        newTabBoxData.rowconfigure(9, weight=0, minsize=10)
        newTabBoxData.rowconfigure(10, weight=0)
        newTabBoxData.rowconfigure(11, weight=0)
        newTabBoxData.rowconfigure(12, weight=0)
        newTabBoxData.rowconfigure(13, weight=0)
        newTabBoxData.rowconfigure(14, weight=0)
        newTabBoxData.rowconfigure(15, weight=0)
        newTabBoxData.rowconfigure(16, weight=0)
        newTabBoxData.rowconfigure(17, weight=0)
        newTabBoxData.rowconfigure(18, weight=0)
        newTabBoxData.rowconfigure(19, weight=0)
        newTabBoxData.rowconfigure(20, weight=0)
        newTabBoxData.rowconfigure(21, weight=0)
        newTabBoxData.rowconfigure(22, weight=1)

        newTabBoxData.columnconfigure(1, weight=1)
        newTabBoxData.columnconfigure(2, weight=1)
        newTabBoxData.columnconfigure(3, weight=8)

        self.main.createNewBoxDataTab(newTabBoxData, item, name)

    def onItemDoubleClickTabInfoCreated(self, event):
        self.onItemDoubleClick(event, self.tabStructureTreeBoxTypes, self.tabStructureTreeBoxTypes)

    def createTabStructure(self):
        self.tabStructureTreeBoxTypes = ttk.Treeview(master=self.tabStructure)
        self.tabStructureTreeBoxTypes.column("#0", width=100, minwidth=150)
        self.tabStructureTreeBoxTypes.heading("#0", text="Box Types", anchor=W)

        self.tabStructureTreeBoxTypes.bind("<Double-1>", self.onItemDoubleClickTabInfoCreated)
        self.tabStructureTreeBoxTypes.grid(row=1, column=1, sticky="nsew")

        self.tabControlBoxData = ttk.Notebook(self.tabStructure)


        self.tabControlBoxData.grid(column=2, row=1, sticky="nsew")

        self.tabStructure.rowconfigure(1, weight=1)
        self.tabStructure.columnconfigure(1, weight=1)
        self.tabStructure.columnconfigure(2, weight=5)

        self.createNewBoxDataTab(self.tabStructureTreeBoxTypes, "I001", "default", True)


