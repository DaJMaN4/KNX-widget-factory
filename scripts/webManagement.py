from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class WebManagement:
    def __init__(self, path, login, password, ip):
        self.path = path
        self.driver = webdriver.Chrome()
        self.driver.get('http://' + login + ':' + password + '@' + ip + '/scada-main')
        self.driver.get('')
        self.driver.find_element(By.ID, "ext-comp-2349__Buildings").click()
        self.driver.maximize_window()
        self.loadedFramework = False
        self.wait = WebDriverWait(self.driver, 10)

    def uploadLevel(self, levelName):
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//td[@class='x-grid3-col x-grid3-cell x-grid3-td-5 scada-cell-down scada-cell-icon ']/following-sibling::td"))).click()
        self.wait.until(EC.element_to_be_clickable((By.ID, "ext-comp-1661"))).click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='keep']"))).click()
        choose_file = self.wait.until(EC.element_to_be_clickable((By.ID, "ext-comp-1653"))).click()
        choose_file.send_keys(r"C:\Users\Damian\PycharmProjects\KNX-widget-factory\output\levels" + "\\" + levelName)
        self.wait.until(EC.element_to_be_clickable((By.ID, "buildings-import-submit"))).click()

    def uploadFramework(self, frameworkName):
        self.wait.until(EC.element_to_be_clickable((By.ID, "ext-comp-1651__ext-comp-1606"))).click()
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@data-record-id='layout']")))
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//table[@id='ext-comp-1664']")))
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='keep']")))
        choose_file = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@accept='.tar']")))
        choose_file.send_keys(r"C:\Users\Damian\PycharmProjects\KNX-widget-factory\output\frameworks" + "\\" + frameworkName)
        self.wait.until(EC.element_to_be_clickable((By.XPATH, "//table[@id='buildings-import-submit']"))).click()
        self.loadedFramework = True

    def uploadWidgetsInOrder(self, infoWidgets, trendWidgets):
        if not self.loadedFramework:
            pass

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

        for widget in organizedTrendDictionary:
            self.wait.until(EC.element_to_be_clickable((By.ID, "ext-comp-1651__ext-comp-1606"))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@data-record-id='widget']"))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//table[@id='ext-comp-1664']"))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='keep']"))).click()
            choose_file = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@accept='.tar']")))
            choose_file.send_keys(r"C:\Users\Damian\PycharmProjects\KNX-widget-factory\output\widgets" + "\\Trend_Widget_Rom-" + widget + ".tar")
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//table[@id='buildings-import-submit']"))).click()

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

        for widget in organizedInfoDictionary:
            self.wait.until(EC.element_to_be_clickable((By.ID, "ext-comp-1651__ext-comp-1606"))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@data-record-id='widget']"))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//table[@id='ext-comp-1664']"))).click()
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='keep']"))).click()
            choose_file = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@accept='.tar']")))
            choose_file.send_keys(r"C:\Users\Damian\PycharmProjects\KNX-widget-factory\output\widgets" + "\\Info_Widget_Rom-" + widget + ".tar")
            self.wait.until(EC.element_to_be_clickable((By.XPATH, "//table[@id='buildings-import-submit']"))).click()

    def uploadInfoWidgets(self, infoWidgets):
        for widget in infoWidgets:
            self.driver.find_element(By.ID, "ext-comp-1651__ext-comp-1606").click()
            sleep(0.5)
            self.driver.find_element(By.XPATH, "//div[@data-record-id='widget']").click()
            sleep(0.2)
            self.driver.find_element(By.XPATH, "//table[@id='ext-comp-1664']").click()
            sleep(0.2)
            self.driver.find_element(By.XPATH, "//input[@value='keep']").click()
            sleep(0.2)
            choose_file = self.driver.find_element(By.XPATH, "//input[@accept='.tar']")
            choose_file.send_keys(
                r"C:\Users\Damian\PycharmProjects\KNX-widget-factory\output\widgets" + "\\Info_Widget_Rom-" + widget + ".tar")
            sleep(0.2)
            self.driver.find_element(By.XPATH, "//table[@id='buildings-import-submit']").click()
            sleep(0.5)

    def uploadTrendWidgets(self, trendWidgets):
        for widget in trendWidgets:
            self.driver.find_element(By.ID, "ext-comp-1651__ext-comp-1606").click()
            sleep(0.5)
            self.driver.find_element(By.XPATH, "//div[@data-record-id='widget']").click()
            sleep(0.2)
            self.driver.find_element(By.XPATH, "//table[@id='ext-comp-1664']").click()
            sleep(0.2)
            self.driver.find_element(By.XPATH, "//input[@value='keep']").click()
            sleep(0.2)
            choose_file = self.driver.find_element(By.XPATH, "//input[@accept='.tar']")
            choose_file.send_keys(
                r"C:\Users\Damian\PycharmProjects\KNX-widget-factory\output\widgets" + "\\Trend_Widget_Rom-" + widget + ".tar")
            sleep(0.2)
            self.driver.find_element(By.XPATH, "//table[@id='buildings-import-submit']").click()
            sleep(0.5)

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


