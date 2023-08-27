import cv2
from flask import Flask, request, jsonify
from ultralytics import YOLO


model = YOLO('model\\best.pt')


app = Flask(__name__)
def run_inference():
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
        return 'No image found'

    file = request.files['image']

    # save video file to disk
    file.save('temp.png')

    img,products = run_inference()
    list_of_products = ''
    for product in products:
        list_of_products+=', '+str(product)
    
    if products!=[]:
        list_of_products = list_of_products[2:]
    else:
        list_of_products = 'No products found'

    
    return jsonify({'Products':list_of_products})


if __name__ == "__main__":
    app.run(host='0.0.0.0')


