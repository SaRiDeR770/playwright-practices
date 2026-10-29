"""Project settings.

Every value can be overridden with an environment variable (see .env.example),
so the same suite runs locally, in CI and against another environment
without touching the code.
"""
import os

from dotenv import load_dotenv

load_dotenv()

BASE_URL: str = os.getenv("BASE_URL", "https://practice.expandtesting.com")
API_URL: str = os.getenv("API_URL", f"{BASE_URL}/notes/api")

# Demo credentials of the public practice site
UI_USERNAME: str = os.getenv("UI_USERNAME", "practice")
UI_PASSWORD: str = os.getenv("UI_PASSWORD", "SuperSecretPassword!")

# Default password for API users created on the fly
API_USER_PASSWORD: str = os.getenv("API_USER_PASSWORD", "Secret123!")

REQUEST_TIMEOUT: float = float(os.getenv("REQUEST_TIMEOUT", "30"))
