from tkinter import *
from tkinter import ttk
from tkinter.font import Font
from tkinter.filedialog import askopenfile


class guiTabInfo:
    def __init__(self, main, root, tabInfo, guiUtilities):
        self.main = main
        self.root = root
        self.tabInfo = tabInfo
        self.guiUtilities = guiUtilities

        self.nameVisible = ""
        self.nameInFiles = ""

        self.createTabInfo()

    def onItemDoubleClickTreeCreated(self, event):
        self.guiUtilities.onItemDoubleClick(event, self.tabInfo, self.tabInfoTreeCreatedWidgets)

    def onItemDoubleClickTabInfoObjects(self, event):
        self.guiUtilities.onItemDoubleClick(event, self.tabInfoTreeObjectsNames, self.tabInfoTreeObjectsNames)

    def importSchematic(self):
        file = askopenfile(mode='r', filetypes=[("Info Widget", '*.tar')])
        if file is not None:
            importWidgets = self.main.createImportWidgetSchematic()
            importWidgets.open(file.name)
            self.main.schematicInfoName = file.name.split("/")[-1]
            self.chosenSchematicLabel.config(text="Chosen schematic: " + file.name.split("/")[-1])

    def createTabInfo(self):
        self.tabInfoTreeCreatedWidgets = ttk.Treeview(master=self.tabInfo)

        self.tabInfoTreeCreatedWidgets.column("#0", width=100, minwidth=150)

        self.tabInfoTreeCreatedWidgets.heading("#0", text="Created Widgets", anchor=W)

        self.tabInfoTreeCreatedWidgets.bind("<Double-1>", self.onItemDoubleClickTreeCreated)
        self.tabInfoTreeCreatedWidgets.grid(row=1, column=1, sticky="nsew", rowspan=30)


        self.tabInfoTreeObjectsNames = ttk.Treeview(master=self.tabInfo)
        self.tabInfoTreeObjectsNames.column("#0", width=300, minwidth=150)
        self.tabInfoTreeObjectsNames.heading("#0", text="Object Names", anchor=W)

        self.tabInfoTreeObjectsNames.insert("", "end", text="Driftsmodus - Rom")
        self.tabInfoTreeObjectsNames.insert("", "end", text="Tilstedesensor -")
        self.tabInfoTreeObjectsNames.insert("", "end", text="Romtemperatur - Verdi")
        self.tabInfoTreeObjectsNames.insert("", "end", text="Romtemperatur - Aktivt settpunkt")
        self.tabInfoTreeObjectsNames.insert("", "end", text="Romtemperatur - Lokal")
        self.tabInfoTreeObjectsNames.insert("", "end", text="Romtemperatur - Settpunkt")
        self.tabInfoTreeObjectsNames.insert("", "end", text="Varmeaktuator - Tilbakemelding")
        self.tabInfoTreeObjectsNames.insert("", "end", text="Kjoleaktuator - Tilbakemelding")
        self.tabInfoTreeObjectsNames.insert("", "end", text="CO2 i rom - Verdi")
        self.tabInfoTreeObjectsNames.insert("", "end", text="Fukt i rom - Verdi")


        ###### IT DONT SHOW ERROR WITHOUT COMMENTING THIS LINES
        # objectsNames: ["Romtemperatur - Verdi", "Varmeaktuator - Tilbakemelding",
        #               "Kjoleaktuator - Tilbakemelding", "CO2 i rom - Verdi", "Tilstedesensor -"]

        self.tabInfo.grid_rowconfigure(0, weight=0)
        self.tabInfo.grid_rowconfigure(1, weight=0)
        self.tabInfo.grid_rowconfigure(2, weight=0)
        self.tabInfo.grid_rowconfigure(3, weight=0)
        self.tabInfo.grid_rowconfigure(4, weight=0)
        self.tabInfo.grid_rowconfigure(5, weight=0)
        self.tabInfo.grid_rowconfigure(7, weight=0)
        self.tabInfo.grid_rowconfigure(8, weight=0)
        self.tabInfo.grid_rowconfigure(9, weight=0)
        self.tabInfo.grid_rowconfigure(10, weight=0)
        self.tabInfo.grid_rowconfigure(11, weight=0)
        self.tabInfo.grid_rowconfigure(12, weight=0)
        self.tabInfo.grid_rowconfigure(13, weight=0)
        self.tabInfo.grid_rowconfigure(14, weight=0)
        self.tabInfo.grid_rowconfigure(15, weight=0)
        self.tabInfo.grid_rowconfigure(16, weight=0)
        self.tabInfo.grid_rowconfigure(17, weight=0)
        self.tabInfo.grid_rowconfigure(19, weight=0)
        self.tabInfo.grid_rowconfigure(21, weight=0)
        self.tabInfo.grid_rowconfigure(22, weight=0)
        self.tabInfo.grid_rowconfigure(23, weight=1)

        self.tabInfoTreeObjectsNames.insert("", "end", text="")
        self.tabInfoTreeObjectsNames.bind("<Double-1>", self.onItemDoubleClickTabInfoObjects)
        self.tabInfoTreeObjectsNames.grid(row=1, column=2, sticky="nsew", rowspan=30)

        title_font = Font(family="Helvetica", size=15, weight="bold")
        label = Label(self.tabInfo, text="Info Widgets", font=title_font)
        label.grid(row=1, column=3, sticky="n")

        # self.tabInfo.grid_rowconfigure(1, weight=1)

        self.tabTextInfo = Label(self.tabInfo,
                                 text="To create Info Widgets, specify on the most left column named 'Name' numbers of rooms. "
                                      "If in KNX file identifier of this room is diffrent then just room name specify the knx name of the widget in column "
                                      "'Knx Name'. Remember that column 'Name' is used to find objects in LM database."
                                      " Use %name% as placeholder for setting name of rooms on LM."
                                      " Import schematic file that will be use as template for creating widgets."
                                      " In the place of widget name write 'room' to signalize that that label will be replaced by room name."
                                      " Remember that objects assigned to that widget must be for the same room as widget. ")
        self.tabTextInfo.grid(row=2, column=3, sticky="new")

        def on_entry_change_files(*args):
            value = entry_text_files.get()
            roomName = self.main.guiElements.getRoomNumbers()[0]
            if self.addPrefixInfoFiles.get() == 1:
                num = 0
                for c in roomName:
                    if not c.isdigit():
                        # Delete character from string at index num
                        roomName = roomName[:num] + roomName[num + 1:]
                    else:
                        break
                    num = num + 1
            self.nameVisible = value
            value = value.replace("%name%", roomName)
            self.labelPreviewInfoVisible.config(text="Preview: " + value)

        self.labelPreviewInfoVisible = Label(self.tabInfo, text="Preview: ")
        self.labelPreviewInfoVisible.grid(row=3, column=3)

        entry_text_files = StringVar()
        entry_text_files.trace_add("write", on_entry_change_files)

        entry = Entry(master=self.tabInfo, textvariable=entry_text_files, width=30)
        entry.grid(row=4, column=3)

        self.addPrefixInfoFiles = IntVar()

        button = ttk.Checkbutton(self.tabInfo, text="Do not add prefix to widget name", variable=self.addPrefixInfoFiles, command=on_entry_change_files)
        button.grid(row=5, column=3, sticky="n")

        self.tabInfo.grid_rowconfigure(6, weight=0, minsize=30)

        def on_entry_change_visible(*args):
            value = entry_text_visible.get()
            roomName = self.main.guiElements.getRoomNumbers()[0]
            if self.addPrefixInfoVisible.get() == 1:
                num = 0
                for c in roomName:
                    if not c.isdigit():
                        # Delete character from string at index num
                        roomName = roomName[:num] + roomName[num + 1:]
                    else:
                        break
                    num = num + 1
            self.nameInFiles = value
            value = value.replace("%name%", roomName)
            self.labelPreviewInFiles.config(text="Preview: " + value)


        entry_text_visible = StringVar()
        entry_text_visible.trace_add("write", on_entry_change_visible)

        self.labelPreviewInFiles = Label(self.tabInfo, text="Preview: ")
        self.labelPreviewInFiles.grid(row=15, column=3, sticky="n")

        entry = Entry(master=self.tabInfo, textvariable=entry_text_visible, width=30)
        entry.grid(row=16, column=3)

        self.addPrefixInfoVisible = IntVar()

        radioBox = ttk.Checkbutton(self.tabInfo, text="Do not add prefix to widget name in files", variable=self.addPrefixInfoVisible, command=on_entry_change_visible)
        radioBox.grid(row=17, column=3)

        self.tabInfo.grid_rowconfigure(18, weight=0, minsize=30)

        add_button = Button(self.tabInfo, text="import schematic", command=lambda: self.importSchematic())
        add_button.grid(row=19, column=3)

        self.tabInfo.grid_columnconfigure(3, weight=1, minsize=30)
        self.tabInfo.grid_rowconfigure(20, weight=0, minsize=20)

        self.chosenSchematicLabel = Label(self.tabInfo, text="No schematic imported")
        self.chosenSchematicLabel.grid(row=21, column=3, sticky="n")

    def insertCreatedWidget(self, text):
        for child in self.tabInfoTreeCreatedWidgets.get_children():
            if self.tabInfoTreeCreatedWidgets.item(child)["text"] == text:
                self.main.log("Info widget with name " + text + " already exists, deleting it")
                return
        self.tabInfoTreeCreatedWidgets.insert("", "end", text=text)

    def deleteCreatedWidget(self, text):
        for child in self.tabInfoTreeCreatedWidgets.get_children():
            if self.tabInfoTreeCreatedWidgets.item(child)["text"] == text:
                self.tabInfoTreeCreatedWidgets.delete(child)
                return

    def getObjects(self):
        objects = []
        for child in self.tabInfoTreeObjectsNames.get_children():
            objects.append(self.tabInfoTreeObjectsNames.item(child)["text"])
        objects.pop()
        return objects

    def getWidgetNameInFiles(self):
        return self.nameInFiles

    def getAddPrefixToWidgetNameInFiles(self):
        if self.addPrefixInfoFiles.get() == 1:
            return True
        else:
            return False

    def getWidgetNameVisible(self):
        return self.nameVisible

    def getAddPrefixToWidgetVisible(self):
        if self.addPrefixInfoVisible.get() == 1:
            return True
        else:
            return False


