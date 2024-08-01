import os
import sys

from Control.User.UpdatePersonalInfoController import UpdatePersonalInfoController
from Control.User.loginController import LoginController

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
from flask import request, render_template, url_for, jsonify,session,send_file,abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from Control.User.SignupController import *
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
from Control.User.reset_pwd import *
from Control.User.verify_account_by_email import *
from Control.Admin.get_all_reviews import *
from Control.Admin.delete_review_by_id import *
from Control.User.insert_searchHistory_by_id import *
from Control.User.get_all_predictionData import *
from Control.User.get_review_by_accountId import *
from Control.premiumUser.verifyApiKeyController import *
from Control.premiumUser.verify_symbol_usingYfinance import *
from Control.premiumUser.getPremiumUsersController import *
from Control.premiumUser.get_accountList_by_followedId import *
from Control.User.delete_predictionData_by_id import *
from Control.premiumUser.set_preference_by_accountId import *
from Control.User.reset_mlView import *
from Control.User.detectDuplicateEmail import *
from Control.Admin.get_all_precessing_predictionData import *
from Control.User.get_AllThresholds_by_account import *
from Control.User.sendEmailController import *
import hashlib
from flask import Flask, redirect
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
# from machineLearningModel.GRU_Model import *
# from machineLearningModel.LSTM_Model import *
# from machineLearningModel.prophet_model import *
# from Control.User.storePredictionResultController import *
# from machineLearningModel.get_symbol_data import *
import threading
import time
from captcha.image import ImageCaptcha
import random
import io
from apscheduler.schedulers.background import BackgroundScheduler
import concurrent.futures
# disable output
# sys.stdout = open(os.devnull,'w')
# sys.stderr = open(os.devnull,'w')
app = Flask(__name__)
app.static_folder = 'static'
app.secret_key = 'csci314'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per minute"]
)

@app.route('/generate_captcha')
@limiter.limit("100 per minute")
def generate_captcha():
    image = ImageCaptcha()
    captcha_text = ''.join(random.choices('1234567890', k=5))
    session['captcha'] = captcha_text
    data = image.generate(captcha_text)
    img_io = io.BytesIO(data.read())
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')

@app.route('/verify_captcha', methods=['POST'])
def verify_captcha():
    user_captcha = request.json.get('captcha')
    account = request.json.get('account')
    rememberMe = request.json.get('rememberMe')
    if user_captcha and user_captcha == session.get('captcha'):
        # handle user has already login
        session['user'] = account
        session.pop('captcha')
        if rememberMe:
            session.permanent = False
        else:
            session.permanent = True
        return jsonify({'success': True})
    return jsonify({'success': False})

@app.route('/upgrade_to_premium',methods=['POST'])
def upgrade_to_premium():
    account = request.json.get('account')
    UpdatePersonalInfoController().update_personal_info(account)
    session['user'] = GetAccountByAccountId().get_account_by_accountId(session['user']['accountId'])
    return jsonify({'success': True})
@app.route('/like_comment/<int:comment_id>', methods=['POST'])
def like_comment(comment_id):
    try:
        # Increment the like count in the database for the comment with comment_id
        CommentController().update_comment_likes(comment_id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/dislike_comment/<int:comment_id>', methods=['POST'])
def dislike_comment(comment_id):
    try:
        # Increment the dislike count in the database for the comment with comment_id
        CommentController().update_comment_dislikes(comment_id)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/preference',methods=['GET','POST'])
def preference():
    if session.get('user'):
        preference = GetPreferenceByAccountId().get_preference_by_accountId(session.get('user')['accountId'])
        return render_template("/premiumUser/preference.html",preference=preference,account=session.get('user'))

    else:
        return redirect(url_for('login'))
@app.route('/space/<string:accountId>',methods=['GET','POST'])
def space(accountId):
    if session.get('user'):
        if request.method == 'GET':
            account = GetAccountByAccountId().get_account_by_accountId(accountId)
            #  admin access admin page
            if session.get('user')['profile'] == 'admin' and account['profile'] == 'admin':
                return render_template('/Admin/adminSpace.html',account=session.get('user'))
            # access self page
            if int(accountId) == session.get('user')['accountId']:
                watchList = GetWatchlistByAccountID().get_watchlist_by_accountID(session.get('user')['accountId'])
                account = GetAccountByAccountId().get_account_by_accountId(session.get('user')['accountId'])
                thresholdList = GetThresholdSettingById().get_threshold_settings_by_id(session.get('user')['accountId'])
                return render_template("/User/mySpace.html",account=account,watchList=watchList,thresholdList=thresholdList,user=session.get("user"))
            # access other user page
            elif int(accountId) != session.get('user')['accountId']:
                # non admin user are prohibits to access admin account page
                if account['profile'] == 'admin':
                    return redirect(url_for('login'))
                accountFavoList = GetFollowListByAccountId().get_followList_by_accountId_List(session.get('user')['accountId'])
                watchList = GetWatchlistByAccountID().get_watchlist_by_accountID(accountId)
                thresholdList = GetThresholdSettingById().get_threshold_settings_by_id(accountId)
                return render_template("/User/otherUserSpace.html",accountFavoList=accountFavoList,account=account,watchList=watchList,thresholdList=thresholdList,Account=session.get('user'))

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
            return render_template("/system/friend.html",followList=followList,who_follow_me_list=who_follow_me_list,account=account, user=session.get("user"))
    else:
        return redirect(url_for('login'))
@app.route('/ratingComment', methods=['GET', 'POST'])
def ratingComment():
    if session.get('user'):
        if request.method == 'GET':
            userReview = GetReviewByAccountId().get_review_by_accountId(session.get('user')['accountId'])
            return render_template("/system/RatingComment.html",user=session.get("user"),userReview=userReview)
        if request.method == 'POST':
            data = request.json
            Insert_review_by_id().insert_review_by_id(session.get('user')['accountId'],data.get("rating"),data.get("comment"))
            return jsonify({'success': True})
    else:
        return redirect(url_for('login'))
@app.route('/getRatingCommentById', methods=['GET'])
def getRatingCommentById():
    if session.get('user'):
        return jsonify(GetReviewByAccountId().get_review_by_accountId(session.get('user')['accountId']))
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
        return render_template("/system/search.html",content=content,accountsList=accountsList,stockWatchList=stockWatchList,accountFavoList=accountFavoList,user=session['user'])
    return redirect(url_for('login'))
@app.route('/search/')
def searchRe():
    if session.get('user'):
        return search("")
    else:
        return redirect(url_for('login'))
@app.route('/mainPage', methods=['GET', 'POST'])
def mainPage():
    if session.get('user'):
        if session.get('user')['profile'] == 'premium':
            watchList = GetWatchlistByAccountID().get_watchlist_by_accountID(session['user']['accountId'])
            global free_user_stockData_cache
            return render_template('/premiumUser/mainPage.html',user=session['user'],watchList=watchList,commonSymbol = free_user_stockData_cache)
        elif session.get('user')['profile'] == 'free':
            watchList = GetWatchlistByAccountID().get_watchlist_by_accountID(session['user']['accountId'])
            return render_template('/individualFreeUser/mainPage.html', user=session['user'], watchList=watchList)
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
        Remove_notification_by_id().remove_notification_by_id(notificationId)

        return jsonify({'success': True})
    else:
        return redirect(url_for('login'))

# user login main page
@app.route('/recommendation_news/<int:page>', methods=['GET', 'POST'])
def recommendation_news(page):
    if session.get('user'):
        if session.get('user')['profile'] == 'premium':
            preference = GetPreferenceByAccountId().get_preference_by_accountId(session['user']['accountId'])
            country = ','.join(preference['preferenceCountry'])
            industry = ','.join(preference['preferenceIndustry'])
            result = NewsController().get_recommendation_news(country,industry,str(page))
            return jsonify(result)
        elif session.get('user')['profile'] == 'free':
            return jsonify(NewsController().get_common_news(str(page)))
    else:
        return redirect(url_for('login'))
# user login main page
@app.route('/recommendation_symbol', methods=['GET', 'POST'])
def recommendation_symbol():
    if session.get('user'):
        if session.get('user')['profile'] == 'premium':
            return jsonify(RecommendationListController().get_recommendationList_by_accountId(session.get('user')['accountId']))
        elif session.get('user')['profile'] == 'free':
            global free_user_stockData_cache
            return jsonify(free_user_stockData_cache)
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

@app.route('/getSimilarSymbol/<string:symbol>', methods=['GET'])
def getSimilarSymbol(symbol):
    if session.get('user'):
        return jsonify(StockDataController().get_similar_stock_data(symbol))
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
            user = session.get('user')
            stockInfo = StockDataController().get_stock_info_full(symbol)
            predictionresult = GetPredictionDataBySymbol().get_predictionData_by_symbol(symbol)
            threshold = Get_threshold_by_symbol_and_id().get_threshold_by_symbol_and_id(session.get('user')['accountId'],symbol)
            watchList = GetWatchlistByAccountID().get_watchlist_by_accountID(session.get('user')['accountId'])
            return render_template('/PremiumUser/symbolPage.html', stockInfo=stockInfo,predictionresult=predictionresult,threshold=threshold,watchList=watchList,user=user)
        elif session.get('user')['profile'] == 'free':
            user = session.get('user')
            stockInfo = StockDataController().get_stock_info_full(symbol)
            predictionresult = GetPredictionDataBySymbol().get_predictionData_by_symbol(symbol)
            threshold = Get_threshold_by_symbol_and_id().get_threshold_by_symbol_and_id(
                session.get('user')['accountId'], symbol)
            watchList = GetWatchlistByAccountID().get_watchlist_by_accountID(session.get('user')['accountId'])
            return render_template('/individualFreeUser/freeUserSymbolPage.html', stockInfo=stockInfo,
                                   predictionresult=predictionresult, threshold=threshold, watchList=watchList,
                                   user=user)
    else:
        return redirect(url_for('login'))
@app.route('/request_for_prediction/<string:symbol>/<string:days>/<string:model>/<string:accountId>', methods=['GET', 'POST'])
@limiter.limit("5 per minute")
def request_for_prediction(symbol, days, model,accountId):
    from datetime import datetime
    days = int(days)
    # 1. Pass the parameters to the machine learning model
    prediction_result = None
    default_layers = 4
    default_neurons = 32

    # pre insert prediction result, without final data
    predictionId = storePredictionResultController.pre_store_prediction_result(symbol,days,accountId,model)
    if model == 'GRU':
        df = GRU_Model.get_stock_data(symbol)
        prediction_result = GRU_Model().predict_future_prices(symbol, df, days, default_layers, default_neurons)

        # format of GRU model result
        # [{'Date': '2024-06-29', 'Predicted': 195.99, 'Recommendation': 'Hold'}, {'Date': '2024-06-30', 'Predicted': 193.51, 'Recommendation': 'Hold'}]

    elif model == 'Prophet':
        prediction_result = Prophet_model(symbol, days).predict()

        # format of LR model result
        # [{'Date': '2024-06-29', 'Predicted': 171.28, 'Recommendation': 'Hold'}]

    elif model == 'LSTM':
        end_date = datetime.today().date()
        start_date = (end_date - timedelta(days=365 * 5))
        df = yf.download(symbol, start=start_date, end=end_date)
        all_dates = pd.date_range(start=df.index.min(), end=df.index.max(), freq='D')
        df = df.reindex(all_dates)
        df = df.fillna(method='ffill')
        LSTM_model = LSTM_Model(symbol, df, n_days=days, layers=default_layers, neurons=default_neurons)
        prediction_result = LSTM_model.predict()
        # format of LSTM prediction result
        # [{'Date': '2024-06-29', 'Predicted': 202.17, 'Recommendation': 'Hold'}]

    else:
        return jsonify({'success': False, 'error': 'Invalid model'}), 400

    if not prediction_result:
        return jsonify({'success': False, 'error': 'Prediction failed'}), 500

    # 2. Store the prediction result in the database
    storePredictionResultController.store_prediction_result(predictionId,symbol, prediction_result,accountId,model)

    # 3. Store a notification
    #def set_notification(self, accountId, notification, notificationType, referenceId, symbol):
    NotificationController().set_notification(accountId, f"Prediction for {symbol} is completed.", 'Prediction', predictionId, symbol)
    # email
    account = GetPreferenceByAccountId().get_preference_by_accountId(accountId)
    if account['receiveNotification'] == 1:
        sendEmailController().send_Notification(account['email'],f"Prediction for {symbol} is completed.")
    return jsonify({'success': True, 'prediction_result': prediction_result})


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
    result = StockDataController().get_update_stock_data(symbol, period)
    return jsonify(result)


@app.route('/stock_data_medium/<string:symbol>',methods=['GET'])
def stock_data_medium(symbol):
    if session.get('user'):
        return jsonify(StockDataController().get_stock_info_medium(symbol))
    else:
        return redirect(url_for('login'))

@app.route('/stock_info_full/<string:symbol>', methods=['GET'])
def stock_info_full(symbol):
    return jsonify(StockDataController().get_stock_info_full(symbol))


@app.route('/emailVerification',methods=['GET','POST'])
def emailVerification():
    if request.method == "GET":
        return render_template("/system/emailVerification.html")
    if request.method == "POST":
        # here to sent email, not verification
        data = request.json
        if data.get('status') == "signup":
            email = data["email"]
            EmailVerificationController().send_verification_code(email)
            return jsonify({"success": True})
        elif data.get('status') == "resetPwd":
            if VerifyAccountByEmail().verify_account_by_email(data["email"]):
                EmailVerificationController().send_verification_code(data["email"])
                return jsonify({"success": True})
            else:
                return jsonify({"success": False})

@app.route('/detectDuplicateEmail',methods=['GET','POST'])
def detectDuplicateEmail():
    data = request.json
    email = data["email"]
    if DetectDuplicateEmail().detectDuplicateEmail(email) == 1:
        return jsonify({"success": False, 'error': "Duplicate email, try to login"})
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
        Set_preference_by_accountId().set_preference_by_accountId(session['user']['accountId'],"Technology","us")
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


@app.route('/reset_pwd',methods=['POST','GET'])
def reset_pwd():
    if request.method == "POST":
        data = request.json
        EmailVerificationController().verify_code(data.get('email'), data.get('code'))
        ResetPwd().reset_pwd(data.get('email'),data.get('password'))
        return jsonify({"success": True})
    elif request.method == "GET":
        return render_template('/system/ResetPassword.html')
@app.route('/signup',methods=['GET'])
def signup():
    return render_template("system/signup.html")
@app.route('/login', methods=['POST','GET'])
@limiter.limit("100 per minute")
def login():
    if request.method == 'GET':
        return render_template("system/login.html")
    if request.method == 'POST':
        try:
            data = request.json
            email = data.get('email')
            password = data.get('password')
            account = LoginController().login(email, password)
            return jsonify({'success':True,'account':account})
        except Exception as e:
            return jsonify({'success':False,'error':str(e)})

@app.route('/updatePersonalInfo', methods=['POST'])
def updatePersonalInfo():
    if session.get('user'):
        account = request.json.get('userAccount')

        if not account:
            return jsonify({'success': False, 'error': 'Invalid input'}), 400

        try:
            update_result = UpdatePersonalInfoController().update_personal_info(account)
            if update_result:
                session['user'] = account
                return jsonify({'data': account})
            else:
                return jsonify({'success': False, 'error': 'Failed to update personal info in the database'}), 500
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
@limiter.limit("10 per minute")
def officialWeb():
    global mainPage_stockData_cache
    predictionData = GetPredictionDataBySymbol().get_predictionData_by_symbol("AAPL")
    review = GetAllHeadLineReviews().get_all_headline_reviews()
    global free_user_stockData_cache
    return render_template("system/template.html",predictionData=predictionData,review=review,commonSymbol=free_user_stockData_cache)

@app.route('/getSystemStats',methods=['GET'])
def getSystemStats():
    usersCount = len(GetAllAccount().get_all_account())
    predictionCount = len(GetAllPredictionData().get_all_predictionData("2024-06-12"))
    return jsonify({'usersCount':usersCount,'prediction':predictionCount,'symbol':5000})

@app.route('/get_predictionData_by_symbol/<string:symbol>',methods=['GET'])
def get_predictionData_by_symbol(symbol):
    return jsonify(GetPredictionDataBySymbol().get_predictionData_by_symbol(symbol))

@app.route('/history',methods=['GET'])
def history():
    if session.get('user'):
        history = Get_searchHistory_by_id().get_searchHistory_by_id(session.get('user')['accountId'])
        return render_template("system/history.html",history=history, user=session.get("user"))
    else:
        return redirect(url_for('login'))
@app.route('/insert_searchHistory/<string:symbol>',methods=['GET','POST'])
def insert_searchHistory(symbol):
    if session.get('user'):
        InsertSearchHistoryById().insert_searchHistory_by_id(session.get('user')['accountId'],symbol)
        return jsonify({'success': True})
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
        if session.get('user')['profile'] != 'admin':
            return redirect(url_for('mainPage'))
        else:
            return redirect(url_for("adminMainPage"))
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

@app.route('/update_ReceiveNotification/<string:receiveNotification>',methods=['GET','POST'])
def update_ReceiveNotification(receiveNotification):
    if session.get('user'):
        UpdatePreferenceByAccountId().update_ReceiveNotification_by_accountId(session['user']['accountId'],receiveNotification)
        return jsonify({'success': True})
    else:
        return redirect(url_for('login'))
@app.route('/pricing',methods=['GET','POST'])
def pricing():
    return render_template("/system/pricing.html")

@app.route('/admin/allUser',methods=['GET','POST'])
def adminAllUser():
    if session.get('user'):
        if session.get('user')['profile'] != 'admin':
            return redirect(url_for('login'))
        if request.method == 'GET':
            allAccounts = GetAllAccount().get_all_account()
            return render_template('/Admin/adminShowAllUser.html',allAccounts=allAccounts,account=session.get('user'))
        if request.method == 'POST':
            data = request.json
            UpdateProfileStatus().update_profile_status(data['Account']["accountId"],data['Account']["status"])
            return jsonify({'success': True})
    else:
        return redirect(url_for('login'))

@app.route('/admin/review',methods=['GET','POST'])
def adminReview():
    if session.get('user'):
        if session.get('user')['profile'] != 'admin':
            return redirect(url_for('login'))
        if request.method == 'GET':
            reviews = Get_all_reviews().get_all_reviews()
            return render_template('/Admin/adminViewAllComment.html',reviews=reviews,account=session.get('user'))
    else:
        return redirect(url_for('login'))
@app.route('/admin/mainPage',methods=['GET'])
def adminMainPage():
    if session.get('user'):
        if session.get('user')['profile'] != 'admin':
            return redirect(url_for('login'))
        stats = [len(GetAllAccount().get_all_account()),len(GetAllPredictionData().get_all_predictionData("1970-01-01")),len(GetAllPrecessingPredictionData().get_all_precessing_predictionData()),len(Get_all_reviews().get_all_reviews())]
        return render_template('/Admin/mainPage.html',account=session['user'],stats=stats)
    else:
        return redirect(url_for('login'))

@app.route('/admin/allPredictions',methods=['GET','POST'])
def adminAllPredictions():
    from datetime import datetime
    if session.get('user'):
        if session.get('user')['profile'] != 'admin':
            return redirect(url_for('login'))
        predictions = GetAllPredictionData().get_all_predictionData("1970-01-01")
        return render_template('/Admin/adminPredictionData.html', predictions=predictions,account=session.get('user'))
    else:
        return redirect(url_for('login'))

@app.route('/predictionData',methods=['GET','POST'])
def predictionData():
    from datetime import datetime
    if session.get('user'):
        if session.get('user')['profile'] != 'premium':
            return redirect(url_for('login'))
        return render_template('/premiumUser/predictionData.html',user=session['user'],predictions=GetAllPredictionData().get_predictionData_by_accountId(session['user']['accountId'],"1970-01-01"))
    else:
        return redirect(url_for('login'))

@app.route('/getALLPredictionData',methods=['GET','POST'])
def getALLPredictionData():
    if session.get('user'):
        if session.get('user')['profile'] != 'admin':
            return redirect(url_for('login'))
        data = request.json
        return GetAllPredictionData().get_all_predictionData(data.get('date'))
    else:
        return redirect(url_for('login'))
@app.route('/getALLPredictionDataBy_accountId',methods=['GET','POST'])
def getALLPredictionDataBy_accountId():
    if session.get('user'):
        data = request.json
        return GetAllPredictionData().get_predictionData_by_accountId(session['user']['accountId'],data.get('date'))
    else:
        return redirect(url_for('login'))
@app.route('/deletePredictionData',methods=['GET','POST'])
def deletePredictionData():
    if session.get('user'):
        data = request.json
        DeletePredictionDataByID().delete_prediction_data_by_id(data.get("predictionId"))
        return jsonify({'success': True})
    else:
        return redirect(url_for('login'))
@app.route('/deleteReview/<string:reviewId>',methods=['GET','POST'])
def deleteReview(reviewId):
    if session.get('user'):
        DeleteReviewById().delete_review_by_id(reviewId)
        return jsonify({'success': True})
    else:
        return redirect(url_for('login'))
@app.route('/api',methods=['GET'])
def api():
    if session.get('user'):
        return render_template('/premiumUser/apiPage.html',user=session.get('user'))
    else:
        return redirect(url_for('login'))

@app.route('/payment',methods=['GET','POST'])
def payment():
    if session.get('user'):
        return render_template('/User/payment.html',user=session.get('user'))
    else:
        return redirect(url_for('login'))

@app.route('/signUpPayment',methods=['GET','POST'])
def signUpPayment():
    return render_template('/User/signUpPayment.html')

@app.route('/api/get',methods=['GET'])
def apiGetPrediction():
    try:
        key = request.args.get('key')
        symbol = request.args.get('symbol')
        VerifyApiKeyController().verifyApiKey(key)
        result  = GetPredictionDataBySymbol().get_predictionData_by_symbol(symbol)
        result.pop("predictionId", None)
        result.pop("accountId", None)
        if not result:
            raise Exception("This symbol do not have prediction data this time")
        return jsonify({'prediction': result})
    except Exception as e:
        return jsonify({'error':str(e)})

@app.route('/api/request',methods=['GET'])
def apiRequest():
    try:
        vmodel = ['fast','balance','accuracy']
        vdays = ["7","14","30"]
        key = request.args.get('key')
        symbol = request.args.get('symbol')
        model = request.args.get('model')
        days = request.args.get('days')
        if model not in vmodel:
            raise Exception("not supported model")
        if days not in vdays:
            raise Exception("not supported days")
        # verify end
        days = int(days)
        verify_symbol_usingYfinance().verify_symbol_usingYfinance(symbol)
        account = VerifyApiKeyController().verifyApiKey(key)
        model_mapping = {
            'accuracy': 'LSTM',
            'balance': 'GRU',
            'fast': 'Prophet'
        }
        model = model_mapping[model]

        url = f'http://127.0.0.1/request_for_prediction/{symbol}/{days}/{model}/{account["accountId"]}'

        def send_request():
            response = requests.get(url)

        prediction = threading.Thread(target=send_request)
        prediction.daemon = True
        prediction.start()

        return jsonify({"success":"You have successfully submitted a request. Login your account to get result"})
    except Exception as e:
        return jsonify({'error': str(e)})


ip_404_counter = {}
blacklist = set()
THRESHOLD = 10

@app.errorhandler(404)
def page_not_found(e):
    remote_addr = get_remote_address()

    if remote_addr in blacklist:
        return "You are blacklisted.", 403

    ip_404_counter[remote_addr] = ip_404_counter.get(remote_addr, 0) + 1

    if ip_404_counter[remote_addr] > THRESHOLD:
        blacklist.add(remote_addr)
        return "You are blacklisted.", 403

    return render_template('/system/404.html'), 404

@app.errorhandler(429)
def page_not_found(e):
    return render_template('/system/429.html'), 429
#
# DO NOT REMOVE, THIS IS SCHEDULE FUNCTION!!!!!
#
# Define cache
notification_cache = {}
free_user_stockData_cache = []

def cache_when_startUp():
    global free_user_stockData_cache
    free_user_stockData_cache = StockDataController().get_common_symbol_data()

def threshold_notification():
    global notification_cache
    for user in GetAllThresholdsByAccount().get_all_thresholds_by_account():
        cache_key = (user['accountId'], user["stockSymbol"], user["changePercentage"])
        current_time = time.time()
        if cache_key not in notification_cache or (current_time - notification_cache[cache_key] > 10800):  # three hour
            symbol = StockDataController().get_stock_info_minimum(user["stockSymbol"])
            if abs(symbol["relative_change"]) > user['changePercentage']:
                # Checking for recent notifications
                notificationWord = f"Hi, Your followed {user['stockSymbol']} that exceeds your threshold."
                NotificationController().set_notification(user['accountId'], notificationWord, "threshold", user['thresholdId'],user['stockSymbol'])
                # email
                if user['receiveNotification']:
                    sendEmailController().send_Notification(user['email'],notificationWord)
                notification_cache[cache_key] = current_time
                for userFollow in GetAccountListByFollowedId().get_accountList_by_followedId(user['accountId']):
                    if userFollow['notifyMe'] == 1:
                        notificationWord = f"There have been updates to stock {user['stockSymbol']} for user {userFollow['userName']} you follow! Please check"
                        hashed_symbol = int(hashlib.md5(user['stockSymbol'].encode()).hexdigest(),16)%(2**31-1)
                        NotificationController().set_notification(userFollow['followListAccountId'],notificationWord,"friend_threshold",hashed_symbol,user['stockSymbol'])
                    #email
                        if user['receiveNotification']:
                            sendEmailController().send_Notification(user['email'],notificationWord)
def daily_task():
    # update ml prediction every day
    cache_when_startUp()
    # Reset the number of times a free user can view ml prediction per day
    reset_mlView().reset_mlView()
    #  update personal interested
    for accountId in GetPremiumUsersController().getPremiumUsers():
        preference = GetPreferenceByAccountId().get_preference_by_accountId(accountId)
        UpdatePreferenceByAccountId().update_preference_by_accountId(accountId,preference['preferenceIndustry'],preference['preferenceCountry'])

def start_threshold_notification_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(threshold_notification, 'interval', seconds=30)
    scheduler.start()

def start_daily_task_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(daily_task, 'cron', hour=5, minute=00)
    scheduler.start()

if __name__ == '__main__':

    # threshold_scheduler_thread = threading.Thread(target=start_threshold_notification_scheduler)
    # threshold_scheduler_thread.daemon = True
    # threshold_scheduler_thread.start()
    #
    # daily_task_scheduler_thread = threading.Thread(target=start_daily_task_scheduler)
    # daily_task_scheduler_thread.daemon = True
    # daily_task_scheduler_thread.start()
    # #
    cache_whenStartUP = threading.Thread(target=cache_when_startUp)
    cache_whenStartUP.start()

    try:
        app.run(host='0.0.0.0', port=80, debug=True,threaded=True)
    finally:
        pass
