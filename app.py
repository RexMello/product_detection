import cv2
from flask import Flask, request, jsonify
from pymongo import MongoClient
from ultralytics import YOLO
import os
import certifi
from flask_cors import CORS
from bson import ObjectId
import base64

try:
    os.remove('model_name.txt')
except:
    pass

with open('model_name.txt','w') as w:
    w.write('')

model = None

cluster = MongoClient("mongodb+srv://kai:13579007@cluster0.wacwe.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=certifi.where())
db = cluster["product_data"]

def get_value(name, data):
    for d in data:
        if d['detection_id'] == str(name):
            return d['value']
    return ''

app = Flask(__name__)
CORS(app)  # Allow CORS for all routes

def run_inference(model):
    image = cv2.imread('temp.png')
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

@app.route('/detect_products/<string:image>', methods=['GET'])
def run_cheating_module(image):
    # check if request has file part
    if not image:
        return jsonify({'Error':'No image found'})

    image = image.replace('!','/')

    image = image.split('base64,')[1]
    #decode base64 string data
    decoded_data=base64.b64decode((image))

    #write the decoded data back to original format in  file
    img_file = open('temp.png', 'wb')
    img_file.write(decoded_data)
    img_file.close()    
    #Loading model
    
    #Loading model
    model_name = request.form.get('ModelName')
    if not model_name:
        return jsonify({'Error':'Model name not found'})
    
    previous_model = ''
    with open('model_name.txt','r') as w:
        previous_model = w.read()

    try:
        if previous_model != model_name:
            
            with open('model_name.txt','w') as w:
                w.write(model_name)

            previous_model = model_name
            model = YOLO('model\\'+model_name+'.pt')
    except:
        return jsonify({'Error':'Model with such name does not exist'})


    try:
        #Running detection on given image
        img,list_of_products = run_inference(model)
    except:
        return jsonify({'Error':'Error running detection'})

    collec = db['model_datas']
    data = collec.find()
    
    products = []
    for product in list_of_products:
        products.append(get_value(product, data))
    
    list_of_products = ''
    for product in products:
        list_of_products+=', '+str(product)
    
    if products!=[]:
        list_of_products = list_of_products[2:]
    else:
        list_of_products = 'No products found'
    os.remove('temp.png')
    
    return jsonify({'Products':list_of_products})

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

    return jsonify(result)

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

@app.route("/hello")
def hello_world():
    return "Hello World!"


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
