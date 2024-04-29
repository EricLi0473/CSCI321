from flask import Flask, request, render_template, redirect, url_for
import pandas as pd


app = Flask(__name__)


@app.route('/')
def upload_file():
    return render_template('upload.html')


@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return "No file part"

    file = request.files['file']

    if file.filename == '':
        return "No selected file"

    if file:
        df = pd.read_csv(file)
        process(df)
        return redirect(url_for('upload_file'))  # redirect to main page

def asd():
    pass

def process(df):
    print(df.head())


if __name__ == '__main__':
    app.run(debug=True)
