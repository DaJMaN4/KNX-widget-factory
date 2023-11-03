import os
import yaml


class Config:
    # Initialize Config class, runs when object of this class is created
    # it connects and load to config.yml file
    def __init__(self, path):
        self.path = path
        # Check if config.yml exists
        if os.path.exists(self.path + "/config.yml"):
            # Open config.yml as "r" which means read only. "file" is a variable name of opened file
            with open(self.path + "/config.yml", 'r') as file:
                # Load yaml file to prime_service variable
                self.prime_service = yaml.safe_load(file)
        # If config.yml doesn't exists
        else:
            # Print error message and exit program
            print("config.yaml not found")
            exit(1)

    # Getters for all variables in config.yml

    def getRooms(self):
        return self.prime_service['rooms']

    def getCreateInfoRoomWidgets(self):
        return self.prime_service['createInfoRoomWidgets']

    def getWidgetName(self):
        return self.prime_service['roomWidgets']['widgetName']

    def getRoomWidgetsAddPrefixToWidgetName(self):
        return self.prime_service['roomWidgets']['addPrefixToWidgetName']

    def getRoomWidgetsWidgetNameInFiles(self):
        return self.prime_service['roomWidgets']['widgetNameInFiles']

    def getRoomWidgetsAddPrefixToNameInFiles(self):
        return self.prime_service['roomWidgets']['addPrefixToWidgetNameInFiles']

    def getRoomWidgetsSchematicToUse(self):
        return self.prime_service['roomWidgets']['schematicToUse']

    def getRoomWidgetsObjectsNamesWidget(self):
        return self.prime_service['roomWidgets']['objectsNamesWidget']

    def getCreateTrendWidgets(self):
        return bool(self.prime_service['createTrendWidgets'])

    def getTrendRoomWidgetsWidgetNameInFiles(self):
        return self.prime_service['trendWidgets']['widgetNameInFiles']

    def getTrendRoomWidgetsAddPrefixToWidgetName(self):
        return self.prime_service['trendWidgets']['addPrefixToWidgetName']

    def getTrendWidgetSchematicToUse(self):
        return self.prime_service['trendWidgets']['schematicToUse']

    def getTrendRoomWidgetsObjectsNamesWidget(self):
        return self.prime_service['trendWidgets']['objectsNamesWidget']

    def getCreateStructures(self):
        return bool(self.prime_service['createStructures'])

    def getStructureSchematicLevel(self):
        return self.prime_service['structure']['schematicLevel']

    def getStructureSchematicFramework(self):
        return self.prime_service['structure']['schematicFramework']

    def getStructureBoxData(self):
        return self.prime_service['structure']['boxData']

    def getStructureRoomNames(self):
        return self.prime_service['structure']['roomNames']
