import allure
import pytest
from playwright.sync_api import Page, expect

from pages import DropdownPage


@allure.feature("Form elements")
class TestDropdown:
    @allure.title("Selected option is reflected in the dropdown value")
    def test_select_option(self, page: Page):
        dropdown = DropdownPage(page).open().select_option("2")
        expect(dropdown.dropdown).to_have_value("2")

    @allure.title("Elements per page can be set to {value}")
    @pytest.mark.parametrize("value", ["10", "20", "50", "100"])
    def test_elements_per_page(self, page: Page, value: str):
        dropdown = DropdownPage(page).open().select_elements_per_page(value)
        expect(dropdown.elements_per_page).to_have_value(value)

    @allure.title("Selection is not persisted after page reload")
    def test_selection_resets_on_reload(self, page: Page):
        dropdown = DropdownPage(page).open()
        dropdown.select_option("2")
        dropdown.select_elements_per_page("50")
        page.reload()
        expect(dropdown.dropdown).not_to_have_value("2")
        expect(dropdown.elements_per_page).not_to_have_value("50")
