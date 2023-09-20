import os
import cv2
from flask import Flask, jsonify, request
from pymongo import MongoClient
from os import getcwd
import certifi
from flask_cors import CORS
from bson import ObjectId
from yolov8 import YOLOv8
import requests

BASE_DIR = getcwd()
model = None
class_names = None
loaded_model = None

# # Construct the download link
# download_link = 'https://drive.usercontent.google.com/download?id=1QZXRbrps8SjcR_5R2ClnxlsgpX5a4M3Q&export=download&authuser=0&confirm=t&uuid=3bccbcab-6202-4aa1-8cf5-6d0c7b0ae68d&at=APZUnTWek41_WXKrPgaFIaUh4-GC:1695222256618'
# print('Downloading model')
# response = requests.get(download_link)

# if response.status_code == 200:
#     with open('model/CakeShop.onnx', 'wb') as file:
#         file.write(response.content)
#     print("Model downloaded successfully.")
# else:
#     print(f"Failed to download the model. HTTP status code: {response.status_code}")


cluster = MongoClient("mongodb+srv://rex:13579007@cluster0.kku4atv.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=certifi.where())
db = cluster["product_data"]

def get_value(name, data):
    for d in data:
        if d == str(name):
            return data[d]['value'], data[d]['name']
    return '', ''

app = Flask(__name__)
CORS(app)  # Allow CORS for all routes

def run_inference(model):
    global class_names
    image = cv2.imread(BASE_DIR+'/temp.png')
    boxes, scores, class_ids = model(image)

    things_found = []

    for box, score, class_id in zip(boxes, scores, class_ids):
        x1, y1, x2, y2 = box.astype(int)
        name = class_names[class_id]
        text = name+' '+str(round(score,2))

        cv2.rectangle(image,(x1,y1),(x2,y2),(0,255,0),1)
        cv2.putText(image,text,(x1,y1-5),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,255,0),1)

        things_found.append(name)
    
    return image, things_found

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
        img,list_of_products = run_inference(model)
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
        return jsonify({'Products values':list_of_products_values, 'Products names': list_of_products_names})

        
    except:
        return jsonify({'Error':'Error running manual stuff'})

@app.route("/fetch_all_data", methods=['GET'])
def fetch_data():
    collec = db['model_datas']
    data = collec.find()
    result = []
    for d in data:
        result.append({
            'id': str(d['_id']),
            'name': d['name'],
            'value': d['value'],
            'ModelName': d['ModelName']
        })

    return jsonify(result)

@app.route("/fetch_model_names", methods=['GET'])
def fetch_model_data():
    collec = db['model_list']
    data = collec.find()

    result = []
    for d in data:
        result.append(d['name'])

    return jsonify({'modelNames':result})

@app.route("/fetch_single_data/<string:id_value>", methods=['GET'])
def get_single_data(id_value):
    collec = db['model_datas']
    output = collec.find_one({'_id':ObjectId(id_value)})
    if output:
        output['_id'] = str(output['_id'])
        return (output)

    return jsonify({'detail':'not found'})

@app.route("/update_data/<string:id_value>/<string:new_value>", methods=['GET'])
def update_user_data(id_value,new_value):
    collec = db['model_datas']
    print('VALUE ',new_value)

    output = collec.find_one({'_id':ObjectId(id_value)})
    if not output:
        return jsonify({'Error':'Invalid id'})

    # Define the filter to identify the document to be updated
    filter_criteria = {"_id": ObjectId(id_value)}

    # Define the update operation
    update_operation = {"$set": {"value": new_value}}

    # Perform the update
    result = collec.update_one(filter_criteria, update_operation)

    print("Modified documents:", result.modified_count)

    return jsonify({'detail':'success'})

@app.route("/get_contact_support", methods=['GET'])
def get_contact():
    collec = db['contact']
    output = collec.find()

    res = ''
    for document in output:
        for entry in document:
            if entry == '_id':
                continue

            res+='   |   '+entry.capitalize()+': '+document[entry]
        break

    if res != '':
        res = res[5:]

    return jsonify({'contact':res})

@app.route("/hello")
def hello_world():
    return "Hello World! "+str(getcwd())


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
