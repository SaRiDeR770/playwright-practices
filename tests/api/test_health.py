import allure

from api import NotesApiClient


@allure.feature("Notes API")
@allure.title("Health check endpoint reports the service is up")
def test_health_check(api_client: NotesApiClient):
    response = api_client.health_check()
    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["status"] == 200
