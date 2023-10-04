from flask import Flask, jsonify

app = Flask(__name__)
@app.route('/api/numbers', methods=['GET'])
def get_numbers():
    return jsonify({'coords':[(582, 298, 852, 429), (634, 173, 763, 244), (441, 65, 570, 134), (162, 200, 329, 297), (453, 225, 609, 344), (335, 223, 473, 315), (381, 332, 583, 408), (308, 94, 400, 164), (219, 286, 362, 411), (609, 233, 723, 300), (389, 96, 502, 166), (524, 104, 631, 179)]})
if __name__ == '__main__':
    app.run(debug=True)

