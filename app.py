import cv2
from flask import Flask, jsonify, request
from pymongo import MongoClient
from os import getcwd
import certifi
from flask_cors import CORS
from bson import ObjectId
import requests

BASE_DIR = getcwd()
model = None
loaded_model = ''


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
    image = cv2.imread(BASE_DIR+'/temp.png')
    results = model.predict(image, conf=0.4)
    
    things_found = []

    for r in results:
        boxes = r.boxes

        for box in boxes:
            thing_found = model.names[int(box.cls)]
            things_found.append(thing_found)

            confidence = box.conf.item()
            b = box.xyxy[0]
            c = box.cls

            x1,y1,x2,y2 = int(b[0].item()),int(b[1].item()),int(b[2].item()), int(b[3].item())
            cv2.rectangle(image,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.putText(image,thing_found+' '+str(round(confidence,2)),(x1,y1-5),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,255,0),1)

    return image, things_found

@app.route('/detect_products', methods=['POST'])
def run_cheating_module_2():
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

    #Loading model
    if not model_name:
        return jsonify({'Error':'Model name not found'})
    

    url = "http://35.87.28.188/detect_products"

    # Define the form data parameters
    form_data = {
        "ModelName": model_name,
    }

    files = {
        "image": ("temp.png", open('temp.png', "rb"))
    }

    try:
        response = requests.post(url, data=form_data, files=files)

        if response.status_code == 200:
            # If the request was successful (status code 200), you can access the response content
            return response.json()
        else:
            return jsonify({'Error':f"Failed to fetch data. Status code: {response.status_code}"})
    except requests.exceptions.RequestException as e:
        return jsonify({'Error':"An error occurred: "+e})

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
