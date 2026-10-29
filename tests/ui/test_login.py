import allure
import pytest
from playwright.sync_api import Page, expect

from config import settings
from pages import LoginPage


@allure.feature("Authentication")
class TestLogin:
    # @allure.id links the autotest to the manual test case in the TMS
    # (Testomat.io / Allure TestOps), so coverage is tracked case by case.
    @allure.id("AUTH-1")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.title("Login with valid credentials opens the secure area")
    def test_login_success(self, login_page: LoginPage):
        with allure.step("Submit valid username and password"):
            login_page.login(settings.UI_USERNAME, settings.UI_PASSWORD)
        with allure.step("Secure area is shown"):
            expect(login_page.page).to_have_url(f"{settings.BASE_URL}/secure")
            expect(login_page.flash_message).to_contain_text(LoginPage.SUCCESS_MESSAGE)

    @allure.id("AUTH-2")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title("Login with {username!r} / {password!r} shows: {expected_message}")
    @pytest.mark.parametrize(
        "username, password, expected_message",
        [
            ("", settings.UI_PASSWORD, LoginPage.INVALID_USERNAME_MESSAGE),
            ("wrong-user", settings.UI_PASSWORD, LoginPage.INVALID_USERNAME_MESSAGE),
            (settings.UI_USERNAME, "", LoginPage.INVALID_PASSWORD_MESSAGE),
            (settings.UI_USERNAME, "wrong-password", LoginPage.INVALID_PASSWORD_MESSAGE),
        ],
        ids=["empty-username", "wrong-username", "empty-password", "wrong-password"],
    )
    def test_login_negative(self, login_page: LoginPage, username, password, expected_message):
        with allure.step("Submit invalid credentials"):
            login_page.login(username, password)
        with allure.step("User stays on the login page and sees an error"):
            expect(login_page.page).to_have_url(f"{settings.BASE_URL}/login")
            expect(login_page.flash_message).to_contain_text(expected_message)

    @allure.title("Session cookie is set after login")
    def test_session_cookie_is_set(self, logged_in_page: Page):
        cookies = logged_in_page.context.cookies()
        assert cookies, "Expected at least one cookie after a successful login"
