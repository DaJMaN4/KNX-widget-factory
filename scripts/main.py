import os
import pip
from tkinter import *
from tkinter import ttk

# Check if yaml module is installed, if not then install it
try:
    import yaml
except ImportError:
    print("Trying to Install required module: pyyaml\n")
    pip.main(['install', "pyyaml"])
    import yaml

# Check if selenium module is installed, if not then install it
try:
    import selenium
except ImportError:
    print("Trying to Install required module: selenium\n")
    pip.main(['install', "selenium"])
    import selenium

import ConfigManager, databaseManager, webManagement
from widgets import ImportWidgets, InfoWidgetFactory, TrendWidgetFactory
from structures import mainStructure, frameworkStructure
from gui import guiElements, guiRightBar, guiTabInfo, guiTabTrend, guiTabStructure, guiBoxDataTab
from utils import guiUtilities

# if config.getCreateStructures():
#    self.biggestWidgetID += 2


class Main:
    def __init__(self):
        self.trendWidgetDictionary = {}
        self.infoWidgetDictionary = {}
        self.boxesIDs = None
        self.mainStructureFile = None
        self.frameworkFile = None
        self.path = os.path.dirname(os.path.dirname(__file__))
        self.databaseManagerObject = databaseManager.DatabaseManager(self.path, self)
        self.biggestWidgetID = 0  # self.databaseManagerObject.getBiggestWidgetID()
        self.schematicInfoName = None
        self.boxDataTabs = {}
        self.boxDataTabsLabelsForResize = []
        self.roomNumbers = []

        self.guiUtilities = guiUtilities.guiUtilities(self)

        self.root = Tk()
        self.root.columnconfigure(1, weight=0)
        self.root.rowconfigure(1, weight=1, minsize=400)
        self.root.columnconfigure(2, weight=0)
        self.root.rowconfigure(2, weight=1)
        self.root.columnconfigure(3, weight=1)
        self.root.rowconfigure(3, weight=1)
        self.root.geometry("1000x700")
        self.root.title('LM Widget Creator')

        self.createTab()
        self.createOutput()
        self.rightBar = guiRightBar.GuiRightBar(self, self.root, self.guiUtilities, self.databaseManagerObject)

        self.guiElements = guiElements.guiElements(self.guiUtilities, self)

        self.root.bind("<Configure>", self.resizeLabels)
        self.root.mainloop()

    def resizeLabels(self, event):
        # Update the label's wraplength to its current width
        self.TabTrend.tabTextTrend.config(wraplength=self.TabTrend.tabTextTrend.winfo_width())
        self.TabInfo.tabTextInfo.config(wraplength=self.TabInfo.tabTextInfo.winfo_width())
        for tab in self.boxDataTabsLabelsForResize:
            tab.config(wraplength=tab.winfo_width())

    def createOutput(self):
        self.output = Text(self.TabFrame, height=15, width=50)
        self.output.config()  # Start with the Text widget in read-only mode

        self.output.pack(fill=BOTH, expand=True)

        self.output.insert(END, "Welcome!\n")
        self.output.config(state=DISABLED)  # Disable editing to prevent user input



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

    def log(self, text):
        self.output.config(state=NORMAL)
        self.output.insert(END, text + "\n")
        self.output.config(state=DISABLED)

    # Runs everything
    def run(self):
        # Create object of Config class


        return
        config = ConfigManager.Config(self.path)

        # Create object of ImportManager class
        importManager = ImportWidgets.ImportManager(
            self.path,
            config.getRoomWidgetsObjectsNamesWidget(),
            main
        )
        # Run open function of ImportManager class
        importManager.open()

    def checksBeforeCreating(self):
        if self.databaseManagerObject.connection is None:
            self.log("Database is not imported. Aborting")
            return

    def createTrendWidgets(self):
        if self.tabTrend.widgetName == "":
            self.log("Widget name is not specified. Aborting")
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
            self.log("Widget name is not specified. Aborting")
            return

        if self.TabInfo.getWidgetNameInFiles() == "":
            self.log("Widget name is not specified. Aborting")
            return

        infoWidgetFactory = InfoWidgetFactory.InfoWidgetFactory(
            self.guiElements.getRoomNumbers(),
            self.TabInfo.getAddPrefixToWidgetVisible(),
            self.TabInfo.getWidgetNameVisible(),
            self.TabInfo.getAddPrefixToWidgetNameInFiles(),
            self.TabInfo.getWidgetNameInFiles(),
            self.TabInfo.getObjects(),
            self.path,
            self.schematicInfoName,   # config.getRoomWidgetsSchematicToUse(),
            self
        )

        # Run run function of InfoWidgetFactory class
        infoWidgetFactory.run()
        # If module is enabled then print message
        if infoWidgetFactory.isEnable():
            print("All info widgets created and saved in output folder")

    def createStructure(self):
        boxData = {}
        rooms = []
        for tab in self.boxDataTabs:
            tab = self.boxDataTabs[tab]
            boxData[tab.name] = [{"template":"A3001", "objectsNames":tab.objectsNames, "normal":tab.boxIcon,
                                  "trendIcon":tab.trendIcon, "rooms":tab.selectedRooms}]
            for room in tab.selectedRooms:
                if room not in self.roomNumbers:
                    self.roomNumbers.append(room)
        mainStructureManagerObject = mainStructure.mainStructureManager(
            self.path,
            self.frameworkFile,
            self.mainStructureFile,
            boxData,
            tab.selectedRooms,
            config.getCreateTrendWidgets(),
            config.getRooms(),
            self
        )
        if mainStructureManagerObject.isEnable():
            mainStructureManagerObject.run()
            self.mainStructureName = mainStructureManagerObject.getName()
            print("Level created and saved in output folder")

        frameworkStructureObject = frameworkStructure.frameworkStructure(
            self.path,
            config.getStructureSchematicFramework(),
            config.getStructureSchematicLevel(),
            config.getStructureBoxData(),
            config.getStructureRoomNames(),
            self
        )
        if frameworkStructureObject.isEnable():
            frameworkStructureObject.run()
            self.frameworkName = frameworkStructureObject.getName()

    def crateWebManagement(self, login, password, ip):
        webManagementObject = webManagement.WebManagement(
            self.path,
            login,
            password,
            ip,
        )
        return webManagementObject

    # Getter for databaseManagerObject
    def getDatabaseObject(self):
        return self.databaseManagerObject

    def getTrendWidgetDictionary(self, roomNumber):
        if self.trendWidgetDictionary.get(roomNumber) is None:
            print("Room Number ", roomNumber, " Does not have corresponding trend widget that was created in this runtime")
            return ""
        return self.trendWidgetDictionary[roomNumber]

    def getInfoWidgetDictionary(self, roomNumber):
        if self.infoWidgetDictionary.get(roomNumber) is None:
            print("Room Number ", roomNumber, " Does not have corresponding info widget that was created in this runtime")
            return ""
        return self.infoWidgetDictionary[roomNumber]

    def getBoxesIDs(self):
        return self.boxesIDs

    def getBiggestWidgetID(self):
        return self.biggestWidgetID

    def newBiggestWidgetID(self, widgetType, room):
        self.biggestWidgetID += 1
        if widgetType == "trend":
            self.trendWidgetDictionary[room] = self.biggestWidgetID
        elif widgetType == "info":
            self.infoWidgetDictionary[room] = self.biggestWidgetID
        else:
            print("Something went very wrong, ID of widgets cannot be determined")
            exit(1)
        return self.biggestWidgetID

    def setBoxesIDs(self, ids):
        self.boxesIDs = ids

    # Getter for path
    def getPath(self):
        return self.path

    def createNewBoxDataTab(self, frame, item, name):
        self.boxDataTabs[item] = (guiBoxDataTab.GuiBoxDataTab(frame, self, self.tabStructure, self.guiUtilities, self.databaseManagerObject.getAllImages(), name))

    def updateImportedLevelStructure(self, file):
        file = file.name
        for tab in self.boxDataTabs:
            self.boxDataTabs[tab].updateImportedLevel(file)

    def updateImportedFrameworkStructure(self, file):
        file = file.name
        for tab in self.boxDataTabs:
            self.boxDataTabs[tab].updateImportedFramework(file)

    def addRoom(self, room):
        self.roomNumbers.append(room)
        for tab in self.boxDataTabs:
            self.boxDataTabs[tab].updateRoomNames(self.roomNumbers)

    def triesToSelectRooms(self, selectedItems):
        if self.tabControl.tab(self.tabControl.select(), "text") == "Framework & Level":
            boxName = self.TabStructure.tabControlBoxData.tab(self.TabStructure.tabControlBoxData.select(), "text")
            for tab in self.boxDataTabs:
                if self.boxDataTabs[tab].name == boxName:
                    self.boxDataTabs[tab].selectRooms(selectedItems)
        #for tab in self.boxDataTabs:
        #    self.boxDataTabs[tab].triesToSelectRooms()


if __name__ == '__main__':
    main = Main()
