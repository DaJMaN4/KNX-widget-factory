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
from levels import levelManager


# Get path of WidgetFactory folder
path = os.path.dirname(os.path.dirname(__file__))

# Check if folders exist, if not then create it
if not os.path.exists(path + "/output"):
    os.mkdir(path + "/output")
if not os.path.exists(path + "/schematics"):
    os.mkdir(path + "/schematics")
if not os.path.exists(path + "/import"):
    os.mkdir(path + "/import")
if not os.path.exists(path + "/data"):
    os.mkdir(path + "/data")
if not os.path.exists(path + "/database"):
    os.mkdir(path + "/database")

# Create object of DatabaseManager class
databaseManagerObject = databaseManager.DatabaseManager(path)
databaseManagerObject.unZipData()


# Runs everything
def run():
    # Create object of Config class
    config = ConfigManager.Config(path)

    # Create object of ImportManager class
    importManager = ImportWidgets.ImportManager(
        path,
        config.getRoomWidgetsObjectsNamesWidget()
    )
    # Run open function of ImportManager class
    importManager.open()

    if config.getCreateLevels():
        levelManagerObject = levelManager.LevelManager(
            path,
            config.getLevelsSchematicFramework(),
            config.getLevelsSchematicLevel(),
            config.getLevelsBoxData(),
            config.getLevelsRoomNames()
        )
        if levelManagerObject.isEnable():
            levelManagerObject.run()
            print("Level and framework created and saved in output folder")
        else:
            print("Level and framework creation disabled in config.yml")

    return
    # Create object of TrendWidgetFactory class
    if config.getCreateTrendWidgets():
        trendWidgetFactory = TrendWidgetFactory.TrendWidgetFactory(
            config.getRooms(),
            config.getTrendRoomWidgetsWidgetNameInFiles(),
            config.getTrendRoomWidgetsAddPrefixToWidgetName(),
            config.getTrendRoomWidgetsObjectsNamesWidget(),
            path,
            config.getTrendWidgetSchematicToUse()
        )
        # Run run function of TrendWidgetFactory class
        trendWidgetFactory.run()
        # If module is enabled then print message
        if trendWidgetFactory.isEnable():
            print("All trend widgets created and saved in output folder")

    # Create object of InfoWidgetFactory class
    if config.getCreateInfoRoomWidgets():
        infoWidgetFactory = InfoWidgetFactory.InfoWidgetFactory(
            config.getRooms(),
            config.getRoomWidgetsAddPrefixToWidgetName(),
            config.getWidgetName(),
            config.getRoomWidgetsAddPrefixToNameInFiles(),
            config.getRoomWidgetsWidgetNameInFiles(),
            config.getRoomWidgetsObjectsNamesWidget(),
            path,
            config.getRoomWidgetsSchematicToUse()
        )
        # Run run function of InfoWidgetFactory class
        infoWidgetFactory.run()
        # If module is enabled then print message
        if infoWidgetFactory.isEnable():
            print("All info widgets created and saved in output folder")


# Getter for databaseManagerObject
def getDatabaseObject():
    return databaseManagerObject


# Getter for path
def getPath():
    return path


# Run everything
if __name__ == '__main__':
    run()
