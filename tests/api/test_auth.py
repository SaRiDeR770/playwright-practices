import allure
import pytest

from api import NotesApiClient
from config import settings


@allure.feature("Notes API")
@allure.story("Authentication")
class TestAuth:
    @allure.title("A registered user can log in and read their own profile")
    def test_register_login_profile(self, api_client: NotesApiClient, api_user: dict):
        with allure.step("Register"):
            response = api_client.register(**api_user)
            assert response.status_code == 201, response.text
            assert response.json()["data"]["email"] == api_user["email"]

        with allure.step("Log in"):
            response = api_client.login(api_user["email"], api_user["password"])
            assert response.status_code == 200, response.text
            assert api_client.token, "Login response must contain a token"

        with allure.step("Profile matches the registered data"):
            response = api_client.profile()
            assert response.status_code == 200, response.text
            profile = response.json()["data"]
            assert profile["email"] == api_user["email"]
            assert profile["name"] == api_user["name"]

        with allure.step("Clean up"):
            api_client.delete_account()

    @allure.title("Registering the same e-mail twice is rejected")
    def test_duplicate_registration(self, auth_client: NotesApiClient, api_user: dict):
        response = auth_client.register(**api_user)
        assert response.status_code == 409, response.text
        assert "already exists" in response.json()["message"].lower()

    # Parametrize values must be identical in every xdist worker, so no
    # random data here: this address is never registered by the suite.
    UNKNOWN_EMAIL = "nobody.registered.here@example.com"

    @allure.title("Login with {case} returns {expected_status}")
    @pytest.mark.parametrize(
        "case, email, password, expected_status",
        [
            ("unknown user", UNKNOWN_EMAIL, settings.API_USER_PASSWORD, 401),
            ("empty e-mail", "", settings.API_USER_PASSWORD, 400),
            ("malformed e-mail", "not-an-email", settings.API_USER_PASSWORD, 400),
            ("empty password", UNKNOWN_EMAIL, "", 400),
        ],
    )
    def test_login_negative(self, api_client: NotesApiClient, case, email, password, expected_status):
        response = api_client.login(email, password)
        assert response.status_code == expected_status, response.text
        assert response.json()["success"] is False

    @allure.title("Protected endpoint rejects a request without a token")
    def test_profile_requires_token(self, api_client: NotesApiClient):
        response = api_client.profile()
        assert response.status_code == 401, response.text

    @allure.title("Token stops working after logout")
    def test_token_invalid_after_logout(self, auth_client: NotesApiClient):
        assert auth_client.logout().status_code == 200
        response = auth_client.profile()
        assert response.status_code == 401, response.text
