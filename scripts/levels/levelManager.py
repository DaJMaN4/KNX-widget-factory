import os
import yaml
from scripts import main
from scripts.utils import importUtil

class LevelManager:
    def __init__(self, path, schematicNameFramework, schematicNameLevel, boxData, roomNames):
        self.importUtil = None
        self.path = path
        self.schematicNameFramework = schematicNameFramework
        self.schematicNameLevel = schematicNameLevel
        self.boxData = boxData
        self.roomNames = roomNames
        self.importSchematics()
        self.isEnabled = True
        self.run()

    def importSchematics(self):
        self.importUtil = importUtil.ImportManager(self.path)
        self.schematicNameFramework = self.importUtil.open("frameworks")
        self.schematicNameLevel = self.importUtil.open("levels")
        print(self.schematicNameFramework)

    def getData(self):
        pass

    def getBoxesIDs(self):
        pass

    def getFrameworkSchematic(self):
        importUtil.ImportManager.getData("frameworks", self.schematicNameFramework)

    def getLevelSchematic(self):
        pass

    def isEnable(self):
        return self.isEnabled

    def run(self):
        pass
