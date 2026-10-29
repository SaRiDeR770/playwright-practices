from playwright.sync_api import Page

from config import settings


class BasePage:
    """Common behaviour for all page objects."""

    path: str = "/"

    def __init__(self, page: Page) -> None:
        self.page = page

    @property
    def url(self) -> str:
        return f"{settings.BASE_URL}{self.path}"

    def open(self) -> "BasePage":
        self.page.goto(self.url)
        return self
