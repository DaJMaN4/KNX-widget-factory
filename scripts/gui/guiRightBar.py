from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askopenfile
from tkinter.font import Font
import os


class GuiRightBar:
    def __init__(self, main, root, guiUtilities, databaseManager, path):
        self.main = main
        self.root = root
        self.guiUtilities = guiUtilities
        self.databaseManager = databaseManager
        self.createRightBar()
        self.path = path

    def importDatabase(self):
        file = askopenfile(mode='r', filetypes=[('LM back-up', '*.zip')])
        if file is not None:
            self.databaseManager.unZipData(file.name)
            self.databaseName.config(text=file.name.split("/")[-1])

    def createObjects(self):
        if not self.main.checksBeforeCreating():
            return
        if self.createTrendWidget.get() == 1:
            self.main.createTrendWidgets()

        if self.createInfoWidget.get() == 1:
            self.main.createInfoWidgets()

        if self.createStructure.get() == 1:
            self.main.createStructure()

    def createObjectsAndUpload(self):
        webManagement = self.main.createWebManagement(self.login.get(), self.password.get(), self.ipAddress.get())
        if not self.main.checksBeforeCreating():
            return
        done = False
        if self.createTrendWidget.get() == 1 and self.createInfoWidget.get() == 1 and self.createStructure.get() == 1:
            self.main.creatingStructure()
            self.main.createTrendWidgets()
            self.main.createInfoWidgets()
            self.main.createStructure()
            webManagement.uploadAllInOrder(self.main.mainStructureFileName, self.main.frameworkFileName, self.main.infoWidgetDictionary, self.main.trendWidgetDictionary)
            for file in os.listdir(self.path + r"\output\widgets"):
                os.remove(self.path + r"\output\widgets" + "\\" + file)
            done = True

        elif self.createTrendWidget.get() == 1 and self.createInfoWidget.get() == 1 and self.createStructure.get() == 0:
            self.main.createTrendWidgets()
            self.main.createInfoWidgets()
            webManagement.uploadTrendWidgets(self.main.trendWidgetDictionary)
            webManagement.uploadInfoWidgets(self.main.infoWidgetDictionary)
            for file in os.listdir(self.path + r"\output\widgets"):
                os.remove(self.path + r"\output\widgets" + "\\" + file)
            done = True

        if self.createStructure.get() == 1 and not done:
            self.main.creatingStructure()
            self.main.createStructure()
            webManagement.uploadLevel(self.main.mainStructureFileName)
            webManagement.uploadFramework(self.main.frameworkFileName)

        if self.createTrendWidget.get() == 1 and not done:
            self.main.createTrendWidgets()
            webManagement.uploadTrendWidgets(self.main.trendWidgetDictionary)
            for file in os.listdir(self.path + r"\output\widgets"):
                os.remove(self.path + r"\output\widgets" + "\\" + file)

        if self.createInfoWidget.get() == 1 and not done:
            self.main.createInfoWidgets()
            webManagement.uploadInfoWidgets(self.main.infoWidgetDictionary)
            for file in os.listdir(self.path + r"\output\widgets"):
                os.remove(self.path + r"\output\widgets" + "\\" + file)

    def createRightBar(self):

        frameRightBar = Frame(self.root)

        frameRightBar.grid_rowconfigure(1, minsize=10)

        add_button = Button(frameRightBar, text="import database", command=lambda: self.importDatabase())
        add_button.grid(row=2, column=1)

        self.databaseName = Label(frameRightBar, text="No database imported")
        self.databaseName.grid(row=3, column=1, sticky="n")

        frameRightBar.grid_rowconfigure(4, minsize=10)

        separator = ttk.Separator(frameRightBar, orient='horizontal')
        separator.grid(row=5, column=1, sticky="nsew")

        frameRightBar.grid_rowconfigure(6, minsize=10)

        self.createTrendWidget = IntVar()
        self.createInfoWidget = IntVar()
        self.createStructure = IntVar()

        radioBox = ttk.Checkbutton(frameRightBar, text="Create Trend Widget", variable=self.createTrendWidget)
        radioBox.grid(row=7, column=1, sticky="w")
        frameRightBar.grid_rowconfigure(8, minsize=10)
        radioBox = ttk.Checkbutton(frameRightBar, text="Create Info Widget", variable=self.createInfoWidget)
        radioBox.grid(row=9, column=1, sticky="w")
        frameRightBar.grid_rowconfigure(10, minsize=10)
        radioBox = ttk.Checkbutton(frameRightBar, text="Create Framework & Level", variable=self.createStructure)
        radioBox.grid(row=11, column=1, sticky="w")
        frameRightBar.grid_rowconfigure(12, minsize=10)

        add_button = Button(frameRightBar, text="Create Objects", command=lambda: self.createObjects())
        add_button.grid(row=13, column=1)

        frameRightBar.grid_rowconfigure(14, minsize=10)

        separator = ttk.Separator(frameRightBar, orient='horizontal')
        separator.grid(row=15, column=1, sticky="nsew")

        frameRightBar.grid_rowconfigure(16, minsize=10)

        label = Label(frameRightBar, text="Login")
        label.grid(row=17, column=1, sticky="n")

        self.login = StringVar()
        entry = Entry(frameRightBar, textvariable=self.login)
        entry.grid(row=18, column=1, sticky="n")

        frameRightBar.grid_rowconfigure(19, minsize=10)

        label = Label(frameRightBar, text="Password")
        label.grid(row=20, column=1, sticky="n")

        self.password = StringVar()
        entry = Entry(frameRightBar, textvariable=self.password)
        entry.grid(row=21, column=1, sticky="n")

        frameRightBar.grid_rowconfigure(22, minsize=10)

        label = Label(frameRightBar, text="IP Address")
        label.grid(row=23, column=1, sticky="n")

        self.ipAddress = StringVar()
        entry = Entry(frameRightBar, textvariable=self.ipAddress)
        entry.grid(row=24, column=1, sticky="n")

        frameRightBar.grid_rowconfigure(25, minsize=10)

        add_button = Button(frameRightBar, text="Create Objects and Upload", command=lambda: self.createObjectsAndUpload())
        add_button.grid(row=26, column=1)

        frameRightBar.grid_columnconfigure(1, minsize=200)

        frameRightBar.grid(row=1, column=5, sticky="nsew", rowspan=3)


