import cv2
from flask import Flask, request, jsonify
from pymongo import MongoClient
from ultralytics import YOLO
import os
import certifi
from flask_cors import CORS

cluster = MongoClient("mongodb+srv://kai:13579007@cluster0.wacwe.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=certifi.where())
db = cluster["product_data"]
collec = db['model_data']
data = collec.find()


def get_value(data,name):
    for d in data:
        if d['name'] == str(name):
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

@app.route('/detect_products', methods=['POST'])
def run_cheating_module():
    # check if request has file part
    if 'image' not in request.files:
        return jsonify({'Error':'No image found'})

    file = request.files['image']

    # save video file to disk
    file.save('temp.png')
    
    #Loading model
    model_name = request.form.get('ModelName')
    if not model_name:
        return jsonify({'Error':'Model name not found'})
    
    if model_name not in db.list_collection_names():
        return jsonify({'Error':'No record for such model exist'})

    try:
        model = YOLO('model\\'+model_name+'.pt')
    except:
        return jsonify({'Error':'Model with such name does not exist'})


    try:
        #Running detection on given image
        img,list_of_products = run_inference(model)
    except:
        return jsonify({'Error':'Error running detection'})

    try:
        #Getting relative videos from
        products = []
        for product in list_of_products:
            products.append(get_value(product))
        
        list_of_products = ''
        for product in products:
            list_of_products+=', '+str(product)
        
        if products!=[]:
            list_of_products = list_of_products[2:]
        else:
            list_of_products = 'No products found'
        os.remove('temp.png')
    except:
        return jsonify({'Error':'There was an error in calculation'})
    
    return jsonify({'Products':list_of_products})


@app.route("/")
def hello_world():
    return "Hello World!"


@app.route("/fetch_all_data", methods=['GET'])
def fetch_data():
    collec = db['model_data']
    data = collec.find()
    result = []
    for d in data:
        result.append({
            'name': d['name'],
            'value': d['value'],
            'ModelName': d['ModelName']
        })

    return jsonify(result)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
