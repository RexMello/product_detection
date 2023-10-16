import os
import cv2
from flask import Flask, jsonify, request
from pymongo import MongoClient
from os import getcwd
import certifi
from flask_cors import CORS
from yolov8 import YOLOv8
from collections import Counter
import requests
import datetime


if not os.path.exists('CakeShop.onnx'):
    file_url = "https://drive.usercontent.google.com/download?id=1t1vlaWs52ZeDXBo-A82UYtcCv5BUtfhm&export=download&authuser=0&confirm=t&uuid=4b93262b-2728-439a-8bdb-18341484a971&at=APZUnTXFsvDcvIaj7U3j94ygQ5hg:1696357658885"
    local_filename = "CakeShop.onnx"
    response = requests.get(file_url)

    if response.status_code == 200:
        with open(local_filename, "wb") as f:
            f.write(response.content)
        print(f"File '{local_filename}' downloaded successfully.")
    else:
        print("Failed to download the file.")


BASE_DIR = getcwd()
model = None
class_names = None
loaded_model = None

print('LOADING MODEL')
model_path = BASE_DIR+'/CakeShop.onnx'
model = YOLOv8(model_path, conf_thres=0.3, iou_thres=0.4)
with open(BASE_DIR+'/CakeShop.txt', "r") as file:
    class_names = [line.strip() for line in file.readlines()]
print('LOADED MODEL')


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
    print('RUNNING PREDICTIONS AT ',datetime.datetime.now())
    boxes, scores, class_ids = model(image)
    print('PREDICTIONS FOUND AT ',datetime.datetime.now())

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
    
    return image, things_found, list_of_coords

app = Flask(__name__)
CORS(app)

@app.route('/detect_products', methods=['POST'])
def run_cheating_module():
    print('STARTING AT ',datetime.datetime.now())

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
        img,list_of_products, list_of_coords = run_inference(model)
        print(list_of_products)
    except:
        return jsonify({'Error':'Error running inference ', 'LOADED MODEL NAME':loaded_model})


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

    else:
        names = 'No products found'
        values = 'No products found'

    cv2.imwrite(BASE_DIR+'/output.png',img)
    os.remove(BASE_DIR+'/temp.png')

    print('ENDED AT ',datetime.datetime.now())

    return jsonify({'Products values': values,'Products names': names, 'coords':list_of_coords})

    # except:
    #     return jsonify({'Error':'Error running manual stuff'})
    
@app.route("/hello")
def hello_world():
    return "Hello World! "+str(getcwd())


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
