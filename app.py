from flask import Flask, request, render_template, redirect, url_for
import requests
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
from flask import Flask, request, render_template, redirect, url_for,abort,jsonify,session
from werkzeug.exceptions import InternalServerError,BadRequest
#slow start when loadin ML functions, normal turn off
# from Control.User.requestForPrediction import RequestForPrediction
#
from Control.User.generateApiKeyController import *
from Control.User.uploadFileController import *
import pandas as pd
import json
from Control.User.loginController import *
from Control.User.SignupController import *
from Control.IndividualUser.getAccountInfo import *
from Control.IndividualUser.getRequestRecord import *
from Control.User.deleteRequestRecord import *
from Control.IndividualUser.updatePersonalInfo import *
from Control.User.changePasswordController import *
from Control.User.stockDataController import *
from Control.User.newsController import *
from Control.premiumUser.get_predictionData_by_symbol import *
from Control.User.commentController import *
from Control.premiumUser.recommendationListController import *
from Control.User.notificationController import *
import hashlib
from flask import Flask, redirect
app = Flask(__name__)
app.static_folder = 'static'
app.secret_key = 'csci314'

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

app = Flask(__name__)


# user login main page
@app.route('/recommendation_news/<int:page>', methods=['GET', 'POST'])
def recommendation_news(page):
    # hard code for test, countries and industries store in session['preferences']
    countries = 'cn'
    industries = 'Technology'
    result = NewsController().get_recommendation_news(countries,industries,str(page))
    return jsonify(result)
# user login main page
@app.route('/recommendation_symbol', methods=['GET', 'POST'])
def recommendation_symbol():
    # hard code for test, userId in session['user']
    accountId = 1
    return jsonify(RecommendationListController().get_recommendationList_by_accountId(accountId))
@app.route('/get_notification',methods=['GET', 'POST'])
def get_notification():
    # hard code for test, userId in session['user']
    accountId = 1
    return jsonify(NotificationController().get_notifications_by_accountId(accountId))

@app.route('/symbol_news/<string:symbol>/<int:page>', methods=['GET', 'POST'])
def symbol_news(symbol,page):
    return jsonify(NewsController().get_news_by_symbol(symbol,str(page)))

@app.route('/symbol/<string:symbol>')
def symbol(symbol):
    stockData = StockDataController().get_update_stock_data(symbol,"180d")
    stockInfo = StockDataController().get_stock_info_full(symbol)
    predictionresult = PredictionData().get_predictionData_by_symbol(symbol)
    return render_template('index.html', stockData=stockData,stockInfo=stockInfo,predictionresult=predictionresult)

@app.route('/symbol_comments/<string:symbol>')
def symbol_comments(symbol):
    return jsonify(CommentController().get_comments_by_symbol(symbol))

@app.route('/emailVerification', methods=['GET', 'POST'])
def emailVerification():
    return render_template("/system/emailVerification.html")

@app.route('/preferenceSetup', methods=['GET', 'POST'])
def preferenceSetup():
    return render_template("/system/preferenceSetUp.html")
@app.route('/demo')
def demo():
    list = StockDataController().get_recommendation_stock_by_preference("us", "Energy,Technology")
    recommendationList = []
    print(list)
    for stock in list:
        try:
            recommendationList.append(StockDataController().get_stock_info_medium(stock))
        except Exception as e:
            continue

    return render_template('demo.html',recommendationList = recommendationList)
@app.route('/stock_info_minimum/<string:symbol>', methods=['GET'])
def stock_info_minimum(symbol):
    return jsonify(StockDataController().get_stock_info_minimum(symbol))

@app.route('/update_stock_data/<string:symbol>/<string:period>', methods=['GET'])
def update_stock_data(symbol, period):
    print(symbol,period)
    return jsonify(StockDataController().get_update_stock_data(symbol, period))

@app.route('/stock_data_medium/<string:symbol>',methods=['GET'])
def stock_data_medium(symbol):
    return jsonify(StockDataController().get_stock_info_medium(symbol))

@app.route('/stock_info_full/<string:symbol>', methods=['GET'])
def stock_info_full(symbol):
    return jsonify(StockDataController().get_stock_info_full(symbol))
@app.route('/api',methods=['GET'])
def api():
    try:
        apikey = request.args.get('apikey')
        symbol = request.args.get('symbol')
        timeframe = request.args.get('timeframe')
        model = request.args.get('model')
        layers = request.args.get('layers')
        neurons = request.args.get('neurons')
        result = RequestForPrediction().getPrediction(apikey,symbol,timeframe,model,layers,neurons,"api")
        return jsonify(result)
    except Exception as e:
        return jsonify({"error":str(e)})


@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'GET':
        return render_template("system/login.html")
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')
        session['user'] = LoginController().login(username, password)
        return jsonify({'success':True})
    except Exception as e:
        return jsonify({'success':False,'error':str(e)})

@app.route('/signup',methods=['POST','GET'])
def signup():
    if request.method == 'GET':
        return render_template("system/signup.html")
    try:
        data = request.json
        SignupController().individualSignUp(data['profile'],data['username'],data['email'],data['password'],data['repassword'],data['invitationCode'])
        return jsonify({'success':True})
    except Exception as e:
        return jsonify({'success':False,'error':str(e)})
@app.route('/businessSignup',methods=['POST','GET'])
def businesssignup():
    if request.method == 'GET':
        return render_template("system/businessSignup.html")
    try:
        data = request.json
        pass
    except Exception as e:
        return jsonify({'success':False,'error':str(e)})

@app.route('/accountInfo',methods=['POST','GET'])
def accountInfo():
    if request.method == 'GET':
        #todo hard code for test
        #session['user']  = {'accountId': 1, 'userName': 'lixiang', 'apikey': 'abcdefg', 'hashedPassword': 'e10adc3949ba59abbe56e057f20f883e', 'email': 'lixiang@gmail.com', 'bio': 'Welcome to stock4me!', 'profile': 'free', 'status': 'valid', 'apikeyUsageCount': 0,'accountType':'individual' 'createDateTime': datetime.datetime(2024, 6, 14, 18, 8, 2)}
        session['user'] = GetAccountInfo().getAccountInfo("1")
        if session['user']['accountType'] == 'individual':
            if session['user']['profile'] == 'free':
                return render_template("individualFreeUser/accountInfo.html",user = session['user'])
            elif session['user']['profile'] == 'premium':
                pass
        elif session['user']['accountType'] == 'business':
            pass

#handle personal info. update(name,bio,email), business update(name,bio,email,companyName)
@app.route('/updatePersonalInfo', methods=['POST'])
def updatePersonalInfo_FreeUser():
    # if 'user' not in session:
    #     print("user not in session")
    #     return jsonify({'success': False, 'error': 'Unauthorized'}), 401

    accountType = request.json.get('accountType')
    accountId = request.json.get('accountId')
    bio = request.json.get('bio')
    userName = request.json.get('userName')
    email = request.json.get('email')
    if accountType == 'individual':
        success = UpdatePersonalInfo().updatePersonalInfo(accountId,userName,email,bio)
    elif accountType == 'business':
        #company, updateBusinessInfo()
        pass

    if success:
        session['user']['bio'] = bio
        session['user']['userName'] = userName
        session['user']['email'] = email
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Failed to update bio in the database'}), 500

@app.route('/changePassword', methods=['POST'])
def change_password():
    # if 'user' not in session:
    #     return jsonify({'success': False, 'error': 'Unauthorized'}), 401
    try:
        old_password = request.json.get('oldPassword')
        new_password = request.json.get('newPassword')
        userName = session['user']['userName']
        if hashlib.md5(old_password.encode()).hexdigest() != session['user']['hashedPassword']:
            raise Exception('Invalid old password')
        if session['user']['accountType'] == 'individual':
            session['user']['hashedPassword'] = ChangePasswordController().changeIndividualPassword(userName,old_password,new_password)
        elif session['user']['accountType'] == 'business':
            pass
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False,'error':str(e)})



@app.route('/predictionResult',methods=['POST','GET'])
def predictionresult():
    if request.method == 'GET':
        #hard code for test
        #session['user']  = {'accountId': 1, 'userName': 'lixiang', 'apikey': 'abcdefg', 'hashedPassword': 'e10adc3949ba59abbe56e057f20f883e', 'email': 'lixiang@gmail.com', 'bio': 'Welcome to stock4me!', 'profile': 'free', 'status': 'valid', 'apikeyUsageCount': 0,'accountType':'individual' 'createDateTime': datetime.datetime(2024, 6, 14, 18, 8, 2)}
        # session['user'] = GetAccountInfo().getAccountInfo("1")
        # predictionResult = GetRequestRecord().getRequestRecord(session['user']['apikey'])
        # print(predictionResult)
        if session['user']['accountType'] == 'individual':
            if session['user']['profile'] == 'free':
                return render_template("individualFreeUser/predictionResult.html")
            elif session['user']['profile'] == 'premium':
                pass
        elif session['user']['accountType'] == 'business':
            pass

@app.route('/updatePredictionResult',methods=['GET'])
def updatePredictionResult():
    # session['user'] = GetAccountInfo().getAccountInfo("1")
    predictionResult = GetRequestRecord().getRequestRecord(session['user']['apikey'])
    return jsonify(predictionResult)

@app.route('/deletePrediction/<int:requestId>', methods=['DELETE'])
def deletePrediction(requestId):
    DeleteRequestRecord().deleteRequestRecord(str(requestId))
    return jsonify({'success':True})
@app.route('/verifyInput',methods=['POST'])
def verifyInput():
    if request.method == 'POST':
        try:
            apikey = session['user']['apikey']
            tickerSymbol = request.json.get('tickerSymbol')
            timeRange = request.json.get('timeRange')
            model = request.json.get('model')
            layers = request.json.get('layers')
            neurons = request.json.get('neurons')
            RequestForPrediction().verifyInput(apikey, tickerSymbol, timeRange, model, layers, neurons)
            return jsonify({'success':True})
        except Exception as e:
            return jsonify({'success':False,'error':str(e)})
@app.route('/predict', methods=['GET','POST'])
def predict():
    if request.method == 'GET':
        #todo hard code for test
        # session['user'] = GetAccountInfo().getAccountInfo("1")
        return render_template("individualFreeUser/RequestPrediction.html")
    if request.method == 'POST':
        try:
            apikey = session['user']['apikey']
            tickerSymbol = request.json.get('tickerSymbol')
            timeRange = request.json.get('timeRange')
            model = request.json.get('model')
            layers = request.json.get('layers')
            neurons = request.json.get('neurons')
            RequestForPrediction().getPrediction(apikey, tickerSymbol, timeRange, model, layers, neurons)
            return jsonify({'success':True})
        except Exception as e:
            return jsonify({'success':False,'error':str(e)})
    # print(apikey,tickerSymbol,timeRange,model,layers,neurons)
    # print(type(apikey),type(tickerSymbol),type(timeRange),type(model),type(layers),type(neurons))
    #
@app.route('/',methods=['GET'])
def officialWeb():
    return render_template("system/OfficialWeb.html")

@app.route('/redirectToUserPage',methods=['GET'])
def redirectToUserPage():
    if 'user' in session:
        if session['user']["accountType"] == 'individual':
            if session['user']["profile"] == "free":
                return redirect(url_for('accountInfo'))
    else:
        return redirect(url_for('login'))

@app.route('/logout',methods=['GET'])
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/documentation',methods=['GET'])
def documentation():
    return render_template("system/documentation.html")

@app.route('/contact',methods=['GET'])
def contact():
    return redirect("https://csit321fyp24s2g27.wixsite.com/group27")

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,debug=True)