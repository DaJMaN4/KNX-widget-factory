import io
import json
import tarfile
import yaml
import os
from scripts import main

class TrendWidgetFactory:
    # Initialize TrendWidgetFactory class it sets all variables when creating the object in the main class
    def __init__(self, roomNumber, widgetName, addPrefix, objectsNames, path, schematicName):
        self.dictionary = None
        self.prime_service = None
        self.roomNumber = roomNumber
        self.widgetName = widgetName
        self.addPrefix = addPrefix
        self.objectsNames = objectsNames
        self.path = path
        self.schematicName = schematicName
        self.disable = False
        # Check if room number is with word or not and writes it to a boolean variable
        # Room with word is something like A2001 and room without word is 2001
        self.theWord = ""
        if roomNumber[0].isdigit():
            self.isWithWord = False
        else:
            self.isWithWord = True
            for s in roomNumber[0]:
                if s.isdigit():
                    break
                self.theWord += s
        self.checkIfFileExists()

    # Check if file exists in schematics folder
    def checkIfFileExists(self):
        onlyOne = False
        if len(os.listdir(self.path + "/schematics/widgets/info")) == 1:
            onlyOne = True
        # Goes through all files in schematics folder
        for schematicFile in os.listdir(self.path + "/schematics/widgets/trends"):
            # If file with the same name as defined in config.yml
            if schematicFile == self.schematicName or onlyOne or self.schematicName == "":
                # Open file as "r" which means read only. "file" is a variable name of opened file
                with open(self.path + "/schematics/widgets/trends/" + schematicFile, 'r') as file:
                    # Load yaml file to dictionary variable
                    self.dictionary = yaml.safe_load(file)
                    # Close loop and end function
                    break
        # Runs if for didn't encounter break which means that file doesn't exist
        else:
            # Print error message and disable TrendWidget module
            print("File ", self.schematicName, " doesn't exists. Disabling TrendWidget module")
            self.disable = True

    # Returns if module is enabled or disabled
    def isEnable(self):
        return not self.disable

    # Run function is called from main class and it contains everything to run successfully the module
    def run(self):
        # If module is disabled then return
        global oldKey
        if self.disable:
            return
        table = main.getDatabaseObject().getTableColumns(["id", "name"], "objects")
        # Create empty dictionary
        valid = {}
        # Go through all rows in table
        for row in table:
            # Get id and name from row
            ID = row[0]
            name = str(row[1])
            # Go through all room numbers defined in config.yml
            for romName in self.roomNumber:
                # If room number is in name of object in current row
                if romName in name:
                    # Go through all object names defined in config.yml
                    for objectName in self.objectsNames:
                        # If object name is in name of object in current row
                        if objectName in name:
                            # If room number is already in dictionary then append object name, ID and name to it
                            if valid.get(romName) is not None:
                                valid[romName].append([ID, name])
                            # If room number is not in dictionary then create Array for current room number and
                            # add object name and ID to it
                            else:
                                valid[romName] = [[ID, name]]

        # Get from table in database called "trends" id, name and category of all trends
        table = main.getDatabaseObject().getTableColumns(["id", "category"], "trends")
        # Create empty dictionary
        assigned = {}
        # Go through all rows in table
        for row in table:
            # Get id and category from row
            ID = row[0]
            category = str(row[1])
            # Go through all room numbers defined in config.yml. Key is room number
            for key in valid:
                # If room number is with word then remove it from key
                # purpose of this is to get only room number without word for category name can be i.e "A-2001"
                # And then if key in category would not work
                if self.isWithWord:
                    newKey = ""
                    oldKey = key
                    afterPrefix = False
                    for s in key:
                        if s.isdigit():
                            afterPrefix = True
                        if afterPrefix:
                            newKey += s
                    key = newKey
                # If room number is in category of trend
                # The reason for few variation of key is that sometimes room number is written with characters _ or -
                # between suffix and prefix, and sometimes it's not, but there will almost certainly newer be a case
                # where there is a room called 2001-A and 2001A at the same time, so it's safe to assume that
                # ignoring _ and - will work always
                if key in category or key.replace("_", "") in category or key.replace("-", "") in category:
                    # If room number is with word, then add word to key back
                    if self.isWithWord:
                        key = oldKey
                    # If room number is already in dictionary then append trend ID to it
                    if assigned.get(key) is not None:
                        assigned[key].append(ID)
                    # If room number is not in dictionary then create Array for current room number
                    # and add trend ID to it
                    else:
                        assigned[key] = [ID]

        if assigned == {}:
            print("\033[93mNo objects with specified name in config.yml were found in database\033[0m")
            exit(1)

        # Go through all room numbers defined in config.yml
        for key in valid:
            # assigned[key] is array of trend IDs
            addresses = assigned.get(key)
            # Create empty string for trend IDs
            stringAddresses = ""
            # Go through all trend IDs in array
            for s in addresses:
                # If it's first trend ID then don't add comma
                if addresses.index(s) == 0:
                    stringAddresses += str(s)
                    continue  # Skip rest of the code in this loop and go to next iteration
                stringAddresses += "," + str(s)

            # Replace placeholders in file with room number and trend IDs
            self.dictionary["plan"]["objects"][0]["params"] = self.dictionary["plan"]["objects"][0]["params"].replace(
                "%trendAddresses%", stringAddresses)

            # Set widget name according to config.yml
            if self.addPrefix:
                widgetName = self.widgetName.replace("%romName%", key)
            else:
                keyWithoutWord = key.replace(self.theWord, "")
                widgetName = self.widgetName.replace("%romName%", keyWithoutWord)

            # Replace placeholders in file with room number
            self.dictionary["plan"]["name"] = widgetName

            # Create a json object from dictionary
            json_object = json.dumps(self.dictionary, indent=4)

            # Create tar file with name Trend_Widget_Rom-<room number>.tar
            file = tarfile.open(self.path + "/" + "output/widgets/Trend_Widget_Rom-" + key + ".tar", "w", None,
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

            # Add trend dictionary to the main class
            main.setTrendDictionary(self.dictionary)

            print("Trend_Widget_Rom-" + key + ".tar created")
