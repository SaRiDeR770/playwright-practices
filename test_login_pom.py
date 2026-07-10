from playwright.sync_api import Page, expect
from login_page import LoginPage
def test_login_pom(page: Page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("practice", "SuperSecretPassword!")
    expect(page.get_by_text('You logged into a secure area!')).to_be_visible()

