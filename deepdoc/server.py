# http://flask.pocoo.org/docs/patterns/fileuploads/
import os
from flask import Flask, request, redirect, url_for, send_from_directory
from werkzeug import secure_filename
import requests
import subprocess
import predict
UPLOAD_FOLDER = 'uploads/predict'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
  # this has changed from the original example because the original did not work for me
    return filename[-3:].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_textfile():
    if request.method == 'POST':
        print("request method")
        file = request.files['file']
        if file and allowed_file(file.filename):
            print('**found file', file.filename)
            filename = secure_filename(file.filename)
            print("filename:",'uploads/predict/'+ filename)
            file.save('uploads/predict/'+ filename)
            result = "lalla"
            
            result = predict.predict()
            print("result",result)
            os.system("rm -r uploads/predict/*")
            # for browser, add 'redirect' function on top of 'url_for'
            return result.decode('utf-8')
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=10000)
