from pages.base_page import BasePage


class LoginPage(BasePage):
    path = "/login"

    SUCCESS_MESSAGE = "You logged into a secure area!"
    INVALID_USERNAME_MESSAGE = "Your username is invalid!"
    INVALID_PASSWORD_MESSAGE = "Your password is invalid!"

    @property
    def username_input(self):
        return self.page.get_by_label("Username")

    @property
    def password_input(self):
        return self.page.get_by_label("Password")

    @property
    def login_button(self):
        return self.page.get_by_role("button", name="Login")

    @property
    def flash_message(self):
        return self.page.locator("#flash")

    def login(self, username: str, password: str) -> "LoginPage":
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
        return self
