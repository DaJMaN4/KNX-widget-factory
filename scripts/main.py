import os
import pip
from tkinter import *
from tkinter import ttk
import copy
from time import sleep


# Check if yaml module is installed, if not then install it
try:
    import yaml
except ImportError:
    print("Trying to Install required module: pyyaml\n")
    pip.main(['install', "pyyaml"])
    import yaml

# Check if selenium module is installed, if not then install it
try:
    #import selenium
    ...
except ImportError:
    print("Trying to Install required module: selenium\n")

    import selenium

import databaseManager, webManagement
from widgets import ImportWidgets, InfoWidgetFactory, TrendWidgetFactory, CreateSchematics
from structures import mainStructure, frameworkStructure
from gui import guiElements, guiRightBar, guiTabInfo, guiTabTrend, guiTabStructure, guiBoxDataTab
from utils import guiUtilities, importUtil


class Main:
    def __init__(self):
        self.trendWidgetDictionary = {}
        self.infoWidgetDictionary = {}
        self.boxesIDs = None
        self.mainStructureFile = None
        self.frameworkFile = None
        self.schematicInfoName = None
        self.mainStructureFileName = None
        self.frameworkFileName = None
        self.path = os.path.dirname(os.path.dirname(__file__))
        self.databaseManagerObject = databaseManager.DatabaseManager(self.path, self)
        self.biggestWidgetID = 0
        self.boxDataTabs = {}
        self.boxDataTabsLabelsForResize = []
        self.roomNumbers = []

        self.createFolders()

        self.guiUtilities = guiUtilities.guiUtilities(self)

        self.root = Tk()
        self.root.columnconfigure(1, weight=0)
        self.root.rowconfigure(1, weight=1, minsize=400)
        self.root.columnconfigure(2, weight=0)
        self.root.rowconfigure(2, weight=1)
        self.root.columnconfigure(3, weight=1)

        self.root.geometry("1000x700")
        self.root.title('LM Widget Creator')

        self.createTab()
        self.createOutput()
        self.rightBar = guiRightBar.GuiRightBar(self, self.root, self.guiUtilities, self.databaseManagerObject, self.path)

        self.guiElements = guiElements.guiElements(self.guiUtilities, self)

        self.root.bind("<Configure>", self.resizeLabels)
        self.root.mainloop()

    def createFolders(self):
        if not os.path.exists(self.path + "/data"):
            os.mkdir(self.path + "/data")
        if not os.path.exists(self.path + "/output"):
            os.mkdir(self.path + "/output")
        if not os.path.exists(self.path + "/output/widgets"):
            os.mkdir(self.path + "/output/widgets")
        if not os.path.exists(self.path + "/output/levels"):
            os.mkdir(self.path + "/output/levels")
        if not os.path.exists(self.path + "/output/frameworks"):
            os.mkdir(self.path + "/output/frameworks")
        if not os.path.exists(self.path + "/schematics"):
            os.mkdir(self.path + "/schematics")
        if not os.path.exists(self.path + "/schematics/levels"):
            os.mkdir(self.path + "/schematics/levels")
        if not os.path.exists(self.path + "/schematics/frameworks"):
            os.mkdir(self.path + "/schematics/frameworks")
        if not os.path.exists(self.path + "/schematics/widgets"):
            os.mkdir(self.path + "/schematics/widgets")
        if not os.path.exists(self.path + "/schematics/widgets/info"):
            os.mkdir(self.path + "/schematics/widgets/info")
        if not os.path.exists(self.path + "/schematics/widgets/trends"):
            os.mkdir(self.path + "/schematics/widgets/trends")
        if not os.path.exists(self.path + "/schematics/widgets/trends/default.yml"):
            CreateSchematics.CreateSchematics(self)

    # Resizes labels to fit their text
    def resizeLabels(self, event):
        # Update the label's wraplength to its current width
        self.TabTrend.tabTextTrend.config(wraplength=self.TabTrend.tabTextTrend.winfo_width())
        self.TabInfo.tabTextInfo.config(wraplength=self.TabInfo.tabTextInfo.winfo_width())
        for tab in self.boxDataTabsLabelsForResize:
            tab.config(wraplength=tab.winfo_width())

    # Creates output text box
    def createOutput(self):
        self.output = Text(self.root, height=15, width=50)  # self.TabFrame
        self.output.config()  # Start with the Text widget in read-only mode

        # self.output.pack(fill=BOTH, expand=True)
        self.output.grid(row=2, column=3, sticky="nsew")

        self.output.insert(END, "Welcome!\n")
        self.output.config(state=DISABLED)  # Disable editing to prevent user input

    # Creates tabbed interface
    def createTab(self):
        self.TabFrame = Frame(self.root)
        self.TabFrame.grid(row=3, column=3, sticky="nsew", columnspan=2, rowspan=2)

        self.tabControl = ttk.Notebook(self.root)

        self.tabTrend = ttk.Frame(self.tabControl)
        self.tabInfo = ttk.Frame(self.tabControl)
        self.tabStructure = ttk.Frame(self.tabControl)

        self.tabControl.add(self.tabTrend, text='Trend Widgets')
        self.tabControl.add(self.tabInfo, text='Info Widgets')
        self.tabControl.add(self.tabStructure, text='Framework & Level')
        self.tabControl.grid(column=3, row=1, sticky="nsew", columnspan=2, rowspan=2)
        self.tabTrend.rowconfigure(1, weight=1)
        self.tabTrend.rowconfigure(2, weight=1)
        self.tabTrend.columnconfigure(1, weight=2)
        self.tabTrend.columnconfigure(2, weight=4)
        self.tabTrend.columnconfigure(3, weight=10)
        self.tabInfo.rowconfigure(1, weight=1)
        self.tabInfo.rowconfigure(2, weight=1)
        self.tabInfo.columnconfigure(1, weight=2)
        self.tabInfo.columnconfigure(2, weight=4)
        self.tabInfo.columnconfigure(3, weight=10)
        self.tabStructure.rowconfigure(1, weight=1)
        self.tabInfo.columnconfigure(1, weight=2)
        self.tabInfo.columnconfigure(2, weight=14)

        self.TabTrend = guiTabTrend.guiTabTrend(self, self.root, self.tabTrend, self.guiUtilities, )
        self.TabInfo = guiTabInfo.guiTabInfo(self, self.root, self.tabInfo, self.guiUtilities)
        self.TabStructure = guiTabStructure.guiTabStructure(self, self.root, self.tabStructure, self.guiUtilities)

    # Logs text to output text box in gui
    def log(self, text):
        self.output.config(state=NORMAL)
        self.output.insert(END, text + "\n")
        self.output.config(state=DISABLED)

    # Checks if all required fields are filled to start any creation
    def checksBeforeCreating(self):
        if self.databaseManagerObject.connection is None:
            self.log("Database is not imported. Aborting")
            return False

        if self.guiElements.getRoomNumbers() == []:
            self.log("Rooms are not selected. Aborting")
            return False
        return True

    def createTrendWidgets(self):
        if self.TabTrend.name == "":
            self.log("Trend widget name is not specified. Aborting")
            return
        trendWidgetFactory = TrendWidgetFactory.TrendWidgetFactory(
            self.guiElements.getRoomNumbers(),
            self.TabTrend.getWidgetNameInFiles(),
            self.TabTrend.getAddPrefixToWidgetNameInFiles(),
            self.TabTrend.getObjects(),
            self.path,
            "",  # config.getTrendWidgetSchematicToUse(),
            self
        )
        # Run run function of TrendWidgetFactory class
        trendWidgetFactory.run()
        # If module is enabled then print message
        if trendWidgetFactory.isEnable():
            pass
            # print("All trend widgets created and saved in output folder")

    def createInfoWidgets(self):
        if self.TabInfo.getWidgetNameVisible() == "":
            self.log("Info widget name is not specified. Aborting")
            return

        if self.TabInfo.getWidgetNameInFiles() == "":
            self.log("Info widget name is not specified. Aborting")
            return

        if self.schematicInfoName is None:
            self.log("Info widget schematic is not imported. Aborting")
            return

        infoWidgetFactory = InfoWidgetFactory.InfoWidgetFactory(
            self.guiElements.getRoomNumbers(),
            self.TabInfo.getAddPrefixToWidgetVisible(),
            self.TabInfo.getWidgetNameVisible(),
            self.TabInfo.getAddPrefixToWidgetNameInFiles(),
            self.TabInfo.getWidgetNameInFiles(),
            self.TabInfo.getObjects(),
            self.path,
            self.schematicInfoName,  # config.getRoomWidgetsSchematicToUse(),
            self
        )
        # Run run function of InfoWidgetFactory class
        infoWidgetFactory.run()
        # If module is enabled then print message
        if infoWidgetFactory.isEnable():
            self.log("All info widgets created and saved in output folder")

    # Creates dictionary boxdata and rooms with mainStructureManager object and runs it
    def createStructure(self):
        boxData = {}
        rooms = {}
        for tab in self.boxDataTabs:
            tab = self.boxDataTabs[tab]
            boxData[tab.name] = {"template": tab.template.get(), "objectsNames": tab.objectsNames, "normal": tab.boxIcon.get(),
                                 "trendIcon": tab.trendIcon.get(), "rooms": tab.selectedRooms}
            rooms[tab.name] = tab.selectedRooms
        mainStructureManagerObject = mainStructure.mainStructureManager(
            self.path,
            self.frameworkFile,
            self.mainStructureFile,
            boxData,
            rooms,
            self.rightBar.createTrendWidget.get() == 1,
            self.guiElements.getRoomNumbers(),
            self,
            importUtil.ImportManager(self.path)
        )
        if mainStructureManagerObject.isEnable():
            mainStructureManagerObject.run()
            self.mainStructureName = mainStructureManagerObject.getName()
            self.log("Level created and saved in output folder")

        frameworkStructureObject = frameworkStructure.frameworkStructure(
            self.path,
            self.frameworkFile,
            self.mainStructureFile,
            boxData,
            rooms,
            self,
            importUtil.ImportManager(self.path)
        )
        if frameworkStructureObject.isEnable():
            frameworkStructureObject.run()
            self.frameworkName = frameworkStructureObject.getName()

    # Creates webManagement object and returns it
    def createWebManagement(self, login, password, ip):
        webManagementObject = webManagement.WebManagement(
            self.path,
            login,
            password,
            ip,
            self
        )
        return webManagementObject

    # Getter for databaseManagerObject
    def getDatabaseObject(self):
        return self.databaseManagerObject

    # Returns ID of trend widget for room number
    def getTrendWidgetDictionary(self, roomNumber):
        if self.trendWidgetDictionary.get(roomNumber) is None:
            self.log("Room Number " + roomNumber +
                  " Does not have corresponding trend widget that was created in this runtime")
            return ""
        return self.trendWidgetDictionary[roomNumber]

    # Returns ID of info widget for room number
    def getInfoWidgetDictionary(self, roomNumber):
        if self.infoWidgetDictionary.get(roomNumber) is None:
            self.log("Room Number " + roomNumber +
                  " Does not have corresponding info widget that was created in this runtime")
            return ""
        return self.infoWidgetDictionary[roomNumber]

    # Getter for boxesIDs
    def getBoxesIDs(self):
        return self.boxesIDs

    # Getter for biggestWidgetID
    def getBiggestWidgetID(self):
        return self.biggestWidgetID

    # Used to get new bigges widget ID which that is used to assign widgets to objects in level and framework
    # Also adds corresponding widget ID to dictionary of widgets types
    def newBiggestWidgetID(self, widgetType, room):
        self.biggestWidgetID += 1
        if widgetType == "trend":
            self.trendWidgetDictionary[room] = self.biggestWidgetID
        elif widgetType == "info":
            self.infoWidgetDictionary[room] = self.biggestWidgetID
        else:
            self.log("Something went very wrong, ID of widgets cannot be determined. This might make the whole application not functioning properly")
        return self.biggestWidgetID

    # Setter for boxesIDs
    def setBoxesIDs(self, ids):
        self.boxesIDs = ids

    # Getter for path
    def getPath(self):
        return self.path

    # Creates new guiBoxDataTab object and adds it to boxDataTabs dictionary
    def createNewBoxDataTab(self, frame, item, name):
        self.boxDataTabs[item] = (guiBoxDataTab.GuiBoxDataTab(frame, self, self.tabStructure, self.guiUtilities,
                                                              self.databaseManagerObject.getAllIcons(), name))

    # Updates label showing name of imported level for all guiBoxDataTab objects
    def updateImportedLevelStructure(self, file):
        file = file.name
        self.mainStructureFile = file
        for tab in self.boxDataTabs:
            self.boxDataTabs[tab].updateImportedLevel(file)

    # Updates label showing name of imported framework for all guiBoxDataTab objects
    def updateImportedFrameworkStructure(self, file):
        file = file.name
        self.frameworkFile = file
        for tab in self.boxDataTabs:
            self.boxDataTabs[tab].updateImportedFramework(file)

    # Adds room to roomNumbers list for all guiBoxDataTab objects
    def addRoom(self, rooms):
        self.roomNumbers = rooms
        for tab in self.boxDataTabs:
            self.boxDataTabs[tab].updateRoomNames(self.roomNumbers)

    # guiTabStructure object uses this function to add rooms to correct tab in guiBoxDataTab object
    def triesToSelectRooms(self, selectedItems):
        for item in selectedItems:
            if item == "" or item == None:
                selectedItems.remove(item)
        selectedItemsOutput = copy.deepcopy(selectedItems)
        if self.tabControl.tab(self.tabControl.select(), "text") == "Framework & Level":
            boxName = self.TabStructure.tabControlBoxData.tab(self.TabStructure.tabControlBoxData.select(), "text")
            for tab in self.boxDataTabs:
                if self.boxDataTabs[tab].name == boxName:
                    for room in selectedItems:
                        for secondTab in self.boxDataTabs:
                            if self.boxDataTabs[tab].name != self.boxDataTabs[secondTab].name:
                                if room in self.boxDataTabs[secondTab].selectedRooms:
                                    self.log("Room " + room + " is already selected in " + self.boxDataTabs[secondTab].name + ". Skipping..")
                                    selectedItemsOutput.remove(room)
                    self.boxDataTabs[tab].selectRooms(selectedItemsOutput)

    # Creates ImportManager object and returns it
    def createImportWidgetSchematic(self):
        importManager = ImportWidgets.ImportManager(
            self.path,
            self.TabInfo.getObjects(),
            self
        )
        return importManager

    # guiRightBar object triggers this function when it's about to create and upload all data
    # Currently it's used to compensate for uploading level and framework before widgets, it is needed to get the
    # correct biggestWidgetID
    def creatingStructure(self):
        self.biggestWidgetID += 2

    # DatabaseManager object triggers this function when it's done with updating database
    # Currently it's used to update icons in boxDataTabs
    def updateDatabase(self, icons):
        for tab in self.boxDataTabs:
            self.boxDataTabs[tab].databaseUpdate(icons)

    # guiRightBar object triggers this function when it's about to create levels and frameworks
    def checkBeforeUploadingFrameworkAndLevel(self):
        if self.frameworkFile == None:
            self.log("Framework schematic is not imported. Aborting")
            return False
        if self.mainStructureFile == None:
            self.log("Level schematic is not imported. Aborting")
            return False
        for tab in self.boxDataTabs:
            if self.boxDataTabs[tab].selectedRooms == []:
                self.log("Rooms are not selected for room type '" + self.boxDataTabs[tab].name + "'. Aborting")
                return False
            if self.boxDataTabs[tab].template.get() == "":
                self.log("Template is not selected for room type '" + self.boxDataTabs[tab].name + "'. Aborting")
                return False
            if self.boxDataTabs[tab].boxIcon.get() == "":
                self.log("Box icon is not selected for room type '" + self.boxDataTabs[tab].name + "'. Aborting")
                return False
            if (self.boxDataTabs[tab].template.get() == None or
                    self.boxDataTabs[tab].template.get() not in self.boxDataTabs[tab].selectedRooms):
                self.log("Template is not in selected rooms for room type '" + self.boxDataTabs[tab].name + "'. Aborting")
                return False
        return True


if __name__ == '__main__':
    main = Main()


# TODO: make KNX name working

# TODO: Changing name of tabs in boxDataTabs

# TODO: make try except for uploading with webManagement

# TODO: when creating new tab in boxDataTabs, imported schematics dont show up

# TODO: It always deletes prefix info for name widget
