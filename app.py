import os

from Control.User.UpdatePersonalInfoController import UpdatePersonalInfoController
from Control.User.loginController import LoginController

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
from flask import request, render_template, url_for, jsonify,session
#slow start when loadin ML functions, normal turn off
# from Control.User.requestForPrediction import RequestForPrediction
#

from Control.User.SignupController import *
from Control.IndividualUser.getAccountInfo import *
from Control.User.changePasswordController import *
from Control.User.newsController import *
from Control.premiumUser.get_predictionData_by_symbol import *
from Control.User.commentController import *
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
from Control.User.get_searchHistory_by_id import *
from Control.User.remove_searchHistory_by_id import *
from Control.premiumUser.get_preference_by_accountId import *
from Control.User.emailVerificationController import *
from Control.Admin.get_all_HeadLine_reviews import *
from Control.Admin.update_profile_status import *
from Control.Admin.get_all_account import *
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
    if session.get('user'):
        preference = GetPreferenceByAccountId().get_preference_by_accountId(session.get('user')['accountId'])
        return render_template("/premiumUser/preference.html",preference=preference)
    else:
        return redirect(url_for('login'))
@app.route('/space/<string:accountId>',methods=['GET','POST'])
def space(accountId):
    if session.get('user'):
        if request.method == 'GET':
            if int(accountId) == session.get('user')['accountId']:
                watchList = GetWatchlistByAccountID().get_watchlist_by_accountID(session.get('user')['accountId'])
                account = GetAccountByAccountId().get_account_by_accountId(session.get('user')['accountId'])
                thresholdList = GetThresholdSettingById().get_threshold_settings_by_id(session.get('user')['accountId'])
                return render_template("/User/mySpace.html",account=account,watchList=watchList,thresholdList=thresholdList)
            else:
                accountFavoList = GetFollowListByAccountId().get_followList_by_accountId(session.get('user')['accountId'])
                watchList = GetWatchlistByAccountID().get_watchlist_by_accountID(accountId)
                account = GetAccountByAccountId().get_account_by_accountId(accountId)
                thresholdList = GetThresholdSettingById().get_threshold_settings_by_id(accountId)
                print(account)
                return render_template("/User/otherUserSpace.html",accountFavoList=accountFavoList,account=account,watchList=watchList,thresholdList=thresholdList)
    else:
        return redirect(url_for('login'))

@app.route('/remove_symbol_from_threshold/<string:thresholdId>',methods=['POST'])
def remove_symbol_from_threshold(thresholdId):
    if session.get('user'):
        Remove_threshold_settings_by_thresholdId().remove_threshold_settings_by_thresholdId(thresholdId)
        return jsonify({"success": True})
    else:
        return redirect(url_for('login'))


@app.route('/friend',methods=['GET','POST'])
def friend_list():
    if session.get('user'):
        if request.method == 'GET':
            followList = GetFollowListByAccountId().get_followList_by_accountId(session.get('user')['accountId'])
            who_follow_me_list = Get_who_follows_me_by_accountID().get_who_follows_me_by_accountID(session.get('user')['accountId'])
            account = GetAccountByAccountId().get_account_by_accountId(session.get('user')['accountId'])
            return render_template("/system/friend.html",followList=followList,who_follow_me_list=who_follow_me_list,account=account)
    else:
        return redirect(url_for('login'))
@app.route('/ratingComment', methods=['GET', 'POST'])
def ratingComment():
    if session.get('user'):
        if request.method == 'GET':
            return render_template("/system/RatingComment.html")
        if request.method == 'POST':
            data = request.json
            Insert_review_by_id().insert_review_by_id(session.get('user')['accountId'],data.get("rating"),data.get("comment"))
            return jsonify({'success': True})
    else:
        return redirect(url_for('login'))

@app.route('/insert_followList/<string:followedId>', methods=['GET', 'POST'])
def insert_followList(followedId):
    if session.get('user'):
        InsertFollowListById().insert_followList_by_id(session.get('user')['accountId'],followedId)
        return jsonify({'success': True})
    else:
        return redirect(url_for('login'))

@app.route('/remove_follower_in_followList/<string:followedId>', methods=['GET', 'POST'])
def remove_follower_in_followList(followedId):
    if session.get('user'):
        RemoveFollowerInFollowListById().remove_follower_in_followList_by_id(session.get('user')['accountId'],followedId)
        return jsonify({'success': True})
    else:
        return redirect(url_for('login'))
@app.route('/toggle-notification',methods=['GET','POST'])
def toggle_notification():
    if session.get('user'):
        data = request.json
        UpdateFollowerInFollowListById().update_follower_in_followList_by_id(session.get('user')['accountId'],data["followId"],data["notifyMe"])
        return jsonify({'success': True})
    else:
        return redirect(url_for('login'))
@app.route('/search/<string:content>')
def search(content):
    if session.get('user'):
        accountsList = GetAccountsByUserName().get_accounts_by_userName(content,session.get('user')['accountId'])
        accountFavoList = GetFollowListByAccountId().get_followList_by_accountId_List(session.get('user')['accountId'])
        stockWatchList = GetWatchlistByAccountID().get_watchlist_by_accountID(session.get('user')['accountId'])
        return render_template("/system/search.html",content=content,accountsList=accountsList,stockWatchList=stockWatchList,accountFavoList=accountFavoList)
    return redirect(url_for('login'))

@app.route('/mainPage', methods=['GET', 'POST'])
def mainPage():
    if session.get('user'):
        if session.get('user')['profile'] == 'premium':
            watchList = GetWatchlistByAccountID().get_watchlist_by_accountID(session['user']['accountId'])
            return render_template('mainPage.html',account=session['user'],watchList=watchList)
        elif session.get('user')['profile'] == 'free':
            pass
    else:
        return redirect(url_for('login'))

#remove notification
@app.route('/remove_notification', methods=['POST'])
def remove_notification():
    if session.get('user'):
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
    else:
        return redirect(url_for('login'))

# user login main page
@app.route('/recommendation_news/<int:page>', methods=['GET', 'POST'])
def recommendation_news(page):
    if session.get('user'):
        preference = GetPreferenceByAccountId().get_preference_by_accountId(session['user']['accountId'])
        country = ','.join(preference['preferenceCountry'])
        industry = ','.join(preference['preferenceIndustry'])
        result = NewsController().get_recommendation_news(country,industry,str(page))
        return jsonify(result)
    else:
        return redirect(url_for('login'))
# user login main page
@app.route('/recommendation_symbol', methods=['GET', 'POST'])
def recommendation_symbol():
    if session.get('user'):
        return jsonify(RecommendationListController().get_recommendationList_by_accountId(session.get('user')['accountId']))
    else:
        return redirect(url_for('login'))
@app.route('/get_notification',methods=['GET', 'POST'])
def get_notification():
    if session.get('user'):
        return jsonify(NotificationController().get_notifications_by_accountId(session.get('user')['accountId']))
    else:
        return redirect(url_for('login'))

@app.route('/symbol_news/<string:symbol>/<int:page>', methods=['GET', 'POST'])
def symbol_news(symbol,page):
    if session.get('user'):
        return jsonify(NewsController().get_news_by_symbol(symbol,str(page)))
    else:
        return redirect(url_for('login'))

@app.route("/searchSymbol/<string:symbol>", methods=['GET', 'POST'])
def searchSymbol(symbol):
    if session.get('user'):
        if request.method == 'POST':
            return jsonify(StockDataController().search_stock(symbol))
    else:
        return redirect(url_for('login'))
@app.route('/delete_comment_by_id/<string:commentId>',methods=['POST'])
def delete_comment_by_id(commentId):
    if session.get('user'):
        CommentController().delete_comment_by_id(commentId)
        return jsonify({'success': True})
    else:
        return redirect(url_for('login'))

@app.route('/symbol/<string:symbol>',methods=['GET','POST'])
def symbol(symbol):
    if session.get('user'):
        if session.get('user')['profile'] == 'premium':
            user = GetAccountByAccountId().get_account_by_accountId(session.get('user')['accountId'])
            stockData = StockDataController().get_update_stock_data(symbol,"1y")
            stockInfo = StockDataController().get_stock_info_full(symbol)
            predictionresult = GetPredictionDataBySymbol().get_predictionData_by_symbol(symbol)
            threshold = Get_threshold_by_symbol_and_id().get_threshold_by_symbol_and_id(session.get('user')['accountId'],symbol)
            watchList = GetWatchlistByAccountID().get_watchlist_by_accountID(session.get('user')['accountId'])
            return render_template('/PremiumUser/symbolPage.html', stockData=stockData,stockInfo=stockInfo,predictionresult=predictionresult,threshold=threshold,watchList=watchList,user=user)
        elif session.get('user')['profile'] == 'free':
            pass
    else:
        return redirect(url_for('login'))
@app.route('/request_for_prediction/<string:symbol>/<string:days>/<string:model>', methods=['GET', 'POST'])
def request_for_prediction(symbol, days, model):
    if session.get('user'):
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
        NotificationController().set_notification(session.get('user')['accountId'], f"Prediction for {symbol} is completed.", 'Prediction', prediction_id, symbol)

        return jsonify({'success': True, 'prediction_result': prediction_result})
    else:
        return redirect(url_for('login'))

@app.route('/submit_comment',methods=["POST"])
def submit_comment():
    if session.get('user'):
        data = request.json
        CommentController().insert_comment(session.get('user')['accountId'],data["symbol"],data["comment"])
        return jsonify({'success': True})
    else:
        return redirect(url_for('login'))
@app.route('/update_watchList',methods=['POST'])
def update_watchList():
    if session.get('user'):
        data = request.json
        UpdateWatchlist().update_Watchlist(session.get('user')['accountId'],data.get("watchList"))
        return jsonify({'success': True})
    else:
        return redirect(url_for('login'))

@app.route("/update_threshold_setting/<string:symbol>/<string:threshold>", methods=['POST'])
def update_threshold_setting(symbol, threshold):
    if session.get('user'):
        Update_threshold_settings().update_threshold_settings(session.get('user')['accountId'], symbol, float(threshold))
        return jsonify({'success': True})
    else:
        return redirect(url_for('login'))
@app.route('/symbol_comments/<string:symbol>')
def symbol_comments(symbol):
    if session.get('user'):
        return jsonify(CommentController().get_comments_by_symbol(symbol))
    else:
        return redirect(url_for('login'))


@app.route('/preferenceSetup', methods=['GET', 'POST'])
def preferenceSetup():
    if session.get('user'):
        return render_template("/system/preferenceSetUp.html")
    else:
        return redirect(url_for('login'))


@app.route('/stock_info_minimum/<string:symbol>', methods=['GET'])
def stock_info_minimum(symbol):
    if session.get('user'):
        return jsonify(StockDataController().get_stock_info_minimum(symbol))
    else:
        return redirect(url_for('login'))

@app.route('/update_stock_data/<string:symbol>/<string:period>', methods=['GET'])
def update_stock_data(symbol, period):
    if session.get('user'):
        result = StockDataController().get_update_stock_data(symbol, period)
        print(len(result))
        return jsonify(result)
    else:
        return redirect(url_for('login'))

@app.route('/stock_data_medium/<string:symbol>',methods=['GET'])
def stock_data_medium(symbol):
    if session.get('user'):
        return jsonify(StockDataController().get_stock_info_medium(symbol))
    else:
        return redirect(url_for('login'))

@app.route('/stock_info_full/<string:symbol>', methods=['GET'])
def stock_info_full(symbol):
    if session.get('user'):
        return jsonify(StockDataController().get_stock_info_full(symbol))
    else:
        return redirect(url_for('login'))

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
@app.route('/detectDuplicateEmail',methods=['GET','POST'])
def detectDuplicateEmail():
    data = request.json
    email = data["email"]
    account = GetAllAccount().get_all_account()
    for i in account:
        if i["email"] == email:
            return jsonify({"success": False,'error':"Duplicate email, try to login"})
    return jsonify({"success": True})

@app.route('/verifyEmailCode',methods=['POST'])
def verifyEmailCode():
    try:
        data = request.json
        email = data.get('account')['email']
        code = data.get('code')
        account = data.get('account')
        EmailVerificationController().verify_code(email,code)
        session['user'] = SignupController().individualSignUp(**account)
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
            session['user'] = LoginController().login(email, password)
            return jsonify({'success':True})
        except Exception as e:
            return jsonify({'success':False,'error':str(e)})

@app.route('/updatePersonalInfo', methods=['POST'])
def updatePersonalInfo():
    if session.get('user'):
        account = request.json.get('userAccount')

        if not account:
            return jsonify({'success': False, 'error': 'Invalid input'}), 400

        try:
            if account['profile'] != "admin":
                update_result = UpdatePersonalInfoController().update_personal_info(account)
                if update_result:
                    # Update session['user']
                    session['user'].update(account)
                    return jsonify({'success': True})
                else:
                    return jsonify({'success': False, 'error': 'Failed to update personal info in the database'}), 500
            else:
                # depends on how we want to do, whether we want to allow admins to update personal info
                return jsonify({'success': False, 'error': 'Admins cannot update personal info this way'}), 403
        except Exception as e:
            return jsonify({'success': False, 'error': str(e)}), 500
    else:
        return redirect(url_for('login'))

@app.route('/changePassword', methods=['POST'])
def change_password():
    if session.get('user'):
        try:
            old_password = request.json.get('oldPassword')
            new_password = request.json.get('newPassword')
            # Determine whether the user's entered previous password is correct or not
            if hashlib.md5(old_password.encode()).hexdigest() != session['user']['hashedPassword']:
                raise Exception('Invalid old password')
            # if it is correct, then change current password
            session['user']['hashedPassword'] = ChangePasswordController().update_password_by_accountId(session['user']['accountId'],
                                                                                                  new_password)
            session.modified = True
            return jsonify({'success': True})
        except Exception as e:
            return jsonify({'success': False,'error':str(e)})
    else:
        return redirect(url_for('login'))

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
    if session.get('user'):
        return jsonify(GetPredictionDataBySymbol().get_predictionData_by_symbol(symbol))
    else:
        return redirect(url_for('login'))
@app.route('/history',methods=['GET'])
def history():
    if session.get('user'):
        history = Get_searchHistory_by_id().get_searchHistory_by_id(session.get('user')['accountId'])
        return render_template("system/history.html",history=history)
    else:
        return redirect(url_for('login'))

@app.route('/remove_searchHistory/<string:id>',methods=['POST'])
def remove_searchHistory(id):
    if session.get('user'):
        RemoveSearchHistory().remove_searchHistory_by_id(id)
        return jsonify({'success':True})
    else:
        return redirect(url_for('login'))
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
    if session.get('user'):
        if request.method == 'GET':
            return render_template("/system/industry.html")
        data = request.json
        session['industry'] = data.get("selectedIndustries")
        return jsonify({'success': True})
    else:
        return redirect(url_for('login'))

@app.route('/country_Setting',methods=['GET','POST'])
def country_Setting():
    if session.get('user'):
        if request.method == 'GET':
            return render_template("/system/country.html")
        data = request.json
        session['country'] = data.get("selectedCountries")
        return jsonify({'success': True})# Dynamically checking that user-selected stocks have not exceeded thresholds
    else:
        return redirect(url_for('login'))
@app.route('/configure_personal_setting',methods=['GET','POST'])
def configure_personal_setting():
    if session.get('user'):
        if request.method == 'GET':
            return render_template("/system/configure_personal_settings.html")
        if request.method == 'POST':
            UpdatePreferenceByAccountId().update_preference_by_accountId(session['user']['accountId'],session['industry'],session['country'])
            return jsonify({'success': True})
    else:
        return redirect(url_for('login'))

@app.route('/pricing',methods=['GET','POST'])
def pricing():
    return render_template("/system/pricing.html")

@app.route('/admin/allUser',methods=['GET','POST'])
def adminAllUser():
    if session.get('user'):
        if request.method == 'GET':
            allAccounts = GetAllAccount().get_all_account()
            return render_template('/Admin/adminShowAllUser.html',allAccounts=allAccounts)
        if request.method == 'POST':
            data = request.json
            UpdateProfileStatus().update_profile_status(data['Account']["accountId"],data['Account']["status"])
            return jsonify({'success': True})
    else:
        return redirect(url_for('login'))
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
