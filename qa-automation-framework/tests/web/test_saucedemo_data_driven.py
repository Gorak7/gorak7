import pytest
from pages.login_page import LoginPage
pytestmark=pytest.mark.web
@pytest.fixture
def signed_in(page):
    LoginPage(page).open();LoginPage(page).login("standard_user","secret_sauce")
    yield page
@pytest.mark.parametrize("username,password",[
 ("invalid","secret_sauce"),("standard_user","wrong"),("","secret_sauce"),("standard_user",""),("locked_out_user","secret_sauce")
])
def test_invalid_credentials(username,password,page):
    LoginPage(page).open();LoginPage(page).login(username,password)
    assert page.locator("[data-test='error']").is_visible()
@pytest.mark.parametrize("index",range(6))
def test_each_product_can_be_added_and_removed(signed_in,index):
    item=signed_in.locator(".inventory_item").nth(index)
    item.locator("button").click()
    assert signed_in.locator(".shopping_cart_badge").inner_text()=="1"
    item.locator("button").click()
    assert signed_in.locator(".shopping_cart_badge").count()==0
@pytest.mark.parametrize("index",range(6))
def test_each_product_opens_detail_page(signed_in,index):
    signed_in.locator(".inventory_item_name").nth(index).click()
    signed_in.locator(".inventory_details_container").wait_for(state="visible")
    assert signed_in.locator(".inventory_details_container").is_visible()
