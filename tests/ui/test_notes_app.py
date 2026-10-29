"""Notes React app: real end-to-end flow and a fully mocked flow.

Two ways to test the same screen:

* `TestNotesAppE2E` talks to the real backend. Test data is created through
  the API (fast, deterministic) and verified through the UI (what the user sees).
* `TestNotesAppMocked` intercepts every API call with `page.route`. No backend
  is touched, so these tests can run on any branch, any number of times, in
  parallel, and they still fail if the frontend stops rendering the data.
"""
import json

import allure
from playwright.sync_api import Page, Route, expect

from api import NotesApiClient
from config import settings
from pages import NotesLoginPage, NotesPage


@allure.feature("Notes app")
@allure.story("End-to-end with real backend")
class TestNotesAppE2E:
    @allure.title("Notes created via API are shown in the UI after login")
    def test_api_created_notes_are_visible(
        self, page: Page, auth_client: NotesApiClient, api_user: dict
    ):
        with allure.step("Prepare data through the API"):
            for title, category in [("Pay rent", "Home"), ("Standup notes", "Work")]:
                response = auth_client.create_note(title, f"{title} description", category)
                assert response.status_code == 200, response.text

        with allure.step("Log in through the UI"):
            notes = NotesLoginPage(page).open().login(api_user["email"], api_user["password"])
            expect(page).to_have_url(f"{settings.BASE_URL}/notes/app")

        with allure.step("Both notes are rendered"):
            expect(notes.note_cards).to_have_count(2)
            assert sorted(notes.card_titles()) == ["Pay rent", "Standup notes"]

        with allure.step("Category filter shows only matching notes"):
            notes.select_category("Work")
            expect(notes.note_cards).to_have_count(1)
            assert notes.card_titles() == ["Standup notes"]

    @allure.title("Wrong password shows an error and keeps the user on the login page")
    def test_login_wrong_password(self, page: Page, api_user: dict):
        login = NotesLoginPage(page).open()
        login.login(api_user["email"], "wrong-password")
        expect(login.alert).to_have_text("Incorrect email address or password")
        expect(page).to_have_url(f"{settings.BASE_URL}/notes/app/login")


@allure.feature("Notes app")
@allure.story("Mocked backend")
class TestNotesAppMocked:
    """The frontend is real, the API is faked. Nothing is written to the server."""

    FAKE_TOKEN = "mocked-token"
    FAKE_NOTES = [
        {
            "id": "1",
            "title": "Mocked note one",
            "description": "Rendered from a stubbed response",
            "category": "Home",
            "completed": False,
            "created_at": "2026-01-01T10:00:00.000Z",
            "updated_at": "2026-01-01T10:00:00.000Z",
            "user_id": "u1",
        },
        {
            "id": "2",
            "title": "Mocked note two",
            "description": "No backend involved",
            "category": "Work",
            "completed": True,
            "created_at": "2026-01-02T10:00:00.000Z",
            "updated_at": "2026-01-02T10:00:00.000Z",
            "user_id": "u1",
        },
    ]

    @staticmethod
    def _json(route: Route, status: int, payload: dict) -> None:
        route.fulfill(
            status=status,
            content_type="application/json",
            body=json.dumps(payload),
        )

    def _mock_backend(self, page: Page, notes: list[dict]) -> None:
        page.route(
            "**/notes/api/users/login",
            lambda route: self._json(
                route, 200, {"success": True, "status": 200, "data": {"token": self.FAKE_TOKEN}}
            ),
        )
        page.route(
            "**/notes/api/notes",
            lambda route: self._json(route, 200, {"success": True, "status": 200, "data": notes}),
        )

    @allure.title("Notes list renders every note from the API response")
    def test_notes_list_renders_mocked_notes(self, page: Page):
        self._mock_backend(page, self.FAKE_NOTES)

        notes = NotesLoginPage(page).open().login("any@example.com", "any-password")

        expect(notes.note_cards).to_have_count(len(self.FAKE_NOTES))
        assert notes.card_titles() == [n["title"] for n in self.FAKE_NOTES]
        assert notes.card_descriptions() == [n["description"] for n in self.FAKE_NOTES]

    @allure.title("Empty notes list shows the placeholder message")
    def test_empty_state(self, page: Page):
        self._mock_backend(page, [])

        notes = NotesLoginPage(page).open().login("any@example.com", "any-password")

        expect(notes.no_notes_message).to_be_visible()
        expect(notes.note_cards).to_have_count(0)

    @allure.title("Backend 401 on login is shown to the user as an error")
    def test_backend_error_is_surfaced(self, page: Page):
        page.route(
            "**/notes/api/users/login",
            lambda route: self._json(
                route, 401, {"success": False, "status": 401, "message": "Incorrect email address or password"}
            ),
        )

        login = NotesLoginPage(page).open()
        login.login("any@example.com", "any-password")

        expect(login.alert).to_have_text("Incorrect email address or password")
