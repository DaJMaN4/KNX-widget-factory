import ast
import os
import tarfile
import yaml


class ImportManager:
    def __init__(self, path):
        self.path = path

    # Opens file and extracts data.json from it
    def open(self, fileInFolder, folder):
        if fileInFolder.endswith(".tar"):
            tar = tarfile.open(fileInFolder, "r")
            for member in tar.getmembers():
                if member.name == "./data.json":
                    f = tar.extractfile(member)
                    if f is not None:
                        content = f.read()
                        self.write(ast.literal_eval(content.decode('utf-8')), fileInFolder.split("/")[-1], folder)
            tar.close()
        else:
            print("File " + "file" + " is not supported, use .tar format")
            exit(1)

    # Writes data to file in schematics folder
    def write(self, data: dict, name, folder):
        # Replace .tar extension to .yml
        name = name.replace(".tar", ".yml")
        # Delete every file in schematics folder
        for file in os.listdir(self.path + "/schematics/" + folder):
            os.remove(self.path + "/schematics/" + folder + "/" + file)
        # Open file as "x" which means write only. "file" is a variable name of opened file
        file = open(self.path + "/schematics/" + folder + "/" + name, "x")
        # Write file to schematics folder
        yaml.dump(data, file, allow_unicode=True)

        print("File " + name + " has been successfully written to schematics")

    # Gets data from file in schematics folder
    def getData(self, schematicName, folder):
        onlyOne = False
        if len(os.listdir(self.path + "/schematics/" + folder)) == 1:
            onlyOne = True
            print("There is only one file in schematics/" + folder + " folder")
        elif len(os.listdir(self.path + "/schematics/" + folder)) == 0:
            print("There is no files in schematics/" + folder + " folder")
            exit(1)
        # Goes through all files in schematics folder
        for schematicFile in os.listdir(self.path + "/schematics/" + folder):
            # If file with the same name as defined in config.yml
            if schematicFile == schematicName or onlyOne or schematicName == "":
                # Open file as "r" which means read only. "file" is a variable name of opened file
                with open(self.path + "/schematics/" + folder + "/" + schematicFile, 'r') as file:
                    # Load yaml file to dictionary variable
                    return yaml.safe_load(file)
        return None

