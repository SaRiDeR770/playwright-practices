from pages.base_page import BasePage


class DropdownPage(BasePage):
    path = "/dropdown"

    @property
    def dropdown(self):
        return self.page.locator("#dropdown")

    @property
    def elements_per_page(self):
        return self.page.locator("#elementsPerPageSelect")

    def select_option(self, value: str) -> "DropdownPage":
        self.dropdown.select_option(value)
        return self

    def select_elements_per_page(self, value: str) -> "DropdownPage":
        self.elements_per_page.select_option(value)
        return self
