from playwright.sync_api import Page, expect
def test_forgot_password(page: 'Page'):
    page.goto('https://practice.expandtesting.com/forgot-password')
    page.get_by_label('E-mail').fill('sardor.saidov.315kb@gmail.com')
    page.get_by_role('button', name = "Retrieve password").click()
    expect(page.get_by_text('An e-mail has been sent to you which explains how to reset your password.')).to_be_visible()
