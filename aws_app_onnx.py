import os
import cv2
from flask import Flask, jsonify, request
from pymongo import MongoClient
from os import getcwd
import certifi
from flask_cors import CORS
from yolov8 import YOLOv8

BASE_DIR = getcwd()
model = None
class_names = None
loaded_model = None

cluster = MongoClient("mongodb+srv://rex:13579007@cluster0.kku4atv.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=certifi.where())
db = cluster["product_data"]

def get_value(name, data):
    for d in data:
        if d == str(name):
            return data[d]['value'], data[d]['name']
    return '', ''

def run_inference(model):
    global class_names
    image = cv2.imread(BASE_DIR+'/temp.png')
    boxes, scores, class_ids = model(image)

    things_found = []
    list_of_coords = []

    for box, score, class_id in zip(boxes, scores, class_ids):
        x1, y1, x2, y2 = box.astype(int)
        list_of_coords.append((x1, y1, x2, y2))
        name = class_names[class_id]
        text = name+' '+str(round(score,2))

        cv2.rectangle(image,(x1,y1),(x2,y2),(0,255,0),1)
        cv2.putText(image,text,(x1,y1-5),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,255,0),1)

        things_found.append(name)
    
    return image, things_found

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

    model_name = request.form.get('ModelName')
    print(model_name)
    model_name = 'CakeShop'

    #Loading model
    if not model_name:
        return jsonify({'Error':'Model name not found'})
    
    model_path = BASE_DIR+'/model/'+model_name+'.onnx'
    
    if not os.path.exists(model_path):
        return jsonify({'Error':BASE_DIR+'/model/'+model_name+'.onnx'+' such name does not exist'})

    
    if loaded_model != model_name:
        model = YOLOv8(model_path, conf_thres=0.3, iou_thres=0.4)
        with open(BASE_DIR+'/model/'+model_name+'.txt', "r") as file:
            class_names = [line.strip() for line in file.readlines()]
        loaded_model = model_name

    try:
        #Running detection on given image
        img,list_of_products, list_of_coords = run_inference(model)
    except:
        return jsonify({'Error':'Error running inference ', 'MODEL NAME':model_name, 'LOADED MODEL NAME':loaded_model})


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


    try:
        list_of_products_names = ''
        list_of_products_values = ''

        for product in products:
            list_of_products_values+=', '+str(product[0])
            list_of_products_names+=', '+str(product[1])

        if products!=[]:
            list_of_products_values = list_of_products_values[2:]
            list_of_products_names = list_of_products_names[2:]
        else:
            list_of_products_values = 'No products found'
            list_of_products_names = 'No products found'

        cv2.imwrite(BASE_DIR+'/output.png',img)
        os.remove(BASE_DIR+'/temp.png')
        return jsonify({'Products values': list_of_products_values,'Products names': list_of_products_names, 'coords':list_of_coords})

        
    except:
        return jsonify({'Error':'Error running manual stuff'})

@app.route("/hello")
def hello_world():
    return "Hello World! "+str(getcwd())


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
