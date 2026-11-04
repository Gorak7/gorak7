import os,pytest
from appium import webdriver
from appium.options.android import UiAutomator2Options
pytestmark=[pytest.mark.mobile,pytest.mark.skipif(os.getenv("RUN_APPIUM")!="1",reason="Requires Appium server and Android emulator")]
@pytest.fixture
def driver():
    caps={"platformName":"Android","automationName":"UiAutomator2","deviceName":"Android Emulator","appPackage":"io.appium.android.apis","appActivity":".ApiDemos","appWaitActivity":"*"}
    d=webdriver.Remote(os.getenv("APPIUM_URL","http://127.0.0.1:4723"),options=UiAutomator2Options().load_capabilities(caps))
    yield d
    d.quit()
def test_appium_launch(driver):
    assert driver.current_package=="io.appium.android.apis"
def test_appium_app_navigation(driver):
    driver.find_element("accessibility id","App").click()
    assert driver.find_element("accessibility id","Action Bar").is_displayed()
def test_appium_activity_is_loaded(driver):
    assert "ApiDemos" in driver.current_activity
def test_appium_orientation_is_supported(driver):
    assert driver.orientation in {"PORTRAIT","LANDSCAPE"}
def test_appium_window_has_size(driver):
    size=driver.get_window_size()
    assert size["width"]>0 and size["height"]>0
def test_appium_home_menu_is_visible(driver):
    assert driver.find_element("accessibility id","App").is_displayed()
def test_appium_navigate_to_action_bar(driver):
    driver.find_element("accessibility id","App").click()
    assert driver.find_element("accessibility id","Action Bar").is_displayed()
def test_appium_back_navigation(driver):
    driver.find_element("accessibility id","App").click()
    driver.back()
    assert driver.find_element("accessibility id","App").is_displayed()
def test_appium_page_source_available(driver):
    assert len(driver.page_source)>100
def test_appium_screen_orientation_can_be_reset(driver):
    driver.orientation="PORTRAIT"
    assert driver.orientation=="PORTRAIT"
