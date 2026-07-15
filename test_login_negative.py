from playwright.sync_api import Page, expect
import allure

@allure.title('Невалидный логиy')
def test_login (page: Page):
 with allure.step('Оставить поле "username" пустым'):
    page.goto('https://practice.expandtesting.com/login')
    login = page.get_by_label('Username')
    login.fill('')
    password = page.get_by_label('Password')
    password.fill('SuperSecretPassword!')
    page.get_by_role('button', name = 'Login').click()
 with allure.step('Проверяем статус'):
    expect(page.get_by_text('Your username is invalid!')).to_be_visible()
