class InventoryPage:
    def __init__(self,page): self.page=page
    def add_first_item(self): self.page.locator("[data-test^='add-to-cart']").first.click()
    def cart_count(self): return self.page.locator(".shopping_cart_badge").inner_text()
    def open_cart(self): self.page.locator(".shopping_cart_link").click()
