import ast
import os
import tarfile
import yaml
import main


class ImportManager:
    # Initialize TrendWidgetFactory class it sets all variables when creating the object in main class
    def __init__(self, path, roomObjectNames):
        self.path = path
        self.roomObjectNames = roomObjectNames

    # Open function is called from main class and it contains everything to run successfully the module it goes
    # through all files in import folder and checks if file with the same name exists in schematics folder, if it
    # exists then it skips this file and continues to next file in import folder, if it doesn't exist then it
    # checks if file is .tar format, if it is then it opens file and goes through all files in it and if it finds
    # data.json file then it reads it and writes it to schematics folder in .yml format, if file is not .tar format
    # then it prints error message and exits program.
    def open(self):
        # Goes through all files in import folder
        for file in os.listdir(self.path + "/import"):
            # Goes through all files in schematics folder
            for fileSchematics in os.listdir(self.path + "/schematics"):
                # Create string with changed extension from .tar to .yml
                fileImport = file.replace(".tar", ".yml")
                # If file with the same name as defined in config.yml
                if fileImport == fileSchematics:
                    # Skip this file and continue to next file in import folder
                    print("File with name " + file + " already exists in schematics, skipping...")
                    break
            # Runs if for didn't encounter break which means that file doesn't exist
            else:
                # If file is .tar format
                if file.endswith(".tar"):
                    # Open file as "r" which means read only. tar is a variable name of opened file
                    tar = tarfile.open(os.path.join(self.path + "/import", file), "r")
                    # Goes through all files in tar file
                    for member in tar.getmembers():
                        # If file is data.json
                        if member.name == "./data.json":
                            # Extract file from tar file
                            f = tar.extractfile(member)
                            # If file is not None
                            if f is not None:
                                # Read file and decode it from bytes to string
                                content = f.read()
                                # Write file to schematics folder
                                self.write(ast.literal_eval(content.decode('utf-8')), file)
                    # Close tar file
                    tar.close()
                # If file is not .tar format
                else:
                    # Print error message and exit program
                    print("File" + file + " is not supported, use .tar format")
                    exit(1)

    # This method is for writing file to schematics folder with placeholders it checks if file is trend widget or
    # info widget, and then it calls method for replacing data either for trend widget or info widget, and then it
    # writes file to schematics folder in .yml format.
    def write(self, data: dict, name):
        # Replace .tar extension to .yml
        name = name.replace(".tar", ".yml")

        # Try to write placeholders into file
        try:
            # Change name of room to placeholder
            data["plan"]["name"] = "%roomName%"

            # If file is trend widget
            if data["plan"]["objects"][0].get("params") is not None and "id=" in data["plan"]["objects"][0].get(
                    "params"):
                data = self.importTrendWidget(data)
            # If file is info widget
            else:
                data = self.importInfoWidget(data)

        # If something goes wrong
        except Exception as e:
            # Print error message and raise exception
            print("\033[93mFailed to automatically write placeholders into files \033[0m")
            raise e

        # Open file as "x" which means write only. "file" is a variable name of opened file
        file = open(self.path + "/schematics/" + name, "x")
        # Write file to schematics folder
        yaml.dump(data, file, allow_unicode=True)

        print("File " + name + " has been successfully written to schematics")

    # This method is for getting addresses form params for trends widget and replacing it with a placeholder
    # It goes through all characters in params to find string "id=" which can appear only once, and it means that
    # next characters are addresses of trends, so if it finds characters i d and = in a row then boolean passed
    # becomes True, and it starts to store addresses in addresses variable, when it finds & character it replaces
    # addresses with a placeholder and breaks the loop
    def importTrendWidget(self, data):
        # Variable for counting how many times it passed
        passIt = 0
        # Variable for checking if it passed
        passed = False
        # Variable for storing addresses
        addresses = ""
        # Goes through all characters in params
        for s in data["plan"]["objects"][0]["params"]:
            # If it passed
            if passed:
                # If character is not &
                if s != "&":
                    # Add character to addresses variable
                    addresses += s
                # If character is &
                else:
                    # Replace addresses with a placeholder
                    data["plan"]["objects"][0]["params"] = data["plan"]["objects"][0]["params"].replace(
                        addresses, "%trendAddresses%")
                    # Break the loop
                    break
            # If it didn't pass
            else:
                # Checks if there is a word id= in params, and if it is then it changes passed to True
                if s == "i":
                    passIt += 1
                elif s == "d" and passIt == 1:
                    passIt += 1
                elif s == "=" and passIt == 2:
                    passIt += 1
                else:
                    passIt = 0
                if passIt == 3:
                    passed = True
        # Returns modified data back to write method
        return data

    # This method is for getting object names from database and replacing it with a placeholder. It goes through all
    # rows in table and gets id and name from row, then it goes through all object names defined in config.yml and if
    # object name is in name of object and current imported file has the same id as object id from database then it
    # is certain that it is the same object, so it replaces object name with a placeholder that will be used in the
    # future to replace it with a real object id of an object of a room.
    def importInfoWidget(self, data):
        table = main.getDatabaseObject().getTableColumns(["id, name"], "objects")
        # Goes through all rows in table
        for row in table:
            # Get object from data which is data from the file that is being imported
            for objectInData in data["plan"]["objects"]:
                # If object is not None
                if objectInData.get("object") is not None:
                    # Get id and name from row
                    ID = row[0]
                    name = str(row[1])
                    # Goes through all room object names defined in config.yml
                    for roomObjectName in self.roomObjectNames:
                        # If room object name is in name of object in current row
                        if roomObjectName in name:
                            # If object name is in name of object in current row
                            if ID == objectInData["object"]:
                                # Replace object name with a placeholder and exit
                                objectInData["object"] = roomObjectName
                                objectInData["statusobject"] = roomObjectName
                                break

        return data
