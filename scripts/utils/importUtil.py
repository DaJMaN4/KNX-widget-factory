import ast
import os
import tarfile
import yaml


class ImportManager:
    def __init__(self, path):
        self.path = path

    def open(self, folder):
        for file in os.listdir(self.path + "/import/" + folder):

            for fileSchematics in os.listdir(self.path + "/schematics/" + folder):
                fileImport = file.replace(".tar", ".yml")
                if fileImport == fileSchematics:
                    print("File with name " + file + " already exists in schematics, skipping...")
                    return
            if file.endswith(".tar"):
                tar = tarfile.open(os.path.join(self.path + "/import/" + folder, file), "r")
                for member in tar.getmembers():
                    if member.name == "./data.json":
                        f = tar.extractfile(member)
                        if f is not None:
                            content = f.read()
                            self.write(ast.literal_eval(content.decode('utf-8')), file, folder)
                tar.close()
            else:
                print("File" + file + " is not supported, use .tar format")
                exit(1)

    def write(self, data: dict, name, folder):
        # Replace .tar extension to .yml
        name = name.replace(".tar", ".yml")
        # Open file as "x" which means write only. "file" is a variable name of opened file
        file = open(self.path + "/schematics/" + folder + "/" + name, "x")
        # Write file to schematics folder
        yaml.dump(data, file, allow_unicode=True)

        print("File " + name + " has been successfully written to schematics")

    def getData(self, schematicName, folder):
        onlyOne = False
        if len(os.listdir(self.path + "/schematics/" + folder)) == 1:
            onlyOne = True
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

