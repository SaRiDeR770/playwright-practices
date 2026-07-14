import httpx

def test_create_note(auth_token):
    response = httpx.post('https://practice.expandtesting.com/notes/api/notes', headers={'x-auth-token': auth_token},
            json={
            'title': 'text',
            'description': 'Sozdana avtotestom',
            'category': 'Home'
        },  timeout=30
        )
   
    print (response.json())
    assert response.status_code == 200
    assert response.json()['data']['title'] == 'text'
