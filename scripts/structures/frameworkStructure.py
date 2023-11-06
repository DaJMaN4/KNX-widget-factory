import os
import tarfile
import scripts.main
from scripts.utils import importUtil

class frameworkStructure:
    def __init__(self, path, schematicNameFramework, schematicNameLevel, boxData, roomNames):
        self.schematicLevelData = None
        self.outPutDataLevel = None
        self.schematicFrameworkData = None
        self.importUtil = importUtil .ImportManager(path)
        self.path = path
        self.schematicNameFramework = schematicNameFramework
        self.schematicNameLevel = schematicNameLevel
        self.boxData = boxData
        self.roomNames = roomNames

    def importSchematics(self):
        self.importUtil.open("frameworks")
        self.importUtil.open("levels")

    def getData(self):
        self.schematicFrameworkData = self.importUtil.getData(self.schematicNameFramework, "frameworks")
        self.schematicFrameworkData = self.schematicFrameworkData["plan"]
        self.schematicLevelData = self.importUtil.getData(self.schematicNameLevel, "levels")
        self.outPutDataLevel = self.schematicLevelData
        self.schematicLevelData = self.schematicLevelData["plan"]

    # Returns if module is enabled or disabled
    def isEnable(self):
        return not self.disable

    # Run function is called from main class and it contains everything to run successfully the module
    def run(self):
        pass