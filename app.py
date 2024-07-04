from flask import Flask, request, render_template, redirect, url_for
import requests
import os

from Control.User.loginController import LoginController

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
from flask import Flask, request, render_template, redirect, url_for,abort,jsonify,session
from werkzeug.exceptions import InternalServerError,BadRequest
#slow start when loadin ML functions, normal turn off
# from Control.User.requestForPrediction import RequestForPrediction
#

from Control.User.SignupController import *
from Control.IndividualUser.getAccountInfo import *
from Control.IndividualUser.updatePersonalInfo import *
from Control.User.changePasswordController import *
from Control.User.newsController import *
from Control.premiumUser.get_predictionData_by_symbol import *
from Control.User.commentController import *
from Control.premiumUser.recommendationListController import *
from Control.User.notificationController import *
from Control.premiumUser.get_followList_by_accountId import *
from Control.premiumUser.get_threshold_by_symbol_and_id import *
from Control.User.get_accounts_by_userName import *
from Control.User.get_account_by_accountId import *
from Control.premiumUser.remove_notification_by_id import *
from Control.premiumUser.remove_threshold_settings_by_thresholdId import *
from Control.User.insert_review_by_id import *
from Control.premiumUser.update_watchlist import *
from Control.premiumUser.get_watchlist_by_accountID import *
from Control.User.get_who_follows_me_by_accountID import *
from Control.premiumUser.update_threshold_settings import *
from Control.User.remove_follower_in_followList_by_id import *
from Control.User.insert_followList_by_id import *
from Control.premiumUser.update_follower_in_followList_by_id import *
from Control.premiumUser.get_threshold_setting_by_id import *
from Control.premiumUser.update_preference_by_accountId import *
from Control.premiumUser.getPremiumUsersController import *
from Control.premiumUser.get_accountList_by_followedId import *
from Control.User.get_searchHistory_by_id import *
from Control.User.remove_searchHistory_by_id import *
from Control.premiumUser.get_preference_by_accountId import *
from Control.User.emailVerificationController import *
from Control.Admin.get_all_HeadLine_reviews import *
import hashlib
from flask import Flask, redirect
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from machineLearningModel.TF_LR_Model import *
from machineLearningModel.GRU_Model import *
from machineLearningModel.LSTM_Model import *
from Control.User.storePredictionResultController import *
import threading
import time
app = Flask(__name__)
app.static_folder = 'static'
app.secret_key = 'csci314'

@app.route('/preference',methods=['GET','POST'])
def preference():
    preference = GetPreferenceByAccountId().get_preference_by_accountId("1")
    return render_template("/premiumUser/preference.html",preference=preference)
@app.route('/space/<string:accountId>',methods=['GET','POST'])
def space(accountId):
    if request.method == 'GET':
        # hard code, assume session["user"] has 1
        if int(accountId) == 1:
            watchList = GetWatchlistByAccountID().get_watchlist_by_accountID("1")
            # stockMiniData = []
            # for i in watchList:
            #     stockMiniData.append(StockDataController().get_stock_info_minimum(i))
            # print(stockMiniData)
            account = GetAccountByAccountId().get_account_by_accountId("1")
            thresholdList = GetThresholdSettingById().get_threshold_settings_by_id("1")
            return render_template("/User/mySpace.html",account=account,watchList=watchList,thresholdList=thresholdList)
        else:
            accountFavoList = GetFollowListByAccountId().get_followList_by_accountId("1")
            watchList = GetWatchlistByAccountID().get_watchlist_by_accountID(accountId)
            account = GetAccountByAccountId().get_account_by_accountId(accountId)
            thresholdList = GetThresholdSettingById().get_threshold_settings_by_id(accountId)
            print(account)
            return render_template("/User/otherUserSpace.html",accountFavoList=accountFavoList,account=account,watchList=watchList,thresholdList=thresholdList)

@app.route('/remove_symbol_from_threshold/<string:thresholdId>',methods=['POST'])
def remove_symbol_from_threshold(thresholdId):
    Remove_threshold_settings_by_thresholdId().remove_threshold_settings_by_thresholdId(thresholdId)
    return jsonify({"success": True})


@app.route('/friend',methods=['GET','POST'])
def friend_list():
    if request.method == 'GET':
        followList = GetFollowListByAccountId().get_followList_by_accountId("1")
        who_follow_me_list = Get_who_follows_me_by_accountID().get_who_follows_me_by_accountID("1")
        account = GetAccountByAccountId().get_account_by_accountId("1")
        return render_template("/system/friend.html",followList=followList,who_follow_me_list=who_follow_me_list,account=account)
@app.route('/ratingComment', methods=['GET', 'POST'])
def ratingComment():
    if request.method == 'GET':
        return render_template("/system/RatingComment.html")
    if request.method == 'POST':
        data = request.json
        Insert_review_by_id().insert_review_by_id("1",data.get("rating"),data.get("comment"))
        return jsonify({'success': True})

@app.route('/insert_followList/<string:followedId>', methods=['GET', 'POST'])
def insert_followList(followedId):
    InsertFollowListById().insert_followList_by_id("1",followedId)
    return jsonify({'success': True})

@app.route('/remove_follower_in_followList/<string:followedId>', methods=['GET', 'POST'])
def remove_follower_in_followList(followedId):
    RemoveFollowerInFollowListById().remove_follower_in_followList_by_id("1",followedId)
    return jsonify({'success': True})
@app.route('/toggle-notification',methods=['GET','POST'])
def toggle_notification():
    data = request.json
    UpdateFollowerInFollowListById().update_follower_in_followList_by_id("1",data["followId"],data["notifyMe"])
    return jsonify({'success': True})
@app.route('/search/<string:content>')
def search(content):
    accountsList = GetAccountsByUserName().get_accounts_by_userName(content,"1")
    accountFavoList = GetFollowListByAccountId().get_followList_by_accountId_List("1")
    stockWatchList = GetWatchlistByAccountID().get_watchlist_by_accountID("1")
    return render_template("/system/search.html",content=content,accountsList=accountsList,stockWatchList=stockWatchList,accountFavoList=accountFavoList)
@app.route('/mainPage', methods=['GET', 'POST'])
def mainPage():
    account = GetAccountByAccountId().get_account_by_accountId("1")
    watchList = GetWatchlistByAccountID().get_watchlist_by_accountID("1")
    return render_template('mainPage.html',account=account,watchList=watchList)

#remove notification
@app.route('/remove_notification', methods=['POST'])
def remove_notification():
    data = request.json
    notificationId = data.get('notificationId')
    notificationType = data.get('notificationType')
    referenceId = data.get('referenceId')

    if notificationType == "threshold":
        Remove_notification_by_id().remove_notification_by_id(notificationId)
        Remove_threshold_settings_by_thresholdId().remove_threshold_settings_by_thresholdId(referenceId)
    else:
        Remove_notification_by_id().remove_notification_by_id(notificationId)

    return jsonify({'success': True})

# user login main page
@app.route('/recommendation_news/<int:page>', methods=['GET', 'POST'])
def recommendation_news(page):
    # hard code for test, countries and industries store in session['preferences']
    countries = 'us'
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

@app.route("/searchSymbol/<string:symbol>", methods=['GET', 'POST'])
def searchSymbol(symbol):
    if request.method == 'POST':
        return jsonify(StockDataController().search_stock(symbol))
@app.route('/delete_comment_by_id/<string:commentId>',methods=['POST'])
def delete_comment_by_id(commentId):
    CommentController().delete_comment_by_id(commentId)
    return jsonify({'success': True})

@app.route('/symbol/<string:symbol>',methods=['GET','POST'])
def symbol(symbol):
    user = GetAccountByAccountId().get_account_by_accountId("1")
    stockData = StockDataController().get_update_stock_data(symbol,"1y")
    stockInfo = StockDataController().get_stock_info_full(symbol)
    predictionresult = GetPredictionDataBySymbol().get_predictionData_by_symbol(symbol)
    threshold = Get_threshold_by_symbol_and_id().get_threshold_by_symbol_and_id("1",symbol)
    watchList = GetWatchlistByAccountID().get_watchlist_by_accountID("1")
    return render_template('/PremiumUser/symbolPage.html', stockData=stockData,stockInfo=stockInfo,predictionresult=predictionresult,threshold=threshold,watchList=watchList,user=user)
@app.route('/request_for_prediction/<string:symbol>/<string:days>/<string:model>', methods=['GET', 'POST'])
def request_for_prediction(symbol, days, model):
    # accountId = session.get('user')['accountId']
    accountId = 1
    print(f"Request for prediction: Symbol={symbol}, Days={days}, Model={model}, AccountId={accountId}")
    days = int(days)
    # 1. Pass the parameters to the machine learning model
    prediction_result = None
    default_layers = 4
    default_neurons = 32
    if model == 'GRU':
        df = GRU_Model.get_stock_data(symbol)
        prediction_result = GRU_Model().predict_future_prices(symbol, df, days, default_layers, default_neurons)

        # format of GRU model result
        # [{'Date': '2024-06-29', 'Predicted': 195.99, 'Recommendation': 'Hold'}, {'Date': '2024-06-30', 'Predicted': 193.51, 'Recommendation': 'Hold'}]

    elif model == 'LR':
        df = LinearRegression_Model.get_stock_data(symbol)
        prediction_result = LinearRegression_Model(symbol, df, days, default_layers, default_neurons).predict_stock_price()

        # format of LR model result
        # [{'Date': '2024-06-29', 'Predicted': 171.28, 'Recommendation': 'Hold'}]

    elif model == 'LSTM':
        end_date = datetime.today().date()
        start_date = (end_date - timedelta(days=365 * 5))
        df = yf.download(symbol, start=start_date, end=end_date)
        all_dates = pd.date_range(start=df.index.min(), end=df.index.max(), freq='D')
        df = df.reindex(all_dates)
        df = df.fillna(method='ffill')
        model = LSTM_Model(symbol, df, n_days=days, layers=default_layers, neurons=default_neurons)
        prediction_result = model.predict()
        # format of LSTM prediction result
        # [{'Date': '2024-06-29', 'Predicted': 202.17, 'Recommendation': 'Hold'}]

    else:
        return jsonify({'success': False, 'error': 'Invalid model'}), 400

    if not prediction_result:
        return jsonify({'success': False, 'error': 'Prediction failed'}), 500

    # 2. Store the prediction result in the database
    prediction_id = storePredictionResultController.store_prediction_result(symbol, prediction_result)

    # 3. Store a notification
    #def set_notification(self, accountId, notification, notificationType, referenceId, symbol):
    NotificationController().set_notification(accountId, f"Prediction for {symbol} is completed.", 'Prediction', prediction_id, symbol)

    return jsonify({'success': True, 'prediction_result': prediction_result})


@app.route('/submit_comment',methods=["POST"])
def submit_comment():
    data = request.json
    CommentController().insert_comment("1",data["symbol"],data["comment"])
    return jsonify({'success': True})
@app.route('/update_watchList',methods=['POST'])
def update_watchList():
    data = request.json
    UpdateWatchlist().update_Watchlist("1",data.get("watchList"))
    return jsonify({'success': True})

@app.route("/update_threshold_setting/<string:symbol>/<string:threshold>", methods=['POST'])
def update_threshold_setting(symbol, threshold):
    Update_threshold_settings().update_threshold_settings("1", symbol, float(threshold))
    return jsonify({'success': True})
@app.route('/symbol_comments/<string:symbol>')
def symbol_comments(symbol):
    return jsonify(CommentController().get_comments_by_symbol(symbol))


@app.route('/preferenceSetup', methods=['GET', 'POST'])
def preferenceSetup():
    return render_template("/system/preferenceSetUp.html")
@app.route('/demo')
def demo():
    list = StockDataController().get_recommendation_stock_by_preference("us", "Energy,Technology")
    recommendationList = []
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
    result = StockDataController().get_update_stock_data(symbol, period)
    print(len(result))
    return jsonify(result)

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

        return
    except Exception as e:
        return jsonify({"error":str(e)})

@app.route('/emailVerification',methods=['GET','POST'])
def emailVerification():
    if request.method == "GET":
        return render_template("/system/emailVerification.html")
    if request.method == "POST":
        # here to sent email, not verification
        data = request.json
        email = data["email"]
        EmailVerificationController().send_verification_code(email)
        return jsonify({"success": True})

@app.route('/verifyEmailCode',methods=['POST'])
def verifyEmailCode():
    try:
        data = request.json
        # if data["accountStatus"] == 'login':
        email = data.get('email')
        code = data.get('code')
        accountId = data.get('accountId')
        EmailVerificationController().verify_code(email,code)
        session['user'] = GetAccountByAccountId().get_account_by_accountId(accountId)
        return jsonify({"success": True})

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})
@app.route('/login', methods=['POST','GET'])
def login():
    if request.method == 'GET':
        return render_template("system/login.html")
    if request.method == 'POST':
        try:
            data = request.json
            email = data.get('email')
            password = data.get('password')
            account = LoginController().login(email, password)
            return jsonify({'success':True,'account': account})
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

#handle personal info
@app.route('/updatePersonalInfo', methods=['POST'])
def updatePersonalInfo():
    account = request.json.get('userAccount')
    #  from here
    userName = account["userName"]
    email = account['email']
    bio = account['bio']
    age = account['age']
    sex  = account['sex']
    occupation = account['occupation']
    incomeLevel = account['incomeLevel']
    netWorth = account['netWorth']
    investmentExperience = account['investmentExperience']
    riskTolerance = account['riskTolerance']
    investmentGoals = account['investmentGoals']
    profile = account['profile']
    #  to here, can simplify by updatePersonalInfo(account['xxx'],account['xxx'])
    if profile != "admin":
        # Refine the following method
        # UpdatePersonalInfo().updatePersonalInfo(,userName,email,bio)

        #update session['user']
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'error': 'Failed to update bio in the database'}), 500

@app.route('/changePassword', methods=['POST'])
def change_password():
    try:
        session['user'] = GetAccountByAccountId().get_account_by_accountId("1")
        old_password = request.json.get('oldPassword')
        new_password = request.json.get('newPassword')
        userName = session['user']['userName']
        # Determine whether the user's entered previous password is correct or not
        if hashlib.md5(old_password.encode()).hexdigest() != session['user']['hashedPassword']:
            raise Exception('Invalid old password')
        # if it is correct, then change current password
        session['user']['hashedPassword'] = ChangePasswordController().changeIndividualPassword(userName,old_password,new_password)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False,'error':str(e)})

@app.route('/',methods=['GET'])
def officialWeb():
    stockInfo = StockDataController().get_stock_info_full("AAPL")
    predictionData = GetPredictionDataBySymbol().get_predictionData_by_symbol("AAPL")
    stockData = StockDataController().get_update_stock_data("AAPL","3mo")
    stockData1 = StockDataController().get_update_stock_data("BILI","3mo")
    stockData2 = StockDataController().get_update_stock_data("MSFT","3mo")

    review = GetAllHeadLineReviews().get_all_headline_reviews()
    return render_template("system/template.html",symbolData1=stockData1,symbolData2=stockData2,stockInfo=stockInfo,predictionData=predictionData,symbolData=stockData,review=review)

@app.route('/get_predictionData_by_symbol/<string:symbol>',methods=['GET'])
def get_predictionData_by_symbol(symbol):
    return jsonify(GetPredictionDataBySymbol().get_predictionData_by_symbol(symbol))
@app.route('/history',methods=['GET'])
def history():
    history = Get_searchHistory_by_id().get_searchHistory_by_id("1")
    return render_template("system/history.html",history=history)

@app.route('/remove_searchHistory/<string:id>',methods=['POST'])
def remove_searchHistory(id):
    RemoveSearchHistory().remove_searchHistory_by_id(id)
    return jsonify({'success':True})
@app.route('/redirectToUserPage',methods=['GET'])
def redirectToUserPage():
    if 'user' in session:
        if session['user']["profile"] == 'premium':
                return redirect(url_for('mainPage'))
    else:
        return redirect(url_for('login'))

@app.route('/logout',methods=['GET'])
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/industry_Setting',methods=['GET','POST'])
def industry_Setting():
    if request.method == 'GET':
        return render_template("/system/industry.html")
    data = request.json
    session['industry'] = data.get("selectedIndustries")
    return jsonify({'success': True})

@app.route('/country_Setting',methods=['GET','POST'])
def country_Setting():
    if request.method == 'GET':
        return render_template("/system/country.html")
    data = request.json
    session['country'] = data.get("selectedCountries")
    return jsonify({'success': True})# Dynamically checking that user-selected stocks have not exceeded thresholds

@app.route('/configure_personal_setting',methods=['GET','POST'])
def configure_personal_setting():
    if request.method == 'GET':
        return render_template("/system/configure_personal_settings.html")
    if request.method == 'POST':
        UpdatePreferenceByAccountId().update_preference_by_accountId("1",session['industry'],session['country'])
        return jsonify({'success': True})

@app.route('/pricing',methods=['GET','POST'])
def pricing():
    return render_template("/system/pricing.html")
#
# DO NOT REMOVE, THIS IS SCHEDULE FUNCTION!!!!!
#
# Define a cache to store recent notifications
# notification_cache = {}
#
# def threshold_notification():
#     global notification_cache
#     premiumUserList = GetPremiumUsersController().getPremiumUsers()
#     for user in premiumUserList:
#         thresholds = GetThresholdSettingById().get_threshold_settings_by_id(user)
#         if thresholds:
#             for threshold in thresholds:
#                 symbol = StockDataController().get_stock_info_minimum(threshold["stockSymbol"])
#                 if abs(symbol["relative_change"]) > threshold['changePercentage']:
#                     cache_key = (user, threshold["stockSymbol"])
#                     current_time = time.time()
#                     # Checking for recent notifications
#                     if cache_key not in notification_cache or (current_time - notification_cache[cache_key] > 3600):  # one hour
#                         notificationWord = f"Hi, Your followed {threshold['stockSymbol']} that exceeds your threshold."
#                         NotificationController().set_notification(user, notificationWord, "threshold", threshold['thresholdId'],threshold['stockSymbol'])
#                         notification_cache[cache_key] = current_time
#                         Personal_who_follow_user_List = GetAccountListByFollowedId().get_accountList_by_followedId(user)
#                         if Personal_who_follow_user_List:
#                             for userFollow in Personal_who_follow_user_List:
#                                 if userFollow['notifyMe'] == 1:
#                                     notificationWord = f"There have been updates to stock {threshold['stockSymbol']} for user {userFollow['userName']} you follow! Please check"
#                                     hashed_symbol = int(hashlib.md5(threshold['stockSymbol'].encode()).hexdigest(),16)%(2**31-1)
#                                     NotificationController().set_notification(userFollow['followListAccountId'],notificationWord,"friend_threshold",hashed_symbol,threshold['stockSymbol'])

# def run_schedule():
#     schedule.every(2).seconds.do(threshold_notification)
#     while True:
#         schedule.run_pending()
#         time.sleep(1)

if __name__ == '__main__':
    # schedule_thread = threading.Thread(target=run_schedule)
    # schedule_thread.daemon = True
    # schedule_thread.start()
    app.run(host='0.0.0.0',port=80,debug=True)
