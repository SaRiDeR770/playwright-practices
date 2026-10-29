import allure
from playwright.sync_api import Page, expect

from pages import ForgotPasswordPage
from tests.conftest import unique_email


@allure.feature("Authentication")
@allure.title("Password reset request shows a confirmation message")
def test_forgot_password(page: Page):
    forgot = ForgotPasswordPage(page).open()
    with allure.step("Submit the reset form"):
        forgot.request_reset(unique_email())
    with allure.step("Confirmation message is visible"):
        expect(page.get_by_text(ForgotPasswordPage.SUCCESS_MESSAGE)).to_be_visible()
