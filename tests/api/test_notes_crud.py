"""End-to-end lifecycle of a note through the API.

One test walks the full path create -> read -> update -> delete and checks
after every step that the server state matches what was sent, not only
that the status code is 200.
"""
import allure
import pytest

from api import NotesApiClient


@allure.feature("Notes API")
@allure.story("Notes CRUD")
class TestNotesCrud:
    @allure.title("Note lifecycle: create, read, update, delete")
    def test_note_lifecycle(self, auth_client: NotesApiClient):
        with allure.step("Create a note"):
            response = auth_client.create_note(
                title="Buy milk", description="2 litres, lactose free", category="Home"
            )
            assert response.status_code == 200, response.text
            note = response.json()["data"]
            note_id = note["id"]
            assert note["title"] == "Buy milk"
            assert note["category"] == "Home"
            assert note["completed"] is False

        with allure.step("The note is returned by GET /notes/{id}"):
            response = auth_client.get_note(note_id)
            assert response.status_code == 200, response.text
            assert response.json()["data"]["id"] == note_id

        with allure.step("The note appears in the user's list"):
            response = auth_client.get_notes()
            assert response.status_code == 200, response.text
            ids = [n["id"] for n in response.json()["data"]]
            assert note_id in ids

        with allure.step("Update the note and mark it completed"):
            response = auth_client.update_note(
                note_id,
                title="Buy oat milk",
                description="1 litre",
                category="Personal",
                completed=True,
            )
            assert response.status_code == 200, response.text
            updated = response.json()["data"]
            assert updated["title"] == "Buy oat milk"
            assert updated["category"] == "Personal"
            assert updated["completed"] is True

        with allure.step("Updated values are persisted on the server"):
            persisted = auth_client.get_note(note_id).json()["data"]
            assert persisted == updated

        with allure.step("Delete the note"):
            response = auth_client.delete_note(note_id)
            assert response.status_code == 200, response.text

        with allure.step("Deleted note is no longer available"):
            response = auth_client.get_note(note_id)
            assert response.status_code == 404, response.text

    @allure.title("Creating a note with {case} is rejected with 400")
    @pytest.mark.parametrize(
        "case, title, description, category",
        [
            ("empty title", "", "desc", "Home"),
            ("too short title", "ab", "desc", "Home"),
            ("empty description", "Title", "", "Home"),
            ("unknown category", "Title", "desc", "Groceries"),
        ],
    )
    def test_create_note_validation(self, auth_client: NotesApiClient, case, title, description, category):
        response = auth_client.create_note(title, description, category)
        assert response.status_code == 400, response.text
        assert response.json()["success"] is False

    @allure.title("A user cannot read another user's note")
    def test_note_isolation_between_users(self, auth_client: NotesApiClient, api_user):
        with allure.step("User A creates a note"):
            note_id = auth_client.create_note("Private", "only mine", "Work").json()["data"]["id"]

        with allure.step("User B registers and logs in"):
            other = NotesApiClient()
            other_email = api_user["email"].replace("@", "+b@")
            assert other.register("Other User", other_email, api_user["password"]).status_code == 201
            assert other.login(other_email, api_user["password"]).status_code == 200

        try:
            with allure.step("User B gets 404 for user A's note"):
                response = other.get_note(note_id)
                assert response.status_code == 404, response.text
        finally:
            other.delete_account()
            other.close()
