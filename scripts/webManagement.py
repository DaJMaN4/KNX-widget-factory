from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import os


class WebManagement:
    def __init__(self, path, login, password, ip, main):
        self.path = path
        self.disable = False
        if ip == "":
            main.log("IP address is missing")
            self.disable = True
            return
        self.driver = webdriver.Chrome()
        print("login  ", login)
        try:
            self.driver.get('http://' + login + ':' + password + '@' + ip + '/scada-main')

        except:
            main.log("Wrong login, password or ip")
            self.disable = True
            return

        try:
            self.driver.find_element(By.ID, "ext-comp-2349__Buildings").click()
        except:
            main.log("Wrong login, password or ip")
            self.disable = True
            return
        self.driver.maximize_window()
        self.loadedFramework = False
        self.wait = WebDriverWait(self.driver, 10)

    def isDisable(self):
        return self.disable

    def uploadLevel(self, levelName):
        self.wait.until(EC.element_to_be_clickable((By.XPATH,
                                                    "//td[@class='x-grid3-col x-grid3-cell x-grid3-td-5 scada-cell-down scada-cell-icon ']/following-sibling::td"))).click()
        self.wait.until(EC.element_to_be_clickable((By.ID, "ext-comp-1661"))).click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='keep']"))).click()
        choose_file = self.wait.until(EC.element_to_be_clickable((By.ID, "ext-comp-1653")))
        choose_file.send_keys(self.path + r"\output\levels" + "\\" + levelName)
        self.wait.until(EC.element_to_be_clickable((By.ID, "buildings-import-submit"))).click()
        sleep(1)

    def uploadFramework(self, frameworkName):
        self.wait.until(EC.element_to_be_clickable((By.ID, "ext-comp-1651__ext-comp-1606"))).click()
        sleep(0.5)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@data-record-id='layout']"))).click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//table[@id='ext-comp-1664']"))).click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='keep']"))).click()
        choose_file = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@accept='.tar']")))
        choose_file.send_keys(self.path + r"\output\frameworks" + "\\" + frameworkName)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//table[@id='buildings-import-submit']"))).click()
        sleep(1)

    def uploadWidgetsInOrder(self, infoWidgets, trendWidgets):
        organizedTrendDictionary = trendWidgets.copy()
        for widget in infoWidgets:
            for widgetOrganized in organizedTrendDictionary:
                if widget == widgetOrganized:
                    continue
            for widgetSecond in infoWidgets:
                for widgetOrganized in organizedTrendDictionary:
                    if widget == widgetOrganized:
                        continue
                if infoWidgets[widget] < infoWidgets[widgetSecond]:
                    break
            else:
                organizedTrendDictionary[widget] = infoWidgets[widget]

        self.uploadTrendWidgets(organizedTrendDictionary)

        organizedInfoDictionary = infoWidgets.copy()
        for widget in infoWidgets:
            for widgetOrganized in organizedInfoDictionary:
                if widget == widgetOrganized:
                    continue
            for widgetSecond in infoWidgets:
                for widgetOrganized in organizedInfoDictionary:
                    if widget == widgetOrganized:
                        continue
                if infoWidgets[widget] < infoWidgets[widgetSecond]:
                    break
            else:
                organizedInfoDictionary[widget] = infoWidgets[widget]

        self.uploadInfoWidgets(organizedInfoDictionary)

    def uploadInfoWidgets(self, infoWidgets):
        for widget in infoWidgets:
            self.wait.until(EC.element_to_be_clickable((By.ID, "ext-comp-1651__ext-comp-1606"))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@data-record-id='widget']"))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//table[@id='ext-comp-1664']"))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='keep']"))).click()
            choose_file = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@accept='.tar']")))
            choose_file.send_keys(self.path + r"\output\widgets" + "\\Info_Widget_Rom-" + widget + ".tar")
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//table[@id='buildings-import-submit']"))).click()
            sleep(1)
            # delete everything in folder output/widgets

    def uploadTrendWidgets(self, trendWidgets):
        for widget in trendWidgets:
            self.wait.until(EC.element_to_be_clickable((By.ID, "ext-comp-1651__ext-comp-1606"))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@data-record-id='widget']"))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//table[@id='ext-comp-1664']"))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='keep']"))).click()
            choose_file = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@accept='.tar']")))
            choose_file.send_keys(self.path + r"\output\widgets" + "\\Trend_Widget_Rom-" + widget + ".tar")
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//table[@id='buildings-import-submit']"))).click()
            sleep(1)

    def isEnable(self):
        pass

    def uploadAllInOrder(self, levelName, frameworkName, infoWidgets, trendWidgets):
        sleep(1)
        if levelName is not None:
            levelName = levelName.replace(".yml", ".tar")
            self.uploadLevel(levelName)
        if frameworkName is not None:
            frameworkName = frameworkName.replace(".yml", ".tar")
            self.uploadFramework(frameworkName)
        self.uploadWidgetsInOrder(infoWidgets, trendWidgets)
