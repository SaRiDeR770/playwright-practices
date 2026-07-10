from playwright.sync_api import Page, expect
class CheckboxPage:
    def __init__(self, page):
        self.page = page
    def open(self):
        self.page.goto('https://practice.expandtesting.com/checkboxes')
    def check_first(self):
         self.page.get_by_label('Checkbox 1').check()
    