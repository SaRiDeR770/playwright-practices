from playwright.sync_api import Page, expect
from forgot_password_page import ForgotPasswordPage
def test_forgot_password_pom(page: Page):
    forgot_password_page = ForgotPasswordPage(page)
    forgot_password_page.open()
    forgot_password_page.click_forgot('sardor.saidov.077@mail.ru')
    expect(page.get_by_text('An e-mail has been sent to you which explains how to reset your password.')).to_be_visible()