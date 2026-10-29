# Playwright + Python test framework

[![Tests](https://github.com/SaRiDeR770/playwright-practices/actions/workflows/tests.yml/badge.svg)](https://github.com/SaRiDeR770/playwright-practices/actions/workflows/tests.yml)
[![Allure report](https://img.shields.io/badge/Allure-report-orange)](https://sarider770.github.io/playwright-practices/)

UI and API test suite for the public demo site [practice.expandtesting.com](https://practice.expandtesting.com),
built the way I build suites at work: Page Object Model, a thin API client, isolated test data,
Allure reporting with screenshots and traces on failure, and a CI pipeline that publishes the report.

## What is covered

| Layer | What | Where |
|---|---|---|
| UI | Login (positive, 4 negative cases, session cookie) | `tests/ui/test_login.py` |
| UI | Checkboxes, dropdowns, state after reload | `tests/ui/test_checkboxes.py`, `test_dropdown.py` |
| UI | Password reset form | `tests/ui/test_forgot_password.py` |
| UI | Hover, iframe input, new window | `tests/ui/test_browser_interactions.py` |
| UI + API | Notes app: data created via API, verified in the UI, category filter | `tests/ui/test_notes_app.py` |
| UI (mocked) | Notes app with `page.route`: list rendering, empty state, backend error — no server calls | `tests/ui/test_notes_app.py` |
| API | Health check | `tests/api/test_health.py` |
| API | Register, login, profile, logout, duplicate e-mail, 4 negative login cases, auth required | `tests/api/test_auth.py` |
| API | Full note lifecycle create → read → update → delete, input validation, isolation between users | `tests/api/test_notes_crud.py` |

Every API test registers its own user and deletes it afterwards, so tests never share state and the whole suite runs in parallel (`pytest -n 4`, ~1 minute).

## Stack

Python 3.12 · Playwright · Pytest · httpx · Allure · GitHub Actions

## Project structure

```
├── api/                 # HTTP client for the Notes API (no test logic inside)
│   └── notes_client.py
├── config/
│   └── settings.py      # URLs, credentials, timeouts; all overridable via env / .env
├── pages/               # Page Object Model
│   ├── base_page.py
│   ├── login_page.py
│   ├── checkbox_page.py
│   ├── dropdown_page.py
│   ├── forgot_password_page.py
│   └── notes_app_page.py   # data-testid based locators
├── tests/
│   ├── conftest.py      # fixtures, auto markers, screenshot on failure
│   ├── ui/
│   └── api/
├── .github/workflows/tests.yml
├── pytest.ini
└── requirements.txt
```

## Run locally

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium

pytest                 # everything
pytest -m api          # API only, no browser needed
pytest -m ui --headed  # watch the browser
pytest -n 4            # parallel
```

Allure report:

```bash
allure serve allure-results
```

To run against another environment, copy `.env.example` to `.env` and change the values.

## CI

`.github/workflows/tests.yml` runs on every push and pull request, weekly on schedule, and on demand:

1. installs Python and Chromium
2. runs the whole suite in parallel
3. on failure uploads Playwright traces, videos and screenshots as artifacts
4. builds the Allure report with history and publishes it to GitHub Pages

## Conventions

- Tests assert on behaviour, not only on status codes: after an update the record is re-read and compared with what was sent.
- Negative cases are parametrized with readable ids so the report shows exactly which input failed.
- `@allure.id` ties an autotest to the manual test case in the TMS, so coverage is tracked case by case.
- Every test is an Allure step-by-step report; screenshots, video and trace are attached on failure.
- Backend can be mocked with `page.route` for frontend-only checks that must be repeatable and independent of server state.
- No personal data in the repo: throwaway e-mails are generated per test, credentials come from config.
- Page objects expose locators as properties and actions as methods that return `self`, so tests read as a chain.
- Locator priority: `data-testid` → role/label → CSS. XPath and text-based locators are a last resort because they break on copy and layout changes.

## Professional background

This is a demo suite on a public site. At work I maintain a Playwright + Python suite of 340+ UI autotests
across several domains of a bank's website, about 100 of them fully localized. Locators are bound to
`data-testid` attributes agreed with the frontend team, so tests survive layout and copy changes.
That code belongs to the employer; this repository shows the same approach on an open target.
