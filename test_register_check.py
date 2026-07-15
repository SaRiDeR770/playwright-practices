import httpx

import allure

@allure.title('Создание заметки авторизованным пользователем')
def test_create_note(auth_token):
    with allure.step('Создаём заметку через POST /notes'):
        response = httpx.post('https://practice.expandtesting.com/notes/api/notes', headers={'x-auth-token': auth_token},
            json={
            'title': 'text',
            'description': 'Sozdana avtotestom',
            'category': 'Home'
        },  timeout=30
        ) 
    with allure.step('Проверяем статус и заголовок заметки'):
        assert response.status_code == 200
        assert response.json()['data']['title'] == 'text'
