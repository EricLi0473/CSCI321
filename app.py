from flask import Flask, request, render_template, redirect, url_for



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

@app.route('/adminRegister')
def adminLoginPage():
    return render_template('front-end page/adminSystem/adminRegister.html')

@app.route('/adminMain')
def adminLoginPage():
    return render_template('front-end page/adminSystem/adminMainPage.html')
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80,debug=True)