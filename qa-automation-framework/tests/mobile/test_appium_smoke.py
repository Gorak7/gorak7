import os,pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
pytestmark=[pytest.mark.mobile,pytest.mark.skipif(os.getenv('RUN_APPIUM')!='1',reason='Requires Appium server and Android emulator')]
@pytest.fixture
def driver():
 caps={'platformName':'Android','automationName':'UiAutomator2','deviceName':'Android Emulator','appPackage':'io.appium.android.apis','appActivity':'.ApiDemos'}
 d=webdriver.Remote(os.getenv('APPIUM_URL','http://127.0.0.1:4723'),options=UiAutomator2Options().load_capabilities(caps)); yield d; d.quit()
def test_appium_launch(driver): assert driver.current_package=='io.appium.android.apis'
def test_appium_app_navigation(driver):
 driver.find_element('accessibility id','App').click()
 assert driver.find_element('accessibility id','Action Bar').is_displayed()
