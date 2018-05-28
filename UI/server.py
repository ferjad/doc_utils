import os
from flask import Flask, render_template, request
import requests
import socket
app = Flask(__name__)

# folder to save files
UPLOAD_FOLDER = os.path.basename('uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = ['.png', '.jpg', '.jpeg', '.gif','.tiff']

# load index.html on start
@app.route('/')
def start_up():
    return render_template('index.html')

# save file on upload
@app.route('/upload', methods=['POST'])
def upload_file():

    #output strings
    classifyout = ""
    tessout = ""
    dateout = ""
    invalidImage = False

    #get image file
    file = request.files['image']
    #get filename
    filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    if(os.path.splitext(filename)[1] in ALLOWED_EXTENSIONS):
        #save file
        file.save(filename)


        #if tesseract output checked, return the text output
        if(request.form.get('tesseract')):
            urltess = "http://tesseract:9200"
            fin = open(filename, 'rb')
            files = {'file': fin}
            try:
                r = requests.post(urltess, files=files)
                tessout = r.text
            finally:
                fin.close()


        #send tesseract output to dateparser if dateparser checked, if tesseract output is unchecked, this will return nothing
        if(request.form.get('dateparser')):

            # if dateparser is checked but tesseract is not checked, run tesseract first
            if not request.form.get('tesseract'):
                urltess = "http://tesseract:9200"
                fin = open(filename, 'rb')
                files = {'file': fin}
                try:
                    r = requests.post(urltess, files=files)
                    tessout = r.text
                finally:
                    fin.close()


            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("parser", 9400))
            s.sendall(tessout.encode())
            data = s.recv(1024)
            dateout=data.decode('utf-8')
            s.close()

        #send file to classifier
        if(request.form.get('classify')):
            urlclassify = "http://111.68.101.28:10000"
            fin = open(filename, 'rb')
            files = {'file': fin}
            try:
                r = requests.post(urlclassify, files=files)
                classifyout = r.text
            finally:
                fin.close()
    else:
        invalidImage = True


    #return template with output
    return render_template('index.html', invalidImage=invalidImage,filename=filename,tessout=tessout, classifyout=classifyout,dateout=dateout,init=True)




if __name__ == "__main__":
    #run server on localhost port 5000
    app.run(host='0.0.0.0', port=5000)
