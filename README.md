# Face recognition system

## celebrity-face-learn-app

A python app for training machine learning model for detecting faces of celebrities and sending calculated model to google drive.

Needed dataset:  
https://www.kaggle.com/datasets/hereisburak/pins-face-recognition

Run app by adding symlink and running docker-compose:  
`ln -sf docker-compose.train.yml docker-compose.yml`  
`docker-compose up`

## face-recogn-app

A python web app for detecting faces which uses cv2 for face detection and model developed in celebrity-face-learn-app.

How to run:

1. Generate model files using celebrity-face-learn-app(or placing them there manually):  
   Model/FaceRecogn.h5 (file with model)  
   Model/classes.txt (file with labels(celebrities names) for indexes extracted from model)

2. Similarly as above run app by adding symlink and running docker-compose:  
   `ln -sf docker-compose.deploy.yml docker-compose.yml`  
   `docker-compose up`
