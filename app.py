from flask import Flask, request, jsonify
from bussiness.bussiness import BussinessClassifier

import os


app = Flask(__name__)
bussiness = BussinessClassifier()

@app.route("/")
def get():
    return "Welcome to IA-Decideur"


@app.route("/predict",methods=["POST"])
def post():
    print("trye http")
    if 'file' not in request.files:
        response = jsonify({'message': "No file part in request", "code": -1})
        response.status_code = 400
        return response
    file = request.files['file']
    if file.filename == '':
        response = jsonify({'message': 'No file selected for uploading', 'code': -2})
        response.status_code = 400
        return response
    else:
        prediction = bussiness.predictFromTextStream(file.stream.read())
        response = jsonify({"message": "success", "code": 0, "prediction": {"prediction": prediction["prediction"],"percent": prediction["percent"]}})
        response.status_code = 200
        return response

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=False, port=port,host="0.0.0.0")
    bussiness.startRabbimtMQ()

