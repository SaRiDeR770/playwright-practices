"""Shared fixtures.

UI fixtures build on the `page` fixture from pytest-playwright.
API fixtures create a fresh user per test so tests never share state.
"""
import uuid
from collections.abc import Iterator

import allure
import pytest
from playwright.sync_api import Page

from api import NotesApiClient
from config import settings
from pages import LoginPage


# ---- helpers -----------------------------------------------------------


def unique_email() -> str:
    """A throwaway e-mail that is unique per call and never a real mailbox."""
    return f"qa.user+{uuid.uuid4().hex[:12]}@example.com"


# ---- UI ----------------------------------------------------------------


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page).open()


@pytest.fixture
def logged_in_page(login_page: LoginPage) -> Page:
    login_page.login(settings.UI_USERNAME, settings.UI_PASSWORD)
    return login_page.page


# ---- API ---------------------------------------------------------------


@pytest.fixture
def api_client() -> Iterator[NotesApiClient]:
    """Anonymous client, no token."""
    client = NotesApiClient()
    yield client
    client.close()


@pytest.fixture
def api_user() -> dict[str, str]:
    return {
        "name": "QA User",
        "email": unique_email(),
        "password": settings.API_USER_PASSWORD,
    }


@pytest.fixture
def auth_client(api_user: dict[str, str]) -> Iterator[NotesApiClient]:
    """Client authenticated as a freshly registered user.

    The user is deleted after the test so the practice server does not
    accumulate garbage accounts.
    """
    client = NotesApiClient()
    with allure.step(f"Register and log in as {api_user['email']}"):
        register = client.register(**api_user)
        assert register.status_code == 201, register.text
        login = client.login(api_user["email"], api_user["password"])
        assert login.status_code == 200, login.text
    yield client
    with allure.step("Clean up: delete the test user"):
        client.delete_account()
    client.close()


# ---- markers -----------------------------------------------------------


def pytest_collection_modifyitems(items):
    """Mark tests by folder so `pytest -m api` / `pytest -m ui` just work."""
    for item in items:
        path = str(item.fspath)
        if "/tests/api/" in path:
            item.add_marker(pytest.mark.api)
        elif "/tests/ui/" in path:
            item.add_marker(pytest.mark.ui)


# ---- reporting ---------------------------------------------------------


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach a screenshot to the Allure report when a UI test fails."""
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or not report.failed:
        return
    page: Page | None = item.funcargs.get("page")
    if page is not None:
        allure.attach(
            page.screenshot(full_page=True),
            name="screenshot_on_failure",
            attachment_type=allure.attachment_type.PNG,
        )
