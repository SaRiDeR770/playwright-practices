import allure
from playwright.sync_api import Page, expect

from pages import CheckboxPage


@allure.feature("Form elements")
class TestCheckboxes:
    @allure.title("Checkbox page opens with the expected title and default state")
    def test_default_state(self, page: Page):
        checkboxes = CheckboxPage(page).open()
        expect(page).to_have_url(checkboxes.url)
        expect(page).to_have_title(CheckboxPage.TITLE)
        expect(checkboxes.checkbox(1)).not_to_be_checked()
        expect(checkboxes.checkbox(2)).to_be_checked()

    @allure.title("Checkbox can be checked and unchecked")
    def test_toggle(self, page: Page):
        checkboxes = CheckboxPage(page).open()
        checkboxes.check(1)
        expect(checkboxes.checkbox(1)).to_be_checked()
        checkboxes.uncheck(1)
        expect(checkboxes.checkbox(1)).not_to_be_checked()
