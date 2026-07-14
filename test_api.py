import httpx
import time

import pytest

# def test_health_check():
#     response=httpx.get('https://practice.expandtesting.com/notes/api/health-check')
#     assert response.status_code == 200
#     body = response.json()
#     print(body)
#     assert body ['success'] == True

# def test_register_check():
#     email = f'sardor.saidov_{time.time()}@mail.ru'
#     httpx.post('https://practice.expandtesting.com/notes/api/users/register',
#       json={'name': 'Sardor', 'email': email, 'password': 'Secret123'})
#     response=httpx.post('https://practice.expandtesting.com/notes/api/users/login',         
#       json={'email': email, 'password': 'Secret123'})    
#     assert response.status_code == 200
#     token = response.json()['data']['token']
#     print('Token:', token)
#     response = httpx.get('https://practice.expandtesting.com/notes/api/users/profile', headers={'x-auth-token': token})
#     assert response.status_code == 200
#     assert response.json()['data']['email'] == email

# def test_negative_case():
#     email = f'sardor.saidov_{time.time()}@mail.ru'
#     httpx.post('https://practice.expandtesting.com/notes/api/users/register',
#       json={'name': 'Sardor', 'email': email, 'password': 'Secret123'})
#     response=httpx.post('https://practice.expandtesting.com/notes/api/users/login',         
#       json={'email': email, 'password': 'WRONG!@#'}, timeout= 30)    
#     assert response.status_code == 401

# def test_negative_case_1():
#     email = f'sardor.saidov_{time.time()}@mail.ru'
#     httpx.post('https://practice.expandtesting.com/notes/api/users/register',
#       json={'name': 'Sardor', 'email': email, 'password': 'Secret123'})
#     response=httpx.post('https://practice.expandtesting.com/notes/api/users/login',         
#       json={'password': 'WRONG!@#'}, timeout= 30)    
#     assert response.status_code == 400

# def test_negative_case_2():
#     email = f'sardor.saidov_{time.time()}@mail.ru'
#     response=httpx.post('https://practice.expandtesting.com/notes/api/users/login',         
#       json={'email': email, 'password': 'WRONG!@#'}, timeout= 30)    
#     assert response.status_code == 401

@pytest.mark.parametrize('email, password, expected_status', [
    (f'no_such_{time.time()}@mail.ru', 'Secret123', 401),  
    ('', 'Secret123', 400),                                 
    ('not-an-email', 'Secret123', 400),                     
    ('sardor@mail.ru', '', 400) ])
def test_login_negative(email, password, expected_status):
          response=httpx.post('https://practice.expandtesting.com/notes/api/users/login',         
          json={'email': email, 'password': password}, timeout=30)
          assert response.status_code == expected_status
