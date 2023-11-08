import os
import pip

# Check if yaml module is installed, if not then install it
try:
    import yaml
except ImportError:
    print("Trying to Install required module: pyyaml\n")
    pip.main(['install', "pyyaml"])
    import yaml

import ConfigManager, databaseManager
from widgets import ImportWidgets, InfoWidgetFactory, TrendWidgetFactory
from structures import mainStructure, frameworkStructure


class Main:
    def __init__(self):
        self.trendWidgetDictionary = {}
        self.infoWidgetDictionary = {}
        self.boxesIDs = None
        # Get path of WidgetFactory folder
        self.path = os.path.dirname(os.path.dirname(__file__))

        # Create object of DatabaseManager class
        self.databaseManagerObject = databaseManager.DatabaseManager(self.path)
        self.databaseManagerObject.unZipData()

        self.biggestWidgetID = self.databaseManagerObject.getBiggestWidgetID()

    # Runs everything
    def run(self):
        # Create object of Config class
        config = ConfigManager.Config(self.path)

        # Create object of ImportManager class
        importManager = ImportWidgets.ImportManager(
            self.path,
            config.getRoomWidgetsObjectsNamesWidget(),
            main
        )
        # Run open function of ImportManager class
        importManager.open()

        # Create object of TrendWidgetFactory class
        if config.getCreateTrendWidgets():
            trendWidgetFactory = TrendWidgetFactory.TrendWidgetFactory(
                config.getRooms(),
                config.getTrendRoomWidgetsWidgetNameInFiles(),
                config.getTrendRoomWidgetsAddPrefixToWidgetName(),
                config.getTrendRoomWidgetsObjectsNamesWidget(),
                self.path,
                config.getTrendWidgetSchematicToUse(),
                self
            )
            # Run run function of TrendWidgetFactory class
            trendWidgetFactory.run()
            # If module is enabled then print message
            if trendWidgetFactory.isEnable():
                pass
                # print("All trend widgets created and saved in output folder")

        if config.getCreateStructures():
            mainStructureManagerObject = mainStructure.mainStructureManager(
                self.path,
                config.getStructureSchematicFramework(),
                config.getStructureSchematicLevel(),
                config.getStructureBoxData(),
                config.getStructureRoomNames(),
                config.getCreateTrendWidgets(),
                self
            )
            if mainStructureManagerObject.isEnable():
                mainStructureManagerObject.run()
                pass
                # print("Level and framework created and saved in output folder")
            else:
                pass
                # print("Level and framework creation disabled in config.yml")

        frameworkStructureObject = frameworkStructure.frameworkStructure(
            self.path,
            config.getStructureSchematicFramework(),
            config.getStructureSchematicLevel(),
            config.getStructureBoxData(),
            config.getStructureRoomNames(),
            self
        )
        frameworkStructureObject.run()

        # Create object of InfoWidgetFactory class
        if config.getCreateInfoRoomWidgets():
            infoWidgetFactory = InfoWidgetFactory.InfoWidgetFactory(
                config.getRooms(),
                config.getRoomWidgetsAddPrefixToWidgetName(),
                config.getWidgetName(),
                config.getRoomWidgetsAddPrefixToNameInFiles(),
                config.getRoomWidgetsWidgetNameInFiles(),
                config.getRoomWidgetsObjectsNamesWidget(),
                self.path,
                config.getRoomWidgetsSchematicToUse(),
                self
            )
            # Run run function of InfoWidgetFactory class
            infoWidgetFactory.run()
            # If module is enabled then print message
            if infoWidgetFactory.isEnable():
                print("All info widgets created and saved in output folder")
        print("saawdawdawdawdadawdwafafwaga")
        print(self.biggestWidgetID, " ", self.trendWidgetDictionary, " ", self.infoWidgetDictionary)

        # global infoWidgetDictionary, trendWidgetDictionary, biggestWidgetID

    # Getter for databaseManagerObject
    def getDatabaseObject(self):
        return self.databaseManagerObject

    def getTrendWidgetDictionary(self, roomNumber):
        if self.trendWidgetDictionary.get(roomNumber) is None:
            print("Room Number ", roomNumber, " Does not have corresponding widget that was created in this runtime")
            return ""
        return self.trendWidgetDictionary[roomNumber]

    def getInfoWidgetDictionary(self, roomNumber):
        if self.infoWidgetDictionary.get(roomNumber) is None:
            print("Room Number ", roomNumber, " Does not have corresponding widget that was created in this runtime")
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
            print("Something went very wrong, it cannot be determined what ID of widgets are")
            exit(1)
        print(self.biggestWidgetID, " ", self.trendWidgetDictionary, " ", self.infoWidgetDictionary)
        return self.biggestWidgetID

    def setBoxesIDs(self, ids):
        self.boxesIDs = ids

    # Getter for path
    def getPath(self):
        return self.path


if __name__ == '__main__':
    main = Main()
    main.run()



