# doc_utils

A document processing pipeline. The available functionality include:
* Document OCR
* Date Extraction
* Document Classification
* Web UI

The functionalities are implemented as microservices.
# Document OCR
Tesseract OCR is used to perform OCR. The web UI sends the image to the OCR service.
The extracted text is communicated back to the UI server.

# Date Extraction 
The UI server passes the extracted text to a regex based parser written in C# using TCP socket. 
The service is running in a docker container using the .NET core framework.
The extracted date is communicated back to the UI server using TCP socket.
Formats supported are listed on: https://www.c-sharpcorner.com/blogs/date-and-time-format-in-c-sharp-programming1

# Document Classification
A deep neural network is trained to classify documents into 9 classes from the Tobacco dataset. 
classes=['Advertising', 'Email','Form', 'Letter', 'Memo', 'News', 'Note','Report','Resume','Scientific']
Renet 152 is fine tuned by removing the final layer and then training for the mentioned classes for 50 epochs.
The image is passed to the document classifier by the UI server. 
The classifier predicts the class and sends it back to the UI server.

# Web UI
The web UI is operating in a docker and uses TCP to communicate with the above mentioned services. 
The server is based on Flash in Python.

# Set up
Run 'bash setup.sh' from base directory.

# Running the containers
Run 'bash run.sh' from base directory.

# Navigating to the web UI
Go to 'http://localhost:5000" from a Web Browser.
Upload a Image and select the relevant services to use.
The image will be processed and the output will be displayed.
