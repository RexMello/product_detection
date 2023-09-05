from ultralytics import YOLO
import cv2

def run_inference():
    model = YOLO('model/CakeShop.pt')
    image = cv2.imread('vals.jpeg')
    results = model.predict(image, conf=0.3)
    
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
            
    cv2.imshow('',image)
    cv2.waitKey()
    print(things_found)


run_inference()