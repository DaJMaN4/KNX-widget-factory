from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class WebManagement:
    def __init__(self, path, levelName, frameworkName, infoWidgets, trendWidgets):
        self.path = path
        self.levelName = levelName
        self.frameworkName = frameworkName
        self.infoWidgets = infoWidgets
        self.trendWidgets = trendWidgets
        self.driver = webdriver.Chrome()
        self.driver.get('')
        self.driver.find_element(By.ID, "ext-comp-2349__Buildings").click()
        self.driver.maximize_window()
        self.loadedFramework = False
        self.wait = WebDriverWait(self.driver, 10)

    def uploadLevel(self):
        # self.wait.until(EC.element_to_be_clickable((By.XPATH, "//td[@class='x-grid3-col x-grid3-cell x-grid3-td-5 scada-cell-down scada-cell-icon ']/following-sibling::td"))).click()
        self.driver.find_element(By.XPATH, "//td[@class='x-grid3-col x-grid3-cell x-grid3-td-5 scada-cell-down scada-cell-icon ']/following-sibling::td").click()
        sleep(0.2)
        # self.wait.until(EC.element_to_be_clickable((By.ID, "ext-comp-1661"))).click()
        self.driver.find_element(By.ID, "ext-comp-1661").click()
        sleep(0.2)
        # new_activity_web_element = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(@class,'x-form-check-wrap')]"))).click(
        self.driver.find_element(By.XPATH, "//input[@value='keep']").click()
        choose_file = self.driver.find_element(By.ID, "ext-comp-1653")
        choose_file.send_keys(r"C:\Users\Damian\PycharmProjects\KNX-widget-factory\output\levels" + "\\" + self.levelName)
        sleep(0.2)
        self.driver.find_element(By.ID, "buildings-import-submit").click()
        sleep(1)

    def uploadFramework(self):

        self.driver.find_element(By.ID, "ext-comp-1651__ext-comp-1606").click()
        sleep(0.2)
        self.driver.find_element(By.XPATH, "//div[@data-record-id='layout']").click()
        sleep(0.2)
        self.driver.find_element(By.XPATH, "//table[@id='ext-comp-1664']").click()
        sleep(0.2)
        self.driver.find_element(By.XPATH, "//input[@value='keep']").click()
        sleep(0.2)
        choose_file = self.driver.find_element(By.XPATH, "//input[@accept='.tar']")
        choose_file.send_keys(r"C:\Users\Damian\PycharmProjects\KNX-widget-factory\output\frameworks" + "\\" + self.frameworkName)
        sleep(0.2)
        self.driver.find_element(By.XPATH, "//table[@id='buildings-import-submit']").click()
        self.loadedFramework = True
        sleep(1)

    def uploadWidgetsInOrder(self, ):
        if not self.loadedFramework:
            pass

        organizedTrendDictionary = self.trendWidgets.copy()
        for widget in self.infoWidgets:
            for widgetOrganized in organizedTrendDictionary:
                if widget == widgetOrganized:
                    continue
            for widgetSecond in self.infoWidgets:
                for widgetOrganized in organizedTrendDictionary:
                    if widget == widgetOrganized:
                        continue
                if self.infoWidgets[widget] < self.infoWidgets[widgetSecond]:
                    break
            else:
                organizedTrendDictionary[widget] = self.infoWidgets[widget]

        for widget in organizedTrendDictionary:
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

        organizedInfoDictionary = self.infoWidgets.copy()
        for widget in self.infoWidgets:
            for widgetOrganized in organizedInfoDictionary:
                if widget == widgetOrganized:
                    continue
            for widgetSecond in self.infoWidgets:
                for widgetOrganized in organizedInfoDictionary:
                    if widget == widgetOrganized:
                        continue
                if self.infoWidgets[widget] < self.infoWidgets[widgetSecond]:
                    break
            else:
                organizedInfoDictionary[widget] = self.infoWidgets[widget]

        for widget in organizedInfoDictionary:
            self.driver.find_element(By.ID, "ext-comp-1651__ext-comp-1606").click()
            sleep(0.5)
            self.driver.find_element(By.XPATH, "//div[@data-record-id='widget']").click()
            sleep(0.2)
            self.driver.find_element(By.XPATH, "//table[@id='ext-comp-1664']").click()
            sleep(0.2)
            self.driver.find_element(By.XPATH, "//input[@value='keep']").click()
            sleep(0.2)
            choose_file = self.driver.find_element(By.XPATH, "//input[@accept='.tar']")
            choose_file.send_keys(r"C:\Users\Damian\PycharmProjects\KNX-widget-factory\output\widgets" + "\\Info_Widget_Rom-" + widget + ".tar")
            sleep(0.2)
            self.driver.find_element(By.XPATH, "//table[@id='buildings-import-submit']").click()
            sleep(0.5)

    def uploadInfoWidgets(self):
        for widget in self.infoWidgets:
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

    def uploadTrendWidgets(self):
        for widget in self.trendWidgets:
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

    def upload(self):
        sleep(1)
        if self.levelName is not None:
            self.levelName = self.levelName.replace(".yml", ".tar")
            self.uploadLevel()
        if self.frameworkName is not None:
            self.frameworkName = self.frameworkName.replace(".yml", ".tar")
            self.loadFramework()
        self.loadWidgets()


