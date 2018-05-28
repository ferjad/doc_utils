import os
from flask import Flask, request
from werkzeug import secure_filename
import requests
import subprocess


app = Flask(__name__)

# save files to this folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


#save file on post request
@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        #get the file
        file = request.files['file']
        #if file is present
        if file:
            #get filename
            filename = secure_filename(file.filename)
            #save file
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            #get tesseract output
            result = subprocess.check_output(['tesseract', 'uploads/'+filename,'stdout'])
            
            return result.decode('utf-8')

if __name__ == '__main__':
    #run server on localhost and port 9200
	app.run(host='0.0.0.0', port=9200)
