class LoginPage:
    def __init__(self,page):
        self.page=page
    def open(self):
        self.page.goto("https://www.saucedemo.com/")
    def login(self,user,password):
        self.page.locator("[data-test='username']").fill(user)
        self.page.locator("[data-test='password']").fill(password)
        self.page.locator("[data-test='login-button']").click()
