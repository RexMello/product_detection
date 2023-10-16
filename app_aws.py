import cv2
from flask import Flask, jsonify, request
from pymongo import MongoClient
from os import getcwd
import certifi
from flask_cors import CORS
from ultralytics import YOLO
from collections import Counter


BASE_DIR = getcwd()
model = YOLO('CakeShop.pt')

cluster = MongoClient("mongodb+srv://rex:13579007@cluster0.kku4atv.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=certifi.where())
db = cluster["product_data"]

def get_value(name, data):
    for d in data:
        if d == str(name):
            return data[d]['value'], data[d]['name']
    return '', ''

def run_inference():
    image = cv2.imread('temp.png')
    results = model.predict(image, conf=0.4)
    list_of_coords = []
    
    things_found = []
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
    file = request.files['image']
    file.save('temp.png')

    try:
        #Running detection on given image
        _,list_of_products, list_of_coords = run_inference()
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
        return jsonify({'Products values': values,'Products names': names, 'coords':list_of_coords})

        
    except:
        return jsonify({'Error':'Error running manual stuff'})

@app.route("/hello")
def hello_world():
    return "Hello World! "+str(getcwd())


if __name__ == "__main__":
    app.run(host='0.0.0.0')

