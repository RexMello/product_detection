import os
import cv2
from flask import Flask, jsonify, request
from pymongo import MongoClient
from os import getcwd
import certifi
from flask_cors import CORS
from ultralytics import YOLO
from collections import Counter
from bson import ObjectId
import requests
import datetime

# Define the URL of the public Google Drive file
file_url = "https://drive.usercontent.google.com/download?id=1AbcXDIuosX9sJB9wtRQLRmMlOFmRsZnP&export=download&authuser=0&confirm=t&uuid=2cdaacdd-b7cd-4036-aabd-c1905b8040a5&at=APZUnTWsYdzLB04PU_dBtTAkRWBj:1696346548785"

# Define the local filename where you want to save the downloaded file
local_filename = "CakeShop.pt"

# Send an HTTP GET request to download the file
response = requests.get(file_url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Open a local file and write the content of the response to it
    with open(local_filename, "wb") as f:
        f.write(response.content)
    print(f"File '{local_filename}' downloaded successfully.")
else:
    print("Failed to download the file.")

# Now you can use the downloaded model file as needed


BASE_DIR = getcwd()
model = None
loaded_model = None

cluster = MongoClient("mongodb+srv://rex:13579007@cluster0.kku4atv.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=certifi.where())
db = cluster["product_data"]

def get_value(name, data):
    for d in data:
        if d == str(name):
            return data[d]['value'], data[d]['name']
    return '', ''

def run_inference(model):
    image = cv2.imread(BASE_DIR+'/temp.png')
    print("IMAGE READ AT ",datetime.datetime.now())
    results = model.predict(image, conf=0.4)
    print("PREDICTIONS FOUND AT ",datetime.datetime.now())
    list_of_coords = []
    
    things_found = []
    print("DRAWING AT",datetime.datetime.now())

    for r in results:
        boxes = r.boxes
        for box in boxes:
            thing_found = model.names[int(box.cls)]
            things_found.append(thing_found)
            confidence = box.conf.item()
            b = box.xyxy[0]
            # c = box.cls
            x1,y1,x2,y2 = int(b[0].item()),int(b[1].item()),int(b[2].item()), int(b[3].item())
            list_of_coords.append((x1,y1,x2,y2))
            cv2.rectangle(image,(x1,y1),(x2,y2),(0,255,0),2)
            cv2.putText(image,str(round(confidence,2)),(x1,y1-5),cv2.FONT_HERSHEY_COMPLEX_SMALL,1.5,(0,255,0),1)
    return image, things_found, list_of_coords

app = Flask(__name__)
CORS(app)

@app.route('/detect_products', methods=['POST'])
def run_cheating_module():
    print("STARTING AT ",datetime.datetime.now())
    global model, loaded_model

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
    print("MODEL AT ",datetime.datetime.now())
    
    model_name = 'CakeShop'

    #Loading model
    if not model_name:
        return jsonify({'Error':'Model name not found'})
    
    model_path = BASE_DIR+'/'+model_name+'.pt'
    
    if not os.path.exists(model_path):
        return jsonify({'Error':BASE_DIR+'/'+model_name+'.pt'+' such name does not exist'})

    
    if loaded_model != model_name:
        print('RELOADING MODEL')
        model = YOLO(model_path)
        loaded_model = model_name

    try:
        print("PREDICTION START AT ",datetime.datetime.now())
        #Running detection on given image
        img,list_of_products, list_of_coords = run_inference(model)
        print("PREDICTION ENDED AT ",datetime.datetime.now())
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

        cv2.imwrite(BASE_DIR+'/output.png',img)
        os.remove(BASE_DIR+'/temp.png')

        
        print("ENDING AT ",datetime.datetime.now())
        return jsonify({'Products values': values,'Products names': names, 'coords':list_of_coords})

        
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


# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=80)

