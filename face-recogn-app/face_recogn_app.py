#!/usr/bin/env python3

from flask import Flask, render_template, Response, send_file
import cv2
from keras import models
import numpy as np
from keras.applications.inception_resnet_v2 import preprocess_input
import time
import logging

import os
import camera_pb2
import camera_pb2_grpc
import grpc
import traceback
import tensorflow as tf
import time

#Initialize the Flask app
app = Flask(__name__)

device = tf.config.list_physical_devices('GPU')
if len(device) > 0:
   tf.config.experimental.set_memory_growth(device[0],True)
   tf.config.experimental.set_virtual_device_configuration(device[0],
     [tf.config.experimental.VirtualDeviceConfiguration(memory_limit=512)])

model = models.load_model("./Model/mdl1")

classes = np.genfromtxt("./Model/classes_mdl1.txt", dtype='str', delimiter='\n')
print('\nClasses detected:\n', classes)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

camera_url = "{0}:80".format(os.environ['CAMERA_SOURCE_SVC'])
print('Connecting to camera with ip: ', camera_url)
log = logging.getLogger("mylogger")

# err_png = cv2.VideoCapture('./error.png')

def gen_frames():  
    retries=0
    while True:
        # Loops, creating gRPC client and grabing frame from camera serving specified url.
        client_channel = grpc.insecure_channel(camera_url, options=(('grpc.use_local_subchannel_pool', 1),))
        camera_stub = camera_pb2_grpc.CameraStub(client_channel)
        
        # try:
        frame = camera_stub.GetFrame(camera_pb2.NotifyRequest())
        frame = frame.frame
        client_channel.close()
        # except grpc.RpcError as e:
        #     log.error(e)
        #     return e, 400
        #     time.sleep(10)
        #     continue

        time.sleep(0.05)

        # encode frame to CV2 type
        nparr = np.fromstring(frame, np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        #start detection
        # start_time = time.time()
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

        # #measure time of detection
        # end_time = time.time()
        # time_of_detection=end_time - start_time
        # print(time_of_detection)

# send frame to browser
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
                   
@app.route('/camera')
def index():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
