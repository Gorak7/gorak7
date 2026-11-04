class LoginPage:
    def __init__(self,page): self.page=page
    def open(self): self.page.goto("https://www.saucedemo.com/")
    def login(self,user,password):
        self.page.get_by_test_id("username").fill(user)
        self.page.get_by_test_id("password").fill(password)
        self.page.get_by_test_id("login-button").click()
