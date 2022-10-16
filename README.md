## Face recognition system

# celebrity-face-learn-app

A python app for training machine learning model for detecting faces of celebrities.

Needed dataset:
https://www.kaggle.com/datasets/hereisburak/pins-face-recognition

can be downloaded with:
kaggle datasets download -d hereisburak/pins-face-recognition

Run app by running:
cd celebrity-face-learn-app
docker-compose up

# face-recogn-app

A python web app for detecting faces which uses cv2 for face detection and model developed in celebrity-face-learn-app.

How to run:

1. Generate model files using celebrity-face-learn-app(or placing them there manually):
   celebrity-face-learn-app/Model/FaceRecogn.h5 (file with model)
   celebrity-face-learn-app/Model/classes.txt (file with labels(celebrities names) for indexes extracted from model)

2. Run file:
   cd face-recogn-app && ./face-recogn-app.py
