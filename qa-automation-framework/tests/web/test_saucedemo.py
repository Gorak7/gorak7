import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
pytestmark=pytest.mark.web
@pytest.fixture
def page(browser):
    p=browser.new_page()
    yield p
    p.close()
def test_valid_login_and_inventory(page):
    LoginPage(page).open();LoginPage(page).login("standard_user","secret_sauce")
    assert page.locator(".title").inner_text()=="Products"
    assert page.locator(".inventory_item").count()==6
def test_invalid_login_message(page):
    LoginPage(page).open();LoginPage(page).login("bad_user","bad_password")
    assert page.locator("[data-test=error]").is_visible()
def test_locked_user_message(page):
    LoginPage(page).open();LoginPage(page).login("locked_out_user","secret_sauce")
    assert "locked out" in page.locator("[data-test=error]").inner_text().lower()
def test_add_to_cart(page):
    LoginPage(page).open();LoginPage(page).login("standard_user","secret_sauce")
    InventoryPage(page).add_first_item()
    assert InventoryPage(page).cart_count()=="1"
def test_cart_checkout(page):
    LoginPage(page).open();LoginPage(page).login("standard_user","secret_sauce")
    InventoryPage(page).add_first_item()
    assert InventoryPage(page).cart_count()=="1"
    InventoryPage(page).open_cart()
    page.locator("[data-test=checkout]").wait_for(state="visible")
    assert page.locator(".shopping_cart_badge").inner_text()=="1"
    page.locator("[data-test=checkout]").click()
    page.locator("[data-test=firstName]").fill("QA")
    page.locator("[data-test=lastName]").fill("Tester")
    page.locator("[data-test=postalCode]").fill("500001")
    page.locator("[data-test=continue]").click()
    page.locator("[data-test=finish]").wait_for(state="visible")
    assert page.locator("[data-test=finish]").is_visible()
