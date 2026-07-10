from playwright.sync_api import Page, expect
class LoginPage:
    def __init__(self, page):
        self.page = page
    def open(self):
        self.page.goto('https://practice.expandtesting.com/login')
    def login(self, username, password):
          login = self.page.get_by_label('Username')
          login.fill(username)
          password_field = self.page.get_by_label('Password')
          password_field.fill(password)
          self.page.get_by_role('button', name = 'Login').click()