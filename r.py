import requests

url = "http://35.87.28.188/detect_products"

# Define the form data parameters
form_data = {
    "ModelName": 'CakeShop',
}

files = {
    "image": ("temp.png", open('temp.png', "rb"))
}

try:
    response = requests.post(url, data=form_data, files=files)

    if response.status_code == 200:
        # If the request was successful (status code 200), you can access the response content
        print(response.json())
    else:
        print({'Error':f"Failed to fetch data. Status code: {response.status_code}"})
except requests.exceptions.RequestException as e:
    print({'Error':"An error occurred: "+str(e)})