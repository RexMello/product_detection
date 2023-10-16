from ultralytics import YOLO

model = YOLO('CakeShop.pt')
model.export(format='onnx')