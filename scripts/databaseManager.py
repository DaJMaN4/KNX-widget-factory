import sqlite3
import os
from zipfile import ZipFile
import shutil


class DatabaseManager:
    def __init__(self, path, main):
        self.connection = None
        self.path = path
        self.main = main

    # Unzips file from database folder to data folder and then connects to database
    def unZipData(self, file):
        # Delete all files in data folder before unzipping
        if self.connection is not None:
            self.main.log("Closing connection to database")
            self.connection.close()
        for filename in os.listdir(self.path + "/data"):
            file_path = os.path.join(self.path + "/data", filename)
            # tries to delete a file or folder in data folder if it fails then it prints error message
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                self.main.log('Failed to delete old data: %s. Reason: %s' % (file_path, e))
        # Goes through all files in database folder

        with ZipFile(file, 'r') as zObject:
            # Extract all the contents of zip file in data directory
            zObject.extractall(self.path + "/data/")
        self.main.log("Unzipped file to data folder")
        # Check if database file exists in data folder
        if os.path.exists(self.path + "/data/storage/db/current.db"):
            # Connect to database
            self.main.log("Successfully connected to the database")
            self.connection = sqlite3.connect(self.path + "/data/storage/db/current.db")
            # Set text factory to bytes, it's a mode that can read special characters like å and ø
            self.connection.text_factory = bytes
        # If database file doesn't exist then print error message and exit program
        else:
            self.main.log("No data found in database folder")
            exit(1)
        # Set biggestWidgetID to the biggest widget id in database
        self.main.biggestWidgetID = self.getBiggestWidgetID()

    # Get chosen columns from chosen table
    def getTableColumns(self, columns: list, table: str = "objects"):
        # Convert list to string
        columns = str(columns)
        # Remove all unnecessary characters from string
        columns = columns.replace("[", "")
        columns = columns.replace("]", "")
        columns = columns.replace("'", "")

        # Execute sql command to get chosen columns from chosen table
        table = self.connection.execute("SELECT " + columns + " from " + table)
        # Return table with chosen columns
        return table

    def getBiggestWidgetID(self):
        table = self.connection.execute("SELECT id from visfloors ORDER BY id DESC LIMIT 1")
        return table.fetchone()[0]

    def getAllImages(self):
        if os.path.exists(self.path + "/data/storage/img"):
            images = []
            for filename in os.listdir(self.path + "/data/storage/img"):
                images.append(filename)
            return images
        return None



