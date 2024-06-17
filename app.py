from flask import Flask, request, render_template, redirect, url_for
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
import hashlib
app = Flask(__name__)
app.static_folder = 'static'
app.secret_key = 'csci314'

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
        #hard code for test
        #session['user']  = {'accountId': 1, 'userName': 'lixiang', 'apikey': 'abcdefg', 'hashedPassword': 'e10adc3949ba59abbe56e057f20f883e', 'email': 'lixiang@gmail.com', 'bio': 'Welcome to stock4me!', 'profile': 'free', 'status': 'valid', 'apikeyUsageCount': 0,'accountType':'individual' 'createDateTime': datetime.datetime(2024, 6, 14, 18, 8, 2)}
        session['user'] = GetAccountInfo().getAccountInfo("1")
        print(session['user'])
        if session['user']['accountType'] == 'individual':
            if session['user']['profile'] == 'free':
                return render_template("individualFreeUser/accountInfo.html",user = session['user'])
            elif session['user']['profile'] == 'premium':
                pass
        elif session['user']['accountType'] == 'business':
            pass

#handle personal info. update(name,bio,email), business update(name,bio,email,companyName)
@app.route('/updatePersonalInfo', methods=['POST'])
def update_bio():
    # if 'user' not in session:
    #     print("user not in session")
    #     return jsonify({'success': False, 'error': 'Unauthorized'}), 401

    accountType = request.json.get('accountType')
    accountId = request.json.get('accountId')
    bio = request.json.get('bio')
    userName = request.json.get('userName')
    email = request.json.get('email')
    print(accountType,accountId,bio,userName,email)
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
        session['user'] = GetAccountInfo().getAccountInfo("1")
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
    print(predictionResult)
    return jsonify(predictionResult)

@app.route('/deletePrediction/<int:requestId>', methods=['DELETE'])
def deletePrediction(requestId):
    DeleteRequestRecord().deleteRequestRecord(str(requestId))
    return jsonify({'success':True})

@app.route('/predict', methods=['GET','POST'])
def predict():
    if request.method == 'GET':
        return render_template("individualFreeUser/RequestPrediction.html")
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


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,debug=True)