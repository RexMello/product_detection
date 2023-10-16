import requests

# URL of the Flask app's `/detect_products` endpoint
app_url = "http://192.168.100.5:5000/detect_products"

# File path to the image you want to send for detection
image_file = "temp.jpg"

# Optional: Model name
model_name = "CakeShop"

# Create a dictionary with the file and model name (if needed)
files = {
    'image': ('image.jpg', open(image_file, 'rb')),
    'ModelName': (None, model_name),
}

# Send a POST request to the Flask app's /detect_products endpoint
response = requests.post(app_url, files=files)

# Check the response from the server
if response.status_code == 200:
    data = response.json()
    print("Products names:", data['Products names'])
    print("Products values:", data['Products values'])
    print("Coordinates:", data['coords'])
else:
    print("Error:", response.text)
