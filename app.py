import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
from flask import Flask, request, render_template, redirect, url_for,abort,jsonify
from werkzeug.exceptions import InternalServerError,BadRequest
from Control.User.mlController import *
import pandas as pd
import json


app = Flask(__name__)
app.static_folder = 'static'

@app.route('/')
def main():
    return render_template('front-end page/UserSystem/MainPage.html')

@app.route('/DocumentPage')
def document_page():
    return render_template('front-end page/UserSystem/DocumentPage.html')

@app.route('/ViewerPage')
def viewerPage():
    return render_template('front-end page/UserSystem/ViewerPage.html')

@app.route('/SearchPage')
def searchPage():
    return render_template('front-end page/UserSystem/SearchPage.html')

@app.route('/admin')
def adminLoginPage():
    return render_template('front-end page/adminSystem/adminLoginPage.html')

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

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,debug=False)