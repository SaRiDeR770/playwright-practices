
import httpx

def test_check_health():
          response=httpx.get('https://practice.expandtesting.com/notes/api/health-check',         timeout=30)
          assert response.status_code == 200
          assert response.json()['success'] == True
