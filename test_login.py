from playwright.sync_api import Page, expect
def test_login (page: Page):
    page.goto('https://practice.expandtesting.com/login')
    login = page.get_by_label('Username')
    login.fill('practice')
    password = page.get_by_label('Password')
    password.fill('SuperSecretPassword!')
    page.get_by_role('button', name = 'Login').click()
    expect(page.get_by_text('You logged into a secure area!')).to_be_visible()