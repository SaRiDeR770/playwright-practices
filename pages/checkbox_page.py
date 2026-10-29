from pages.base_page import BasePage


class CheckboxPage(BasePage):
    path = "/checkboxes"

    TITLE = "Check Boxes page for Automation Testing Practice"

    def checkbox(self, number: int):
        return self.page.get_by_label(f"Checkbox {number}")

    def check(self, number: int) -> "CheckboxPage":
        self.checkbox(number).check()
        return self

    def uncheck(self, number: int) -> "CheckboxPage":
        self.checkbox(number).uncheck()
        return self
