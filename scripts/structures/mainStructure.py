from scripts.utils import importUtil
import json
import tarfile
import io


class mainStructureManager:
    def __init__(self, path, schematicNameFramework, schematicNameLevel, boxData, roomNames, doCreateTrend, activeRooms,
                 main):
        self.importUtil = importUtil.ImportManager(path)
        self.path = path
        self.schematicNameFramework = schematicNameFramework
        self.schematicNameLevel = schematicNameLevel
        self.boxData = boxData
        self.roomNames = roomNames
        self.doCreateTrend = doCreateTrend
        self.activeRooms = activeRooms
        self.main = main
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
        self.IDsOfObjectsInTemplates = {}

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
                for roomType in self.roomNames:
                    for roomNum in self.roomNames[roomType]:
                        if roomNum == obj["name"]:
                            self.namesLocations[obj["name"]] = [obj["locx"], obj["locy"], roomType]

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
        for obj in self.schematicLevelData["objects"]:  # get objects from level
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

                            if self.IDsOfObjectsInTemplates.get(box) is None:
                                self.IDsOfObjectsInTemplates[box] = [boxType, obj["id"]]
                            else:
                                self.IDsOfObjectsInTemplates[box].append(obj["id"])

    def getObjectsPlacement(self):
        table = self.main.getDatabaseObject().getTableColumns(["id", "name"], "objects")
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

                                placementX = int(self.templateObjects[obj][singleObjNum]["locx"]) - self.boxesIDs[obj][
                                    3]
                                placementY = int(self.templateObjects[obj][singleObjNum]["locy"]) - self.boxesIDs[obj][
                                    2]
                                objectID = int(self.templateObjects[obj][singleObjNum]["id"])
                                if self.objectPlacements.get(roomTypes) is None:
                                    self.objectPlacements[roomTypes] = [[objectName, placementY, placementX, objectID]]
                                else:
                                    self.objectPlacements[roomTypes].append(
                                        [objectName, placementY, placementX, objectID])

    def getObjectsPlacementForClearObjects(self):
        table = self.main.getDatabaseObject().getTableColumns(["id"], "visobjects")
        for row in table:
            ID = row[0]

            for placement in self.objectPlacements:
                for index in range(len(self.objectPlacements[placement])):
                    if ID == self.objectPlacements[placement][index][3]:
                        break
                else:
                    continue
                break
            else:
                for objectTemplateID in self.IDsOfObjectsInTemplates:
                    for templateID in self.IDsOfObjectsInTemplates[objectTemplateID]:

                        if templateID != ID:
                            continue

                        for obj in self.templateObjects:
                            for singleObjNum in range(len(self.templateObjects[obj])):
                                if singleObjNum == 0:
                                    continue

                                if self.templateObjects[obj][singleObjNum].get("id") == ID:
                                    for nameObject in self.namesLocations:
                                        if (self.namesLocations[nameObject][0] ==
                                                self.templateObjects[obj][singleObjNum]["locx"] and
                                                self.namesLocations[nameObject][1] ==
                                                self.templateObjects[obj][singleObjNum]["locy"]):
                                            break
                                    else:
                                        placementX = int(self.templateObjects[obj][singleObjNum]["locx"]) - \
                                                     self.boxesIDs[obj][3]
                                        placementY = int(self.templateObjects[obj][singleObjNum]["locy"]) - \
                                                     self.boxesIDs[obj][2]

                                        for roomTypes in self.roomNames:
                                            for roomName in self.roomNames[roomTypes]:
                                                if roomName == obj:
                                                    self.objectPlacements[roomTypes].append(
                                                        ["custom", placementY, placementX, ID, roomName])

    def createObjects(self):
        for boxType in self.roomNames:
            for boxName in self.roomNames[boxType]:
                for boxTemplate in self.templateObjects:
                    for singleObjNum in range(len(self.templateObjects[boxTemplate])):  # good
                        if singleObjNum == 0:
                            continue
                        if self.templateObjects[boxTemplate][singleObjNum].get("object") is None or \
                                self.templateObjects[boxTemplate][0] != boxType:
                            for nameLocation in self.namesLocations:
                                if (self.namesLocations[nameLocation][0] ==
                                        self.templateObjects[boxTemplate][singleObjNum]["locx"] and
                                        self.namesLocations[nameLocation][1] ==
                                        self.templateObjects[boxTemplate][singleObjNum]["locy"]):
                                    break
                            else:
                                pass

                            continue
                        doneRoomObj = None

                        table = self.main.getDatabaseObject().getTableColumns(["id", "name"], "objects")
                        for row in table:
                            ID = row[0]
                            name = str(row[1])
                            if ID == self.templateObjects[boxTemplate][singleObjNum]["object"]:

                                for roomObj in self.boxData[boxType]["objectsNames"]:
                                    if roomObj in name:
                                        if boxTemplate in name:
                                            doneRoomObj = roomObj
                                            break
                                else:
                                    continue
                                break

                        if doneRoomObj is None:
                            newObject = self.templateObjects[boxTemplate][singleObjNum].copy()

                            for placement in self.objectPlacements[boxType]:
                                if newObject["id"] == placement[3]:
                                    newObject["locx"] = self.boxesIDs[boxName][3] + placement[2]
                                    newObject["locy"] = self.boxesIDs[boxName][2] + placement[1]

                                    if self.boxData[boxType].get("trendIcon") is not None and \
                                            self.boxData[boxType].get("trendIcon") != "" and \
                                            self.doCreateTrend:

                                        for room in self.activeRooms:
                                            if room == boxName:
                                                break
                                        else:
                                            continue

                                        paramsDict = newObject["params"].replace("\\", "")
                                        paramsDict = json.loads(paramsDict)

                                        if paramsDict["icon_default"] == self.boxData[boxType]["trendIcon"]:
                                            paramsDict["widget"] = self.main.getTrendWidgetDictionary(boxName)
                                            paramsDict = str(paramsDict)
                                            paramsDict = paramsDict.replace("'", '"')
                                            paramsDict = paramsDict.replace(" ", "")
                                            paramsDict = paramsDict.replace("False", "false")
                                            paramsDict = paramsDict.replace("True", "true")
                                            paramsDict = paramsDict.replace("None", "null")
                                            newObject["params"] = paramsDict

                            self.outPutDataLevel["plan"]["objects"].append(newObject)
                            continue

                        self.iteratingThroughObjects(boxType, boxName, boxTemplate, singleObjNum, doneRoomObj)

    def iteratingThroughObjects(self, boxType, boxName, boxTemplate, singleObjNum, objName):
        table = self.main.getDatabaseObject().getTableColumns(["id", "name"], "objects")
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
                    break
            self.outPutDataLevel["plan"]["objects"].append(newObject)

    def changeRoomNamesPlace(self):
        placements = {}
        for obj in self.schematicLevelData["objects"]:
            if obj.get("name") is not None:
                for template in self.templateObjects:
                    if template == obj["name"]:
                        if template == self.boxData[self.templateObjects[template][0]]["template"]:
                            placements[template] = \
                                [int(self.namesLocations[template][0]) - self.boxesIDs[template][3],
                                 int(self.namesLocations[template][1]) - self.boxesIDs[template][2]]

        for obj in self.outPutDataLevel["plan"]["objects"]:
            if obj.get("name") is not None:
                for name in self.namesLocations:
                    if name == obj["name"]:
                        for placementsType in placements:
                            if self.namesLocations[placementsType][2] == self.namesLocations[name][2]:
                                obj["locx"] = placements[placementsType][0] + self.boxesIDs[name][3]
                                obj["locy"] = placements[placementsType][1] + self.boxesIDs[name][2]
                                break

    def saveLevel(self):
        json_object = json.dumps(self.outPutDataLevel, indent=4)

        # Create tar file with name Trend_Widget_Rom-<room number>.tar
        file = tarfile.open(self.path + "/" + "output/levels/" + self.schematicNameLevel.replace(".yml", ".tar"),
                            "w", None, tarfile.GNU_FORMAT)

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

    def getName(self):
        return self.schematicNameLevel.replace(".tar", ".yml")

    def run(self):
        self.importSchematics()
        self.getData()
        self.getNamesLocations()
        self.getBoxesIDs()
        self.getObjectsFromTemplates()
        self.getObjectsPlacement()
        self.getObjectsPlacementForClearObjects()
        self.createObjects()
        self.changeRoomNamesPlace()
        self.saveLevel()
        self.main.setBoxesIDs(self.boxesIDs)
