import os
import yaml
from scripts import main
from scripts.utils import importUtil
import json


class LevelManager:
    def __init__(self, path, schematicNameFramework, schematicNameLevel, boxData, roomNames):
        self.importUtil = importUtil.ImportManager(path)
        self.path = path
        self.schematicNameFramework = schematicNameFramework
        self.schematicNameLevel = schematicNameLevel
        self.boxData = boxData
        self.roomNames = roomNames
        self.isEnabled = True
        self.schematicFrameworkData = None
        self.schematicLevelData = None
        self.namesLocations = {}
        self.boxesIDs = {}
        self.templateObjects = {}
        self.sizeOfBoxes = {}

    def importSchematics(self):
        self.importUtil.open("frameworks")
        self.importUtil.open("levels")

    def getData(self):
        self.schematicFrameworkData = self.importUtil.getData(self.schematicNameFramework, "frameworks")["plan"]
        self.schematicLevelData = self.importUtil.getData(self.schematicNameLevel, "levels")["plan"]

    def getNamesLocations(self):
        for obj in self.schematicLevelData["objects"]:
            if obj.get("name") is not None:
                for type in self.roomNames:
                    for roomNum in self.roomNames[type]:
                        if roomNum == obj["name"]:
                            self.namesLocations[obj["name"]] = [obj["locx"], obj["locy"], type]

    def getBoxesIDs(self):
        for obj in self.schematicFrameworkData["objects"]:
            if obj.get("params") is not None:
                paramsDict = obj["params"].replace("\\", "")
                paramsDict = json.loads(paramsDict)
                for boxType in self.boxData:
                    if self.boxData[boxType]["normal"] == paramsDict.get("icon_default"):
                        if paramsDict.get("width") is not None and paramsDict.get("height") is not None:
                            width = int(paramsDict["width"])
                            height = int(paramsDict["height"])
                            locationBoxX = obj["locx"]
                            locationBoxY = obj["locy"]
                            combinedX = width + locationBoxX
                            combinedY = height + locationBoxY
                            if self.sizeOfBoxes.get(boxType) is None:
                                self.sizeOfBoxes[boxType] = [width, height]
                            for nameLocation in self.namesLocations:
                                locationNameX = self.namesLocations[nameLocation][0]
                                locationNameY = self.namesLocations[nameLocation][1]
                                if combinedX >= locationNameX >= locationBoxX and combinedY >= locationNameY >= locationBoxY:
                                    self.boxesIDs[nameLocation] = [obj["id"], boxType, locationBoxY, locationBoxX]

    def getObjectsFromTemplates(self):
        for obj in self.schematicLevelData["objects"]:
            if obj.get("object") is not None and obj.get("statusobject") is not None:
                for boxType in self.boxData:
                    for box in self.boxesIDs:
                        if self.boxesIDs.get(box)[0] == self.boxesIDs.get(self.boxData[boxType].get("template"))[0]:
                            width = self.sizeOfBoxes.get(boxType)[0]
                            height = self.sizeOfBoxes.get(boxType)[1]
                            locationBoxX = self.boxesIDs.get(box)[3]
                            locationBoxY = self.boxesIDs.get(box)[2]
                            combinedX = width + locationBoxX
                            combinedY = height + locationBoxY
                            locationObjX = obj["locx"]
                            locationObjY = obj["locy"]
                            if combinedX >= locationObjX >= locationBoxX and combinedY >= locationObjY >= locationBoxY:
                                if self.templateObjects.get(box) is None:
                                    self.templateObjects[box] = [boxType, obj]
                                else:
                                    self.templateObjects[box].append(obj)

    def createObjects(self):
        for boxType in self.roomNames:
            for boxName in self.roomNames[boxType]:
                for boxTemplate in self.templateObjects:
                    if self.templateObjects[boxTemplate][0] == boxType:
                        #for obj in self.templateObjects[boxTemplate]:

                        #self.schematicLevelData["objects"].append(self.templateObjects[boxTemplate])
                        self.iteratingThroughObjects( boxType, boxName, boxTemplate)

    # Has the same type of box and iterates through all objects in that box,
    # change id of object by finding the same name in database that corresponds to room and
    # object name sample in config.yml

    def gettingDataFromTemplates(self):
        for obj in self.boxData:
            template = self.boxData[obj].get("template")
            table = main.getDatabaseObject().getTableColumns(["id", "name"], "objects")
            for row in table:
                ID = row[0]
                name = str(row[1])
                if template in name:
                    print("woo ", name, " ", ID)


    def iteratingThroughObjects(self, boxType, boxName, boxTemplate):
        table = main.getDatabaseObject().getTableColumns(["id", "name"], "objects")
        for row in table:
            ID = row[0]
            name = str(row[1])
            if boxName in name:
                for objectName in self.boxData[boxType]["objectsNames"]:
                    if objectName in name:
                        #print("Found object " + name + " in database " + objectName + " with id " + str(ID))
                        #obj["object"] = ID
                        #obj["statusobject"] = ID
                        pass

    def isEnable(self):
        return self.isEnabled

    def run(self):
        self.importSchematics()
        self.getData()
        self.getNamesLocations()
        self.getBoxesIDs()
        self.getObjectsFromTemplates()
        self.createObjects()
        self.gettingDataFromTemplates()
