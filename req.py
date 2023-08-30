import requests

d = requests.get('http://54.212.1.25/fetch_all_data')

print(type(d.text))