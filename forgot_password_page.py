from playwright.sync_api import Page, expect
class ForgotPasswordPage:
    def __init__(self, page):
        self.page = page
    def open(self):
        self.page.goto('https://practice.expandtesting.com/forgot-password')
    def click_forgot(self, email):
        self.page.get_by_label('E-mail').fill(email)
        self.page.get_by_role('button', name='Retrieve password').click()