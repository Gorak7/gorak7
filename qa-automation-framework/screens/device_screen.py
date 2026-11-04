from appium.webdriver.common.appiumby import AppiumBy
class DeviceScreen:
 def __init__(self,driver): self.driver=driver
 def open_app(self): self.driver.find_element(AppiumBy.ACCESSIBILITY_ID,'App').click()
 def open_action_bar(self): self.open_app(); self.driver.find_element(AppiumBy.ACCESSIBILITY_ID,'Action Bar').click()
