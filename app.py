from flask import Flask, request, render_template, redirect, url_for
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
from flask import Flask, request, render_template, redirect, url_for,abort,jsonify
from werkzeug.exceptions import InternalServerError,BadRequest
from Control.User.mlController import *
from Control.User.generateApiKeyController import *
from Control.User.uploadFileController import *
import pandas as pd
import json


app = Flask(__name__)
app.static_folder = 'static'

@app.route('/')
def main():
    return render_template('front-end page/UserSystem/')

@app.route('/DocumentPage')
def document_page():
    return render_template('front-end page/UserSystem/')

@app.route('/ViewerPage')
def viewerPage():
    return render_template('front-end page/UserSystem/')

@app.route('/SearchPage')
def searchPage():
    return render_template('front-end page/UserSystem/')

@app.route('/admin')
def adminLoginPage():
    return render_template('front-end page/adminSystem/adminLoginPage.html')

@app.route('/adminRegister')
def adminRegisterPage():
    return render_template('front-end page/adminSystem/')

@app.route('/adminMain')
def adminMainPage():
    return render_template('front-end page/adminSystem/')

@app.errorhandler(400)
def bad_request_error(error):
    return render_template('error400.html', error_message=error), 400

@app.route('/api')
def index():
    return render_template('apiPage.html')
@app.route('/apiRequest')
def api():
    apikey = request.args.get('apikey')
    symbol = request.args.get('symbol')
    timeframe = request.args.get('timeframe')
    model = request.args.get('model')
    layers = request.args.get('layers')
    neurons = request.args.get('neurons')

    try:
        if len(timeframe) == 0:
            timeframe = "5"
        if len(model) == 0:
            model = 'lr'
        if len(layers) == 0:
            layers = "10"
        if len(neurons) == 0:
            neurons = "16"
        result = MlController().getMLResultByApi(apikey,symbol,model,timeframe,layers,neurons)
        resultDict = json.loads(result)
        return jsonify(resultDict)
    except Exception as e:
        raise BadRequest(e)


@app.route('/getapikey', methods=['POST'])
def get_api_key():
    user_type = request.form.get('userType')
    user_name = request.form.get('userName')

    apikey = GenerateApiKeyController().generateApiKey(user_type, user_name)
    return render_template('front-end page/UserSystem/', apikey=apikey)

@app.route('/getPredictionResult', methods=['POST'])
def getPredictionResult():
    apikey = request.form.get('apikey')
    tickerSymbol = request.form.get('tickerSymbol')
    modelName = request.form.get('modelName')
    timeFrame = request.form.get('timeFrame')
    layers = request.form.get('layers')
    neurons = request.form.get('neurons')
    file = request.files['file']
    try:
        if file:
            df = pd.read_csv(file)
            is_valid, message = UploadFileController().checkUploadDataFormat(df)
            if is_valid:
                result = MlController().getMLResultByUploadData(df,apikey,file.filename[:-4],modelName,timeFrame,layers,neurons)
            else:
                return jsonify(success=False, error=str(message))
        else:
            result = MlController().getMLResultByParameters(apikey, tickerSymbol, modelName, timeFrame, layers, neurons)
        resultDict = json.loads(result)
        return jsonify(success=True, result=resultDict)
    except Exception as e:
        return jsonify(success=False, error=str(e))

## crud sample
items = []

@app.route('/crudSample', methods=['GET'])
def crudSample():
    return render_template("CRUD_Sample.html")
@app.route('/items', methods=['GET'])
def get_items():
    return jsonify(items)

@app.route('/items', methods=['POST'])
def add_item():
    item = request.json
    items.append(item)
    return jsonify(item), 201

@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = request.json
    if 0 <= item_id < len(items):
        items[item_id] = item
        return jsonify(item)
    else:
        return jsonify({"error": "Item not found"}), 404

@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    if 0 <= item_id < len(items):
        removed_item = items.pop(item_id)
        return jsonify(removed_item)
    else:
        return jsonify({"error": "Item not found"}), 404

## sample end

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,debug=True)