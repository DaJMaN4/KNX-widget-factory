import io
import tarfile
from scripts.utils import importUtil
import json


class frameworkStructure:
    def __init__(self, path, schematicFileFramework, schematicFileLevel, boxData, roomNames, main):
        self.schematicFrameworkData = None
        self.disable = False
        self.importUtil = importUtil .ImportManager(path)
        self.path = path
        self.schematicFileFramework = schematicFileFramework
        self.schematicFileLevel = schematicFileLevel
        self.boxData = boxData
        self.roomNames = roomNames
        self.main = main
        self.boxesIDs = self.main.getBoxesIDs()
        self.boxObjects = {}
        self.boxParameters = {}
        if self.boxesIDs is None:
            self.main.log("Boxes IDs are not loaded, this might make the whole application not functioning. Disabling Framework Structure module.")
            self.disable = True
            return

        self.schematicNameFramework = self.schematicFileFramework.split("/")[-1]
        self.schematicNameLevel = self.schematicFileLevel.split("/")[-1]

    def importSchematics(self):
        self.importUtil.open(self.schematicFileFramework, "frameworks")
        self.importUtil.open(self.schematicFileLevel, "levels")

    def getData(self):
        self.schematicFrameworkData = self.importUtil.getData(self.schematicNameFramework, "frameworks")
        self.schematicFrameworkData = self.schematicFrameworkData["plan"]

    def findBoxObjects(self):
        table = self.main.getDatabaseObject().getTableColumns(["id", "name"], "objects")
        for row in table:
            ID = row[0]
            name = str(row[1])
            if "Farge boks" not in name:
                continue

            for box in self.boxesIDs:
                if box in name:
                    self.boxObjects[box] = ID

    def createParameters(self):
        for template in self.boxData:
            for box in self.schematicFrameworkData["objects"]:
                for boxObj in self.boxesIDs:
                    if boxObj == self.boxData[template]["template"]:
                        if box["id"] == self.boxesIDs[boxObj][0]:
                            paramsDict = box["params"]#.replace("\\", "")
                            paramsDict = json.loads(paramsDict)
                            self.boxParameters[boxObj] = paramsDict["icons_add"]

    def addObjectToBox(self):
        for box in self.schematicFrameworkData["objects"]:
            for boxObj in self.boxesIDs:
                if box["id"] == self.boxesIDs[boxObj][0]:
                    for roomType in self.roomNames:
                        for roomNumber in self.roomNames[roomType]:
                            if roomNumber == boxObj:
                                paramsDict = box["params"]
                                paramsDict = json.loads(paramsDict)
                                paramsDict["icons_add"] = self.boxParameters[self.boxData[roomType]["template"]]
                                paramsDict["widget"] = self.main.getInfoWidgetDictionary(roomNumber)
                                paramsDict = str(paramsDict)
                                paramsDict = paramsDict.replace("'", '"')
                                paramsDict = paramsDict.replace(" ", "")
                                paramsDict = paramsDict.replace("False", "false")
                                paramsDict = paramsDict.replace("True", "true")
                                paramsDict = paramsDict.replace("None", "null")
                                box["params"] = paramsDict
                                box["object"] = self.boxObjects[boxObj]
                                box["statusobject"] = self.boxObjects[boxObj]

    def saveFramework(self):
        self.schematicFrameworkData = {"plan": self.schematicFrameworkData}
        json_object = json.dumps(self.schematicFrameworkData, indent=4)

        # Create tar file with name Trend_Widget_Rom-<room number>.tar
        file = tarfile.open(self.path + "/" + "output/frameworks/" + self.schematicNameFramework.replace(".yml", ".tar"),
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

    # Returns if module is enabled or disabled
    def isEnable(self):
        return not self.disable

    def getName(self):
        return self.schematicNameFramework.replace(".yml", ".tar")

    # Run function is called from main class and it contains everything to run successfully the module
    def run(self):
        self.importSchematics()
        self.getData()
        self.findBoxObjects()
        self.createParameters()
        self.addObjectToBox()
        self.saveFramework()

