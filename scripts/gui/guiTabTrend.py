from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfile
from tkinter.font import Font


class guiTabTrend:
    def __init__(self, main, root, tabTrend, guiUtilities):
        self.main = main
        self.root = root
        self.tabTrend = tabTrend
        self.guiUtilities = guiUtilities

        self.name = ""

        self.createTabTrend()

    def onItemDoubleClickTreeCreated(self, event):
        self.guiUtilities.onItemDoubleClick(event, self.tabTrend, self.tabTrendTreeCreatedWidgets)

    def onItemDoubleClickTabObjects(self, event):
        self.guiUtilities.onItemDoubleClick(event, self.tabTrendTreeObjectsNames, self.tabTrendTreeObjectsNames)

    def createTabTrend(self):
        self.tabTrendTreeCreatedWidgets = ttk.Treeview(master=self.tabTrend)
        self.tabTrendTreeCreatedWidgets.column("#0", width=100, minwidth=150)
        self.tabTrendTreeCreatedWidgets.heading("#0", text="Created Widgets", anchor=W)

        self.tabTrendTreeCreatedWidgets.bind("<Double-1>", self.onItemDoubleClickTreeCreated)
        self.tabTrendTreeCreatedWidgets.grid(row=1, column=1, sticky="nsew", rowspan=20)

        self.tabTrendTreeObjectsNames = ttk.Treeview(master=self.tabTrend)
        self.tabTrendTreeObjectsNames.column("#0", width=300, minwidth=150)
        self.tabTrendTreeObjectsNames.heading("#0", text="Object Names", anchor=W)

        self.tabTrendTreeObjectsNames.insert("", "end", text="Romtemperatur - Verdi")
        self.tabTrendTreeObjectsNames.insert("", "end", text="Romtemperatur - Aktivt settpunkt")
        self.tabTrendTreeObjectsNames.insert("", "end", text="CO2 i rom - Verdi")
        self.tabTrendTreeObjectsNames.insert("", "end", text="Tilstedesensor -")

        self.tabTrendTreeObjectsNames.insert("", "end", text="")

        self.tabTrendTreeObjectsNames.bind("<Double-1>", self.onItemDoubleClickTabObjects)

        self.tabTrendTreeObjectsNames.grid(row=1, column=2, sticky="nsew", rowspan=20)

        title_font = Font(family="Helvetica", size=15, weight="bold")
        label = Label(self.tabTrend, text="Trend Widgets", font=title_font)
        label.grid(row=1, column=3, sticky="n")

        self.tabTextTrend = Label(self.tabTrend,
                                  text="To create Trend Widgets, specify on the most left column named 'Name' numbers of rooms. "
                                       "If in KNX file identifier of this room is diffrent then just room name specify the knx name of the widget in column "
                                       "'Knx Name'. Remember that column 'Name' is used to find category of trend logs in LM database."
                                       " Use %roomname% as placeholder for setting name of room in files on LM. ")
        self.tabTextTrend.grid(row=2, column=3, sticky="new")

        def on_entry_change(*args):
            value = entry_text.get()
            roomName = self.main.guiElements.getRoomNumbers()[0]
            if self.addPrefixTrend.get() == 1:
                num = 0
                for c in roomName:
                    if not c.isdigit():
                        # Delete character from string at index num
                        roomName = roomName[:num] + roomName[num + 1:]
                    else:
                        break
                    num = num + 1
            self.name = value
            value = value.replace("%name%", roomName)
            self.labelPreviewTrend.config(text="Preview: " + value)

        self.labelPreviewTrend = Label(self.tabTrend, text="Preview: ")
        self.labelPreviewTrend.grid(row=3, column=3, sticky="n")

        entry_text = StringVar()
        entry_text.trace_add("write", on_entry_change)

        entry = Entry(master=self.tabTrend, textvariable=entry_text, width=30)
        entry.grid(row=4, column=3)

        self.addPrefixTrend = IntVar()

        radioBox = ttk.Checkbutton(self.tabTrend, text="Do not add prefix to widget name", variable=self.addPrefixTrend, command=on_entry_change)
        radioBox.grid(row=5, column=3)

        self.tabTrend.grid_columnconfigure(3, weight=1, minsize=30)
        self.tabTrend.grid_rowconfigure(1, weight=0)
        self.tabTrend.grid_rowconfigure(2, weight=0)
        self.tabTrend.grid_rowconfigure(3, weight=0)
        self.tabTrend.grid_rowconfigure(4, weight=0)
        self.tabTrend.grid_rowconfigure(5, weight=0, minsize=10)
        self.tabTrend.grid_rowconfigure(6, weight=0)
        self.tabTrend.grid_rowconfigure(7, weight=0, minsize=150)

        self.tabTrend.grid_rowconfigure(10, weight=1)

    def insertCreatedWidget(self, text):
        for child in self.tabTrendTreeCreatedWidgets.get_children():
            if self.tabTrendTreeCreatedWidgets.item(child)["text"] == text:
                self.main.log("Trend widget with name " + text + " already exists, deleting it")
                return
        self.tabTrendTreeCreatedWidgets.insert("", "end", text=text)

    def getObjects(self):
        objects = []
        for child in self.tabTrendTreeObjectsNames.get_children():
            objects.append(self.tabTrendTreeObjectsNames.item(child)["text"])
        objects.pop()
        return objects

    def getWidgetNameInFiles(self):
        return self.name

    def getAddPrefixToWidgetNameInFiles(self):
        if self.addPrefixTrend.get() == 1:
            return True
        else:
            return False
