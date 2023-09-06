import requests

try:
    response = requests.get("http://54.212.1.25/get_contact_support")
    if response.status_code == 200:
        # If the request was successful (status code 200), you can access the content
        data = response.text
        return data
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
