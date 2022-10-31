#!/usr/bin/env python3

from flask import Flask, render_template, Response
import cv2
from keras import models
import numpy as np
from keras.applications.inception_resnet_v2 import preprocess_input

#Initialize the Flask app
app = Flask(__name__)

#Load model
model = models.load_model('../Model/FaceRecogn.h5')
classes = np.genfromtxt('../Model/classes.txt', dtype='str', delimiter='\n')
print('\nClasses detected:\n', classes)

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

camera = cv2.VideoCapture(0)

def gen_frames():  
    while True:
        success, frame = camera.read()  # read the camera frame
        if not success:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=8, minSize=(50,50))
        for (x, y, w, h) in faces:
            #print('Person detected!',x, y, w, h)
            incr_by=20 #in px
            if y>incr_by: y-=incr_by
            if x>incr_by: x-=incr_by
            if h>incr_by: h+=incr_by
            if w>incr_by: w+=incr_by

            roi_color = frame[y:y+h, x:x+w, :]
            # roi_gray = gray[y:y+h, x:x+w]   #region of interest
            # cv2.imwrite(img_item, roi_gray)
            
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
        
        # send frame to browser
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
                   
@app.route('/')
def index():
    return render_template('index.html')
    
@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    
if __name__ == "__main__":
    app.run()
    
    
#pip install markupsafe==2.0.1
#pip install Werkzeug==2.0.3
