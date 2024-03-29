import io
import json
import tarfile
import yaml
import os
import main


class InfoWidgetFactory:
    # Initialize TrendWidgetFactory class it sets all variables when creating the object in main class
    def __init__(self, roms, addPrefixToName, widgetName, addPrefixToWidgetNameInFiles, widgetNameInFiles,
                 objectsNames, path, schematicName):
        self.roms = roms
        self.addPrefixToName = addPrefixToName
        self.widgetName = widgetName
        self.addPrefixToWidgetNameInFiles = addPrefixToWidgetNameInFiles
        self.widgetNameInFiles = widgetNameInFiles
        self.objectsNames = objectsNames
        self.path = path
        self.schematicName = schematicName
        self.disable = False
        self.dictionary = None
        # Check if file exists in schematics folder by running method of this class
        self.checkIfFileExists()
        self.theWord = ""
        # Check if room number is with word or not, writes it to a boolean variable and sets
        # the words in a separate variable
        if roms[0].isdigit():
            self.isWithWord = False
        else:
            self.isWithWord = True
            for s in roms[0]:
                if s.isdigit():
                    break
                self.theWord += s

    # Checks if file exists in schematics folder
    def checkIfFileExists(self):
        # Goes through all files in schematics folder
        for schematicFile in os.listdir(self.path + "/schematics"):
            # If file with the same name as defined in config.yml
            if schematicFile == self.schematicName:
                # Open file as "r" which means read only. "file" is a variable name of opened file
                with open(self.path + "/schematics/" + schematicFile, 'r') as file:
                    # Load yaml file to dictionary variable
                    self.dictionary = yaml.safe_load(file)
                    # Close loop and end function
                    break
        # Runs if for didn't encounter break which means that file doesn't exist
        else:
            # Print error message and disable InfoWidget module
            print("File ", self.schematicName, " doesn't exists. Disabling InfoWidget module")
            self.disable = True

    # Returns if module is enabled or disabled
    def isEnable(self):
        return not self.disable

    # Run function is called from main class and it contains everything to run successfully the module
    def run(self):
        # If module is disabled then return
        if self.disable:
            return
        # Get from table in database called "objects" id and name of all objects
        table = main.getDatabaseObject().getTableColumns(["id", "name"], "objects")
        valid = {}
        # Goes through all rows in table
        for row in table:
            # Get id and name from row
            ID = row[0]
            name = str(row[1])
            # Goes through all room names
            for romName in self.roms:
                # If room name is in name of object in current row
                if romName in name:
                    # Goes through all object names
                    for objectName in self.objectsNames:
                        # If object name is in name of object in current row
                        if objectName in name:
                            # If room name is already in dictionary
                            if valid.get(romName) is not None:
                                # Append object name, ID and name to it
                                valid[romName].append([objectName, ID, name])
                            # If room name isn't in dictionary
                            else:
                                # Create Array for current room name and append object name, ID and name to it
                                valid[romName] = [[objectName, ID, name]]

        if valid == {}:
            print("\033[93mNo objects with specified name in confi.yml were found in database\033[0m")
            exit(1)

        # Goes through all room names
        for key in valid:
            # Get all objects from
            Objs = valid.get(key)

            # Replace placeholders in file with room number
            if self.addPrefixToName:
                widgetNameAdd = self.widgetNameInFiles.replace("%romName%", key)
            else:
                keyWithoutWord = key.replace(self.theWord, "")
                widgetNameAdd = self.widgetNameInFiles.replace("%romName%", keyWithoutWord)

            if self.addPrefixToWidgetNameInFiles:
                roomNameWidget = self.widgetName.replace("%romName%", key)
            else:
                keyWithoutWord = key.replace(self.theWord, "")
                roomNameWidget = self.widgetName.replace("%romName%", keyWithoutWord)

            # Goes through all objects in dictionary with current room name
            for obj in self.dictionary["plan"]["objects"]:
                # Goes through all object names defined in config.yml
                for desiredObj in self.objectsNames:
                    # If object name is not None
                    if obj.get("object") is not None:
                        # If object name is in name of object in current row
                        if obj["object"] == desiredObj:
                            # Goes through all objects in dictionary with current room name
                            for objectValid in Objs:
                                # If object name is in name of object in current row
                                if desiredObj in objectValid[0]:
                                    # Replace placeholders in file with object name, ID and
                                    obj["object"] = objectValid[1]
                                    obj["statusobject"] = objectValid[1]
                # Get name of object
                objName = obj.get("name")
                # If name of object is not None
                if objName is not None:
                    # Make name of object lowercase
                    objName = objName.lower()
                    # If name of object is "rom" or "room"
                    if objName == "rom" or objName == "room":
                        # Replace placeholders in file with room number
                        obj["name"] = roomNameWidget

            # Replace placeholders in file with room number
            self.dictionary["plan"]["name"] = widgetNameAdd

            # Transform dictionary to json object
            json_object = json.dumps(self.dictionary, indent=4)

            # Create tar file
            file = tarfile.open(self.path + "/" + "output/Info_Widget_Rom-" + key + ".tar", "w", None,
                                tarfile.GNU_FORMAT)

            # Create file inside tar file called "."
            dir_info = tarfile.TarInfo(name='.')
            # Set type to directory
            dir_info.type = tarfile.DIRTYPE

            # Get content of json_object and transform it to bytes
            file_contents = io.BytesIO(json_object.encode())
            # Create file inside tar file called data.json
            file_info = tarfile.TarInfo(name='./data.json')
            # Set size of file to length of file contents
            file_info.size = len(file_contents.getvalue())
            # Add file to tar file
            file.addfile(tarinfo=file_info, fileobj=file_contents)

            # Close and save tar file
            file.close()

            print("Info_Widget_Rom-" + key + ".tar created")
