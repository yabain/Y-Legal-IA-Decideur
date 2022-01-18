from flask import Flask, request, jsonify
import os

from bussiness.bussiness import BussinessClassifier

app = Flask(__name__)
bussiness = BussinessClassifier()


class HTTPRestAPI:
    """API Rest """


    @staticmethod
    @app.route("/predict", methods=['POST'])
    def doPost():
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

    def run(self):
        port = int(os.environ.get('PORT', 5000))
        app.run(debug=True, host='0.0.0.0', port=port)
        bussiness.startRabbimtMQ()


