"""Browser-level interactions: hover, iframes, new windows."""
import allure
from playwright.sync_api import Page, expect

from config import settings
from tests.conftest import unique_email


@allure.feature("Browser interactions")
class TestBrowserInteractions:
    @allure.title("Hovering an avatar reveals the user caption")
    def test_hover_shows_caption(self, page: Page):
        page.goto(f"{settings.BASE_URL}/hovers")
        page.get_by_test_id("user-1").hover()
        expect(page.get_by_text("name: user1")).to_be_visible()

    @allure.title("Input inside an iframe accepts text")
    def test_iframe_input(self, page: Page):
        page.goto(f"{settings.BASE_URL}/iframe")
        email = unique_email()
        frame = page.frame_locator("#email-subscribe")
        frame.locator("#email").fill(email)
        expect(frame.locator("#email")).to_have_value(email)

    @allure.title("Link opens a new window with the expected content")
    def test_new_window(self, page: Page):
        page.goto(f"{settings.BASE_URL}/windows")
        with page.context.expect_page() as new_page_info:
            page.get_by_role("link", name="Click here").click()
        new_page = new_page_info.value
        expect(
            new_page.get_by_text("Example of a new window page for Automation Testing Practice")
        ).to_be_visible()
