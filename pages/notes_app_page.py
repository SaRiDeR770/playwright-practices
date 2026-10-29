"""Page object for the Notes React app (/notes/app).

All locators use data-testid attributes exposed by the frontend, so they
survive copy and layout changes.
"""
from pages.base_page import BasePage


class NotesLoginPage(BasePage):
    path = "/notes/app/login"

    @property
    def email_input(self):
        return self.page.get_by_test_id("login-email")

    @property
    def password_input(self):
        return self.page.get_by_test_id("login-password")

    @property
    def submit_button(self):
        return self.page.get_by_test_id("login-submit")

    @property
    def alert(self):
        return self.page.get_by_test_id("alert-message")

    def login(self, email: str, password: str) -> "NotesPage":
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.submit_button.click()
        return NotesPage(self.page)


class NotesPage(BasePage):
    path = "/notes/app"

    @property
    def notes_list(self):
        return self.page.get_by_test_id("notes-list")

    @property
    def note_cards(self):
        return self.page.get_by_test_id("note-card")

    @property
    def no_notes_message(self):
        return self.page.get_by_test_id("no-notes-message")

    @property
    def logout_button(self):
        return self.page.get_by_test_id("logout")

    def card_titles(self) -> list[str]:
        return [t.strip() for t in self.page.get_by_test_id("note-card-title").all_inner_texts()]

    def card_descriptions(self) -> list[str]:
        return [t.strip() for t in self.page.get_by_test_id("note-card-description").all_inner_texts()]

    def select_category(self, category: str) -> "NotesPage":
        self.page.get_by_test_id(f"category-{category.lower()}").click()
        return self
