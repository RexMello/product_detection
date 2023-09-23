from flask import Flask, jsonify
from os import getcwd
from flask_cors import CORS

BASE_DIR = getcwd()

app = Flask(__name__)
CORS(app)

@app.route('/detect_products', methods=['POST'])
def run_cheating_module():
    return jsonify({'Products values':'value1, value2', 'Products names': 'product1, product2'})
    

@app.route("/fetch_all_data", methods=['GET'])
def fetch_data():
    return jsonify([
    {
        "ModelName": "CakeShop",
        "id": "64f47da10b91a05d5a0392be",
        "name": "Tong lou shao銅鑼燒",
        "value": "1002"
    },
    {
        "ModelName": "CakeShop",
        "id": "64f47db80b91a05d5a03a96e",
        "name": "Honey cake蜂蜜蛋糕",
        "value": "1008"
    },
    {
        "ModelName": "CakeShop",
        "id": "64f4a1eb0b91a05d5a2a36db",
        "name": "White bean cake白豆沙",
        "value": "1017"
    },
    {
        "ModelName": "CakeShop",
        "id": "64f4a2020b91a05d5a2a4e2e",
        "name": "Chocolate cake巧克力饅頭",
        "value": "1005"
    },
    {
        "ModelName": "CakeShop",
        "id": "64f4a36e0b91a05d5a2bd459",
        "name": "Red bean YG小倉羊羹",
        "value": "1020"
    },
    {
        "ModelName": "CakeShop",
        "id": "64f4a37f0b91a05d5a2be6b2",
        "name": "Shao MT燒饅頭",
        "value": "1007"
    },
    {
        "ModelName": "CakeShop",
        "id": "64f4a38f0b91a05d5a2bf9b2",
        "name": "Nut cake果仁蛋糕",
        "value": "1009"
    },
    {
        "ModelName": "CakeShop",
        "id": "64f4a39f0b91a05d5a2c09dd",
        "name": "Hei zi ma su黑芝麻酥",
        "value": "1010"
    },
    {
        "ModelName": "CakeShop",
        "id": "64f4a3b90b91a05d5a2c269a",
        "name": "Tong lou shao MS銅鑼燒麻糬",
        "value": "1003"
    },
    {
        "ModelName": "CakeShop",
        "id": "64f4a3ce0b91a05d5a2c3d25",
        "name": "Pineapple cake鳳梨酥5入",
        "value": "3032"
    },
    {
        "ModelName": "CakeShop",
        "id": "64f4a3e10b91a05d5a2c5302",
        "name": "Red bean cake最中",
        "value": "3033"
    },
    {
        "ModelName": "CakeShop",
        "id": "64f4a53c0b91a05d5a2dcb57",
        "name": "Red bean cakeA最中",
        "value": "3033"
    },
    {
        "ModelName": "CakeShop",
        "id": "64f4a5540b91a05d5a2de3b6",
        "name": "Da fu Sixpcs大福6入",
        "value": "3039"
    },
    {
        "ModelName": "CakeShop",
        "id": "64f4a5620b91a05d5a2df3c3",
        "name": "Zui Zhong shell最中殼",
        "value": "1026"
    },
    {
        "ModelName": "CakeShop",
        "id": "64f4a5700b91a05d5a2e0301",
        "name": "Wet bean jam紅豆餡",
        "value": "1027"
    },
    {
        "ModelName": "CakeShop",
        "id": "64f4a57f0b91a05d5a2e1296",
        "name": "Dry bean jam甘紅豆粒",
        "value": "1028"
    },
    {
        "ModelName": "CakeShop",
        "id": "64f4a5900b91a05d5a2e2554",
        "name": "Red suger MS赤糖麻糬",
        "value": "1004"
    },
    {
        "ModelName": "CakeShop",
        "id": "64f4a59f0b91a05d5a2e3531",
        "name": "Lian zi MT蓮子饅頭",
        "value": "1018"
    },
    {
        "ModelName": "CakeShop",
        "id": "64f4a5ae0b91a05d5a2e4551",
        "name": "Red bean lu zi紅豆鹿子",
        "value": "1019"
    },
    {
        "ModelName": "CakeShop",
        "id": "64f4a5bc0b91a05d5a2e53c6",
        "name": "Egg yield cake蛋黃酥",
        "value": "1015"
    },
    {
        "ModelName": "CakeShop",
        "id": "64f4a5cc0b91a05d5a2e6513",
        "name": "Green bean cake綠豆椪",
        "value": "1016"
    },
    {
        "ModelName": "CakeShop",
        "id": "64f4a5d90b91a05d5a2e742a",
        "name": "Wu Long Tea YG烏龍茶羊羹",
        "value": "1021"
    },
    {
        "ModelName": "CakeShop",
        "id": "64fddebd0b91a05d5ac0a52d",
        "name": "Lizi MT栗子饅頭",
        "value": "1006"
    },
    {
        "ModelName": "CakeShop",
        "id": "6508119c68606251f5a8204c",
        "name": "ZhaoNiSu棗泥酥",
        "value": "1011"
    }
])

@app.route("/fetch_model_names", methods=['GET'])
def fetch_model_data():

    return jsonify({'modelNames':['CakeShop']})

@app.route("/fetch_single_data/<string:id_value>", methods=['GET'])
def get_single_data():
    return jsonify({
    "ModelName": "CakeShop",
    "_id": "64f47da10b91a05d5a0392be",
    "detection_id": "0",
    "name": "Tong lou shao銅鑼燒",
    "value": "1002"
})

@app.route("/update_data/<string:id_value>/<string:new_value>", methods=['GET'])
def update_user_data():
    return jsonify({'detail':'success'})

@app.route("/get_contact_support", methods=['GET'])
def get_contact():
    return jsonify({'contact':'emai: Rex@hotmail.com'})

@app.route("/hello")
def hello_world():
    return "Hello World! "+str(getcwd())


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)