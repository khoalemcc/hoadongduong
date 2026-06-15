import requests, json

BASE_URL = 'http://localhost:8000'

def login(email, password):
    data = {'username': email, 'password': password}
    resp = requests.post(f'{BASE_URL}/auth/login', data=data)
    print('Login status:', resp.status_code)
    if resp.status_code != 200:
        print('Login failed:', resp.text)
        return None
    token_data = resp.json()
    return token_data.get('access_token')

def get_my_orders(token):
    headers = {'Authorization': f'Bearer {token}'}
    resp = requests.get(f'{BASE_URL}/orders/my-orders', headers=headers)
    print('My-orders status:', resp.status_code)
    print('Response body:', resp.text)

if __name__ == '__main__':
    token = login('khoale.mcc@gmail.com', '1234')
    if token:
        get_my_orders(token)
