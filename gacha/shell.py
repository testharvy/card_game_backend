import requests

url = 'http://127.0.0.1:8000/api/api-token-auth/'

headers = {'username': 'testharvy', 'password': '123'}
# headers = {'Authorization': 'Token 9054f7aa9305e012b3c2300408c3dfdf390fcddf'}
r = requests.get(url, headers=headers)



curl

curl -X POST -d "token=887c1caa3d7369bbbb35a1e328b6d6d1a48a1c88" http://127.0.0.1:8000/api/me/

curl -X POST -H 'Authorization: Token 887c1caa3d7369bbbb35a1e328b6d6d1a48a1c88' http://127.0.0.1:8000/api/me/


curl -X POST http://127.0.0.1:8000/api/me/ -H 'Authorization: Token 887c1caa3d7369bbbb35a1e328b6d6d1a48a1c88'
