#!/usr/bin/env python3

from flask import Flask, render_template, Response, send_file
import cv2
from keras import models
import numpy as np
from keras.applications.inception_resnet_v2 import preprocess_input
import time
import logging

import os
import traceback
from flask_socketio import SocketIO, emit

#Initialize the Flask app
app = Flask(__name__)
socketio = SocketIO(app, logger=True, engineio_logger=True)

#Load model and classess
# model_path = os.environ['MODEL_PATH']
# print('model_path: ', model_path)

# model = models.load_model("{0}/FaceRecogn.h5".format(model_path))
# classes = np.genfromtxt("{0}/classes.txt".format(model_path), dtype='str', delimiter='\n')
model = models.load_model("./Model/FaceRecogn.h5")
classes = np.genfromtxt("./Model/classes.txt", dtype='str', delimiter='\n')
print('\nClasses detected:\n', classes)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# camera_url = "{0}:80".format(os.environ['CAMERA_SOURCE_SVC'])
log = logging.getLogger("mylogger")

# err_png = cv2.VideoCapture('./error.png')

@socketio.on('image')
def image(data_image):
    print('Received data image!')
    sbuf = StringIO()
    sbuf.write(data_image)

    # decode and convert into image
    b = io.BytesIO(base64.b64decode(data_image))
    pimg = Image.open(b)

    ## converting RGB to BGR, as opencv standards
    frame = cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)
    
    # # encode frame to CV2 type
    # nparr = np.fromstring(frame, np.uint8)
    # frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=8, minSize=(50,50))
    for (x, y, w, h) in faces:
        #print('Person detected!',x, y, w, h)
        incr_by=20 #in px
        if y>incr_by: y-=incr_by
        if x>incr_by: x-=incr_by
        if h>incr_by: h+=incr_by
        if w>incr_by: w+=incr_by

        #region of interest from picture in color
        roi_color = frame[y:y+h, x:x+w, :]
        
        #Resize dimensions to match the input to model
        img_array = cv2.resize(roi_color, (256, 256))

        #preprocessing input
        i=preprocess_input(img_array)
        input_arr = np.array([i])

        #using model for prediction
        mod_pred=model.predict(input_arr)

        #calculate probability and show label only above 80% of probability
        prob=np.max(mod_pred)
        if prob>0.8:
            pred = np.argmax(mod_pred)
            #name predicting based on index
            name = classes[pred]
            print(name, '<- with ', round(prob*100, 2), '% probability')
        else: 
            name=''
        
        #draw rectangle on screen
        color = (0, 0, 255) #BGR
        stroke = 2
        end_cord_x = x + w
        end_cord_y = y + h
        cv2.rectangle(frame, (x, y), (end_cord_x, end_cord_y), color, stroke)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, name, (x,y), font, 1, color, stroke, cv2.LINE_AA)

        # # send frame to browser
        # ret, buffer = cv2.imencode('.jpg', frame)
        # frame = buffer.tobytes()

        imgencode = cv2.imencode('.jpg', frame)[1]

        # base64 encode
        stringData = base64.b64encode(imgencode).decode('utf-8')
        b64_src = 'data:image/jpg;base64,'
        stringData = b64_src + stringData

        # emit the frame back
        emit('response_back', stringData)
        
        # yield (b'--frame\r\n'
        #         b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
                   
@app.route('/camera')
def index():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    # app.run(host='0.0.0.0', port=5000)
    socketio.run(app, host='0.0.0.0', port=5000)
