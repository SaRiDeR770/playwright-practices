from pages.base_page import BasePage


class ForgotPasswordPage(BasePage):
    path = "/forgot-password"

    SUCCESS_MESSAGE = (
        "An e-mail has been sent to you which explains how to reset your password."
    )

    @property
    def email_input(self):
        return self.page.get_by_label("E-mail")

    @property
    def submit_button(self):
        return self.page.get_by_role("button", name="Retrieve password")

    def request_reset(self, email: str) -> "ForgotPasswordPage":
        self.email_input.fill(email)
        self.submit_button.click()
        return self
