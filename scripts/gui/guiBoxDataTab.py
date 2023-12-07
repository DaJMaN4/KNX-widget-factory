from tkinter import *
from tkinter import ttk
from tkinter.font import Font
from tkinter.filedialog import askopenfile


class GuiBoxDataTab:
    def __init__(self, frame, main, mainTab, guiUtilities, icons, name):
        self.frame = frame
        self.main = main
        self.mainTab = mainTab
        self.guiUtilities = guiUtilities
        self.icons = icons
        self.name = name

        self.selectedRooms = []
        self.objectsNames = []

        self.createBoxDataDefault()

    def onItemDoubleClickObjectsNames(self, event):
        self.guiUtilities.onItemDoubleClick(event, self.tabStructureTreeObjectsNames, self.tabStructureTreeObjectsNames)

    def databaseUpdate(self, icons):
        self.trendIconChoicer['values'] = icons
        self.boxIconChoicer['values'] = icons

    def unlink(self):
        self.main.boxDataTabsLabelsForResize.remove(self.tabTextStructure)

    def importFrameworkSchematic(self):
        file = askopenfile(mode='r', filetypes=[("Framework", '*.tar')])
        if file is not None:
            self.schematicFrameworkFile = file
            self.importedFrameworkLabel.config(text="Framework: " + file.name.split("/")[-1])
            self.main.updateImportedFrameworkStructure(file)

    def importLevelSchematic(self):
        file = askopenfile(mode='r', filetypes=[("Level", '*.tar')])
        if file is not None:
            self.schematicLevelName = file
            self.importedLevelLabel.config(text="Level: " + file.name.split("/")[-1])
            self.main.updateImportedLevelStructure(file)

    def createBoxDataDefault(self):
        self.tabStructureTreeObjectsNames = ttk.Treeview(master=self.frame)
        self.tabStructureTreeObjectsNames.column("#0", width=300, minwidth=150)
        self.tabStructureTreeObjectsNames.heading("#0", text="Object Names", anchor=W)

        self.tabStructureTreeObjectsNames.insert("", "end", text="Romtemperatur - Verdi")
        self.objectsNames.append("Romtemperatur - Verdi")
        self.tabStructureTreeObjectsNames.insert("", "end", text="Varmeaktuator - Tilbakemelding")
        self.objectsNames.append("Varmeaktuator - Tilbakemelding")
        self.tabStructureTreeObjectsNames.insert("", "end", text="Kjoleaktuator - Tilbakemelding")
        self.objectsNames.append("Kjoleaktuator - Tilbakemelding")
        self.tabStructureTreeObjectsNames.insert("", "end", text="CO2 i rom - Verdi")
        self.objectsNames.append("CO2 i rom - Verdi")
        self.tabStructureTreeObjectsNames.insert("", "end", text="Tilstedesensor -")
        self.objectsNames.append("Tilstedesensor -")

        self.tabStructureTreeObjectsNames.insert("", "end", text="")
        self.tabStructureTreeObjectsNames.bind("<Double-1>", self.onItemDoubleClickObjectsNames)
        self.tabStructureTreeObjectsNames.grid(row=1, column=1, sticky="nsew", rowspan=40)

        self.tabStructureTreeRooms = ttk.Treeview(master=self.frame)
        self.tabStructureTreeRooms.column("#0", width=110, minwidth=110)
        self.tabStructureTreeRooms.heading("#0", text="Selected Rooms", anchor=W)
        self.tabStructureTreeRooms.grid(row=1, column=2, sticky="nsew", rowspan=40)

        title_font = Font(family="Helvetica", size=15, weight="bold")
        label = Label(self.frame, text="Structure", font=title_font)
        label.grid(row=1, column=3, sticky="n")

        self.tabTextStructure = Label(self.frame,
                                      text="In order to create Structure, you must first create a framework and level "
                                           "which will be used as schematics to create objects and assign group addresses to them. "
                                           "In framework there must be boxes for each room, and in level there must be "
                                           "text labels on each box with room name, same room name as in column 'level'. "
                                           "For each box type there must be a box with everything done, it will be used as template for the rest. "
                                           "To add new box type, double click under newest box type, insert name and click enter. "
                                           "To select rooms, click ctrl and click on rooms and then click enter."
                                           "If trend widget creation is chosen then the program will automatically connect them to icons. "
                                           "Choices for icons will appear only when database is imported. "
                                      )
        self.tabTextStructure.grid(row=2, column=3, sticky="new")


        self.templateTabTextStructure = Label(self.frame, text="Choose which room will be used as template")
        self.templateTabTextStructure.grid(column=3, row=3, sticky="")


        self.template = StringVar()

        self.templateChoicer = ttk.Combobox(self.frame, width=27, textvariable=self.template)
        # Adding combobox drop down list
        self.templateChoicer['values'] = self.main.roomNumbers

        self.templateChoicer.grid(column=3, row=4)


        self.boxTabTextStructure = Label(self.frame, text="Insert which icon is used as box icon")
        self.boxTabTextStructure.grid(column=3, row=5, sticky="")


        self.main.boxDataTabsLabelsForResize.append(self.tabTextStructure)

        self.boxIcon = StringVar()

        self.boxIconChoicer = ttk.Combobox(self.frame, width=27, textvariable=self.boxIcon)

        # Adding combobox drop down list
        self.boxIconChoicer['values'] = self.icons

        self.boxIconChoicer.grid(column=3, row=6)

        self.trendTabTextStructure = Label(self.frame, text="Choose which icon will be used for trend widgets.")
        self.trendTabTextStructure.grid(column=3, row=7, sticky="")

        self.trendIcon = StringVar()

        self.trendIconChoicer = ttk.Combobox(self.frame, width=27,
                                      textvariable=self.trendIcon)
        # Adding combobox drop down list
        self.trendIconChoicer['values'] = self.icons

        self.trendIconChoicer.grid(column=3, row=8)

        separator = ttk.Separator(self.frame, orient='horizontal')
        separator.grid(column=3, row=10, sticky="nsew")

        self.importedLevelLabel = Label(self.frame, text="Common Data")
        self.importedLevelLabel.grid(column=3, row=11, sticky="")

        add_button = Button(self.frame, text="import Level schematic",
                            command=lambda: self.importLevelSchematic())
        add_button.grid(column=3, row=12)

        self.importedLevelLabel = Label(self.frame, text="No level schematic imported")
        self.importedLevelLabel.grid(column=3, row=13, sticky="")

        add_button = Button(self.frame, text="import Framework schematic",
                            command=lambda: self.importFrameworkSchematic())
        add_button.grid(row=14, column=3)

        self.importedFrameworkLabel = Label(self.frame, text="No framework schematic imported")
        self.importedFrameworkLabel.grid(column=3, row=15, sticky="")

    def updateImportedFramework(self, file):
        self.importedFrameworkLabel.config(text=file.split("/")[-1])
        self.schematicFrameworklName = file

    def updateImportedLevel(self, file):
        self.importedLevelLabel.config(text=file.split("/")[-1])
        self.schematicLevelName = file

    def updateRoomNames(self, roomNames):
        self.templateChoicer['values'] = roomNames

    def selectRooms(self, selectedRooms):
        self.selectedRooms = selectedRooms
        self.tabStructureTreeRooms.delete(*self.tabStructureTreeRooms.get_children())
        for room in selectedRooms:
            self.tabStructureTreeRooms.insert("", "end", text=room)


