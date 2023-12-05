from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfile


class guiElements:
    def __init__(self, guiUtilities, main):
        self.guiUtilities = guiUtilities
        self.main = main
        self.root = self.main.root
        self.createMenuBar()
        self.createLeftTree()

    def do_nothing(self):
        print("i do nothing")

    def onItemDoubleClickRootLeftTree(self, event):
        self.guiUtilities.onItemDoubleClick(event, self.root, self.leftTree, self.main.addRoom)

    def select(self):
        roomNumbersList = []
        for child in self.leftTree.selection():
            roomNumbersList.append(self.leftTree.item(child)["text"])
        self.main.triesToSelectRooms(roomNumbersList)

    def createMenuBar(self):
        self.menu_bar = Menu(self.root)
        self.root.config(menu=self.menu_bar)

        self.uploadMenu = Menu(self.menu_bar, tearoff=0)

        self.uploadMenu.add_command(label="Import Database", command=self.do_nothing)
        self.uploadMenu.add_command(label="Open", command=self.do_nothing)
        self.uploadMenu.add_command(label="Save", command=self.do_nothing)
        self.menu_bar.add_cascade(label="Upload", menu=self.uploadMenu)

        self.menu_bar.add_command(label="help", command=self.do_nothing)
        self.menu_bar.add_separator()

    def createLeftTree(self):
        self.leftTree = ttk.Treeview(master=self.root, columns=("knxName"))

        self.leftTree.column("#0", width=80, minwidth=80)
        self.leftTree.column("knxName", anchor=W, width=80, minwidth=80)

        self.leftTree.heading("#0", text="Name", anchor=W)
        self.leftTree.heading("knxName", text="Knx Name", anchor=W)

        for x in range(2001, 2008):
            self.leftTree.insert("", "end", text="A"+str(x), values=("Rom" + str(x),))
            self.main.addRoom("A"+str(x))

        self.leftTree.insert("", "end", text="", values=("",))

        self.leftTree.bind("<Double-1>", self.onItemDoubleClickRootLeftTree)
        self.leftTree.bind("<Return>", lambda e: self.select())

        self.leftTree.grid(row=1, column=1, sticky="nsew", columnspan=2, rowspan=4)

    def getRoomNumbers(self):
        roomNumbers = {}
        roomNumbersList = []
        for child in self.leftTree.get_children():
            roomNumbers[self.leftTree.item(child)["text"]] = self.leftTree.item(child)["values"][0]
            roomNumbersList.append(self.leftTree.item(child)["text"])
        roomNumbersList.pop()
        return roomNumbersList


