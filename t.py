import cv2
from yolov8 import YOLOv8

# Initialize yolov8 object detector
model_path = "model\CakeShop.onnx"
yolov8_detector = YOLOv8(model_path, conf_thres=0.2, iou_thres=0.3)
class_names = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21']


# Read image
img = cv2.imread('relative_images/11.jpg')

# Detect Objects
boxes, scores, class_ids = yolov8_detector(img)

for box, score, class_id in zip(boxes, scores, class_ids):
    x1, y1, x2, y2 = box.astype(int)
    name = class_names[class_id]
    text = name+' '+str(round(score,2))

    cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),1)
    cv2.putText(img,text,(x1,y1-5),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,(0,255,0),1)
    print(score)



# Draw detections
# combined_img = yolov8_detector.draw_detections(img)
cv2.imshow("Detected Objects", img)
cv2.waitKey(0)
