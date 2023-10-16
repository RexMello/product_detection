from flask import Flask, jsonify, request
from pymongo import MongoClient
from os import getcwd
import certifi
from flask_cors import CORS
import requests

cluster = MongoClient("mongodb+srv://rex:13579007@cluster0.kku4atv.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=certifi.where())
db = cluster["product_data"]

def get_value(name, data):
    for d in data:
        if d == str(name):
            return data[d]['value'], data[d]['name']
    return '', ''

app = Flask(__name__)
CORS(app)

@app.route('/detect_products', methods=['POST'])
def run_cheating_module():
    if 'image' not in request.files:
        return jsonify({'detail':'Image not found'})

    file = request.files['image']
    if file.filename == '':
        return jsonify({'detail':'Image not selected'})
    
    try:
        file.save('temp.jpg')
    except:
        return jsonify({'detail':'Invalid image type'})

    model_name = request.form.get('ModelName')
    app_url = "http://52.77.228.23/detect_products"
    image_file = "temp.jpg"
    files = {
        'image': ('image.jpg', open(image_file, 'rb')),
        'ModelName': (None, model_name),
    }

    response = requests.post(app_url, files=files)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return jsonify({"Error:", response.text})

@app.route("/hello")
def hello_world():
    return "Hello World! "+str(getcwd())


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)

