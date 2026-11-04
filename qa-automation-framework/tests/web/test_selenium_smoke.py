import os,pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
pytestmark=[pytest.mark.web,pytest.mark.skipif(os.getenv('RUN_SELENIUM')!='1',reason='Set RUN_SELENIUM=1 to run Selenium smoke')]
def test_saucedemo_login_page():
 d=webdriver.Chrome()
 try:
  d.get('https://www.saucedemo.com/'); assert d.find_element(By.ID,'user-name').is_displayed()
 finally: d.quit()
