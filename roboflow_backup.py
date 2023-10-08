
from flask import Flask, jsonify, request
from pymongo import MongoClient
from os import getcwd, remove
import certifi
from flask_cors import CORS
from collections import Counter
import datetime
from roboflow import Roboflow
import shutil


rf = Roboflow(api_key="3qDkbkKGa9Wf7OkF4u4y")
project = rf.workspace().project("product-detection-tr3t3")
model = project.version(1).model

cluster = MongoClient("mongodb+srv://rex:13579007@cluster0.kku4atv.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=certifi.where())
db = cluster["product_data"]

def get_value(name, data):
    for d in data:
        if d == str(name):
            return data[d]['value'], data[d]['name']
    return '', ''

def run_inference():
    global model
    print('RUNNING PREDICTIONS AT ',datetime.datetime.now())
    outputs = model.predict("temp.jpg", confidence=50, overlap=40).json()
    print('PREDICTIONS FOUND AT ',datetime.datetime.now())

    things_found = []
    list_of_coords = []
    if outputs:
        for output in outputs['predictions']:
            x = int(output['x'])
            y = int(output['y'])
            width = int(output['width'])
            height = int(output['height'])

            x1 = x - (width/2)
            y1 = y - (height/2)
            x2 = x + (width/2)
            y2 = y + (height/2)

            list_of_coords.append((int(x1), int(y1), int(x2), int(y2)))
            things_found.append(output['class'])
        
    return things_found, list_of_coords

app = Flask(__name__)
CORS(app)

@app.route('/detect_products', methods=['POST'])
def run_cheating_module():
    try:
        remove('temp.jpg')
    except:
        pass

    print('STARTING AT ',datetime.datetime.now())

    if 'image' not in request.files:
        shutil.copy('default.jpg', 'temp.jpg')

    else:
        file = request.files['image']
        try:
            file.save('temp.jpg')
        except:
            return jsonify({'detail':'Invalid image type'})

    # model_name = request.form.get('ModelName')
  
    try:
        #Running detection on given image
        list_of_products, list_of_coords = run_inference()
    except:
        return jsonify({'Error':'Error running inference '})


    try:
        collec = db['model_datas']
        data = collec.find()

        product_values = {}
        for d in data:
            product_values[d['detection_id']] = {'value':d['value'], 'name': d['name']}
        
        products = []
        for product in list_of_products:
            products.append(get_value(product, product_values))
    
    except:
        return jsonify({'Error':'Error hitting database'})


    # try:
    if products != []:
        list_of_products_names = []
        list_of_products_values = []

        for product in products:
            list_of_products_values.append(product[0])
            list_of_products_names.append(product[1])
        
        if list_of_products_names:
            name_counts = Counter(list_of_products_names)
            temp = []
            # Format and print the results
            for name, count in name_counts.items():
                if count==1:
                    formatted_name = name
                else:
                    formatted_name = f"{count} x {name}"
                temp.append(formatted_name)

            list_of_products_names = sorted(temp)

        names = ''
        values = ''
        for name in list_of_products_names:
            names+=name+', '
        
        for value in list_of_products_values:
            values+=value+', '

        list_of_products_values = list_of_products_values[2:]
        list_of_products_names = list_of_products_names[2:]
        values = values[:-2]
        names = names[:-2]

    else:
        names = 'No products found'
        values = 'No products found'


    print('ENDED AT ',datetime.datetime.now())

    return jsonify({'Products values': values,'Products names': names, 'coords':list_of_coords})

    # except:
    #     return jsonify({'Error':'Error running manual stuff'})

@app.route("/fetch_model_names", methods=['GET'])
def fetch_model_data():
    collec = db['model_list']
    data = collec.find()

    result = []
    for d in data:
        result.append(d['name'])

    return jsonify({'modelNames':result})


@app.route("/hello")
def hello_world():
    return "Hello World! "+str(getcwd())


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
