import pytest
import httpx
import time
from playwright.sync_api import Page
from login_page import LoginPage

@pytest.fixture
def logged_in_page(page: Page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("practice", "SuperSecretPassword!")
    return page

@pytest.fixture
def auth_token():
    email = f'sardor.saidov_{time.time()}@mail.ru'
    httpx.post('https://practice.expandtesting.com/notes/api/users/register',
      json={'name': 'Sardor', 'email': email, 'password': 'Secret123'})
    response=httpx.post('https://practice.expandtesting.com/notes/api/users/login',         
      json={'email': email, 'password': 'Secret123'})    
    assert response.status_code == 200
    return response.json()['data']['token']