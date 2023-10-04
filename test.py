import os
import cv2
from flask import Flask, jsonify, request
from pymongo import MongoClient
from os import getcwd
import certifi
from flask_cors import CORS
from collections import Counter
from yolov8 import YOLOv8

BASE_DIR = getcwd()
model = None
loaded_model = None
model = YOLOv8('model/CakeShop.onnx', conf_thres=0.3, iou_thres=0.4)
with open('model/CakeShop.txt', "r") as file:
    class_names = [line.strip() for line in file.readlines()]

cluster = MongoClient("mongodb+srv://rex:13579007@cluster0.kku4atv.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=certifi.where())
db = cluster["product_data"]

def get_value(name, data):
    for d in data:
        if d == str(name):
            return data[d]['value'], data[d]['name']
    return '', ''

def run_inference():
    global class_names, model
    image = cv2.imread(BASE_DIR+'/temp.png')
    boxes, scores, class_ids = model(image)

    things_found = []
    list_of_coords = []

    for box, score, class_id in zip(boxes, scores, class_ids):
        x1, y1, x2, y2 = box.astype(int)
        list_of_coords.append((int(x1), int(y1), int(x2), int(y2)))
        name = class_names[class_id]
        text = name+' '+str(round(score,2))

        cv2.rectangle(image,(x1,y1),(x2,y2),(0,255,0),1)
        cv2.putText(image,text,(x1,y1-5),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,255,0),1)

        things_found.append(name)
    
    return things_found, list_of_coords

app = Flask(__name__)
CORS(app)

@app.route('/detect_products', methods=['POST'])
def run_cheating_module():
    global model, class_names, loaded_model

    if 'image' not in request.files:
        return jsonify({'detail':'Image not found'})

    file = request.files['image']

    # check if file is empty
    if file.filename == '':
        return jsonify({'detail':'Image not selected'})
    
    try:
        # save video file to disk
        file.save('temp.png')
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

    else:
        names = 'No products found'
        values = 'No products found'

    os.remove(BASE_DIR+'/temp.png')

    print(type(list_of_coords))
    return jsonify({'coords':list_of_coords})

@app.route("/hello")
def hello_world():
    return "Hello World! "+str(getcwd())


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
