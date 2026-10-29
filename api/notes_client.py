"""Thin client for the Notes API of practice.expandtesting.com.

Every method returns the raw httpx.Response so tests can assert on
status code, headers and body themselves. The client only knows URLs
and authentication, not test logic.
"""
from __future__ import annotations

import httpx

from config import settings


class NotesApiClient:
    def __init__(self, base_url: str = settings.API_URL, token: str | None = None) -> None:
        self.base_url = base_url.rstrip("/")
        self.token = token
        self._client = httpx.Client(base_url=self.base_url, timeout=settings.REQUEST_TIMEOUT)

    # ---- helpers -------------------------------------------------------

    @property
    def _auth_headers(self) -> dict[str, str]:
        return {"x-auth-token": self.token} if self.token else {}

    def close(self) -> None:
        self._client.close()

    # ---- system --------------------------------------------------------

    def health_check(self) -> httpx.Response:
        return self._client.get("/health-check")

    # ---- users ---------------------------------------------------------

    def register(self, name: str, email: str, password: str) -> httpx.Response:
        return self._client.post(
            "/users/register",
            json={"name": name, "email": email, "password": password},
        )

    def login(self, email: str, password: str) -> httpx.Response:
        response = self._client.post("/users/login", json={"email": email, "password": password})
        if response.status_code == 200:
            self.token = response.json()["data"]["token"]
        return response

    def profile(self) -> httpx.Response:
        return self._client.get("/users/profile", headers=self._auth_headers)

    def logout(self) -> httpx.Response:
        return self._client.delete("/users/logout", headers=self._auth_headers)

    def delete_account(self) -> httpx.Response:
        return self._client.delete("/users/delete-account", headers=self._auth_headers)

    # ---- notes ---------------------------------------------------------

    def create_note(self, title: str, description: str, category: str) -> httpx.Response:
        return self._client.post(
            "/notes",
            headers=self._auth_headers,
            json={"title": title, "description": description, "category": category},
        )

    def get_notes(self) -> httpx.Response:
        return self._client.get("/notes", headers=self._auth_headers)

    def get_note(self, note_id: str) -> httpx.Response:
        return self._client.get(f"/notes/{note_id}", headers=self._auth_headers)

    def update_note(
        self, note_id: str, title: str, description: str, category: str, completed: bool
    ) -> httpx.Response:
        return self._client.put(
            f"/notes/{note_id}",
            headers=self._auth_headers,
            json={
                "title": title,
                "description": description,
                "category": category,
                "completed": completed,
            },
        )

    def delete_note(self, note_id: str) -> httpx.Response:
        return self._client.delete(f"/notes/{note_id}", headers=self._auth_headers)
