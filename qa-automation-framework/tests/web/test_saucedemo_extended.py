import pytest
from pages.login_page import LoginPage
pytestmark=pytest.mark.web
@pytest.fixture
def logged_in(page):
    LoginPage(page).open();LoginPage(page).login("standard_user","secret_sauce")
    yield page
@pytest.mark.parametrize("sort_value",["az","za","lohi","hilo"])
def test_inventory_sort_options(logged_in,sort_value):
    logged_in.locator("[data-test='product-sort-container']").select_option(sort_value)
    assert logged_in.locator(".inventory_item").count()==6
def test_product_detail_navigation(logged_in):
    logged_in.locator(".inventory_item_name").first.click()
    assert logged_in.locator(".inventory_details").is_visible()
def test_add_then_remove_product(logged_in):
    logged_in.locator("[data-test^='add-to-cart']").first.click()
    logged_in.locator("[data-test^='remove']").first.click()
    assert logged_in.locator(".shopping_cart_badge").count()==0
def test_cart_badge_updates(logged_in):
    logged_in.locator("[data-test^='add-to-cart']").nth(0).click()
    logged_in.locator("[data-test^='add-to-cart']").nth(1).click()
    assert logged_in.locator(".shopping_cart_badge").inner_text()=="2"
def test_checkout_requires_first_name(logged_in):
    logged_in.locator("[data-test^='add-to-cart']").first.click()
    logged_in.locator(".shopping_cart_link").click()
    logged_in.locator("[data-test='checkout']").click()
    logged_in.locator("[data-test='lastName']").fill("Tester")
    logged_in.locator("[data-test='postalCode']").fill("500001")
    logged_in.locator("[data-test='continue']").click()
    assert logged_in.locator("[data-test='error']").is_visible()
def test_complete_checkout(logged_in):
    logged_in.locator("[data-test^='add-to-cart']").first.click()
    logged_in.locator(".shopping_cart_link").click()
    logged_in.locator("[data-test='checkout']").click()
    logged_in.locator("[data-test='firstName']").fill("Gorak")
    logged_in.locator("[data-test='lastName']").fill("QA")
    logged_in.locator("[data-test='postalCode']").fill("500001")
    logged_in.locator("[data-test='continue']").click()
    logged_in.locator("[data-test='finish']").click()
    assert "Thank you" in logged_in.locator(".complete-header").inner_text()
def test_logout(logged_in):
    logged_in.locator("#react-burger-menu-btn").click()
    logged_in.locator("#logout_sidebar_link").click()
    assert logged_in.locator("[data-test='login-button']").is_visible()
