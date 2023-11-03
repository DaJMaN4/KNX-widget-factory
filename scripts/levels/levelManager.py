import os
import yaml
from scripts import main
from scripts.utils import importUtil
import json
import tarfile
import io

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
        self.newObject = None
        self.namesLocations = {}
        self.boxesIDs = {}
        self.templateObjects = {}
        self.sizeOfBoxes = {}
        self.objectPlacements = {}
        self.outPutDataLevel = {}

    def importSchematics(self):
        self.importUtil.open("frameworks")
        self.importUtil.open("levels")

    def getData(self):
        self.schematicFrameworkData = self.importUtil.getData(self.schematicNameFramework, "frameworks")
        self.schematicFrameworkData = self.schematicFrameworkData["plan"]
        self.schematicLevelData = self.importUtil.getData(self.schematicNameLevel, "levels")
        self.outPutDataLevel = self.schematicLevelData
        self.schematicLevelData = self.schematicLevelData["plan"]


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
                                    self.templateObjects[box].append(obj)  # templates room databox from config.yml
        print("template", self.templateObjects)

    def getObjectsPlacement(self):
        table = main.getDatabaseObject().getTableColumns(["id", "name"], "objects")
        for row in table:
            ID = row[0]
            name = str(row[1])
            for roomTypes in self.roomNames:
                for roomName in self.roomNames[roomTypes]:
                    if roomName not in name:
                        continue
                    for obj in self.templateObjects:
                        if obj != roomName:
                            continue
                        for singleObjNum in range(len(self.templateObjects[obj])):
                            if singleObjNum == 0:
                                continue
                            if self.templateObjects[obj][singleObjNum].get("object") is None:
                                continue
                            if self.templateObjects[obj][singleObjNum]["object"] != ID:
                                continue
                            for objectName in self.boxData[roomTypes]["objectsNames"]:
                                if objectName not in name:
                                    continue
                                placementX = int(self.templateObjects[obj][singleObjNum]["locx"]) - self.boxesIDs[obj][3]
                                placementY = int(self.templateObjects[obj][singleObjNum]["locy"]) - self.boxesIDs[obj][2]
                                if self.objectPlacements.get(roomTypes) is None:
                                    self.objectPlacements[roomTypes] = [[objectName, placementY, placementX]]
                                else:
                                    self.objectPlacements[roomTypes].append([objectName, placementY, placementX])

        print(self.objectPlacements)

    def createObjects(self):
        for boxType in self.roomNames:
            for boxName in self.roomNames[boxType]:
                for boxTemplate in self.templateObjects:
                    if self.templateObjects[boxTemplate][0] != boxType:
                        continue
                    for singleObjNum in range(len(self.templateObjects[boxTemplate])):# good
                        if singleObjNum == 0:
                            continue
                        if self.templateObjects[boxTemplate][singleObjNum].get("object") is None:
                            continue
                        doneRoomObj = None
                        table = main.getDatabaseObject().getTableColumns(["id", "name"], "objects")
                        for row in table:
                            ID = row[0]
                            name = str(row[1])
                            if ID == self.templateObjects[boxTemplate][singleObjNum]["object"]:
                                #print(ID, "  ", self.templateObjects[boxTemplate][singleObjNum]["object"], "  " , name, "  ", boxTemplate, "  ", singleObjNum, "  ", boxType, "  ", boxName, "  ", name)
                                for roomObj in self.boxData[boxType]["objectsNames"]:
                                    if roomObj in name:
                                        if boxTemplate in name:
                                            doneRoomObj = roomObj
                                            break
                                else:
                                    continue
                                break
                        self.iteratingThroughObjects(boxType, boxName, boxTemplate, singleObjNum, doneRoomObj)


    # Has the same type of box and iterates through all objects in that box,
    # change id of object by finding the same name in database that corresponds to room and
    # object name sample in config.yml

    def iteratingThroughObjects(self, boxType, boxName, boxTemplate, singleObjNum, objName):
        table = main.getDatabaseObject().getTableColumns(["id", "name"], "objects")
        for row in table:
            ID = row[0]
            name = str(row[1])
            if boxName not in name:
                continue

            if objName not in name:
                continue

            newObject = self.templateObjects[boxTemplate][singleObjNum].copy()

            newObject["object"] = ID
            newObject["statusobject"] = ID
            for placement in self.objectPlacements[boxType]:
                if placement[0] == objName:
                    newObject["locx"] = self.boxesIDs[boxName][3] + placement[2]
                    newObject["locy"] = self.boxesIDs[boxName][2] + placement[1]
                    print("assignesd", newObject["locx"], "  ", newObject["locy"], "  ", boxName, "  ", objName)
                    break
            self.outPutDataLevel["plan"]["objects"].append(newObject)

            #print(self.outPutDataLevel)

            #newObject["statusobject"] = ID
                #print(boxType, "  ", boxName, "  ", boxTemplate, "  ", name, "  ", self.templateObjects[boxTemplate][singleObjNum])
                #template = self.templateObjects[boxTemplate]
                #template["object"] = ID
                #template["statusobject"] = ID

    def saveLevel(self):
        json_object = json.dumps(self.outPutDataLevel, indent=4)

        # Create tar file with name Trend_Widget_Rom-<room number>.tar
        file = tarfile.open(self.path + "/" + "output/widgets/Trend_Widget_Rom-" + "bla" + ".tar", "w", None,
                            tarfile.GNU_FORMAT)

        # Create file inside tar file called "."
        dir_info = tarfile.TarInfo(name='.')
        # Set type to directory
        dir_info.type = tarfile.DIRTYPE

        # Get the content of json_object and transform it to bytes
        file_contents = io.BytesIO(json_object.encode())
        # Create file inside tar file called data.json
        file_info = tarfile.TarInfo(name='./data.json')
        # Set size of file to length of file contents
        file_info.size = len(file_contents.getvalue())
        # Add file to tar file
        file.addfile(tarinfo=file_info, fileobj=file_contents)

        # Close and save tar file
        file.close()



    def isEnable(self):
        return self.isEnabled

    def run(self):
        self.importSchematics()
        self.getData()
        self.getNamesLocations()
        self.getBoxesIDs()
        self.getObjectsFromTemplates()
        self.getObjectsPlacement()
        self.createObjects()
        self.saveLevel()
