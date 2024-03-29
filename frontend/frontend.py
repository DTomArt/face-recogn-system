#!/usr/bin/env python3

from flask import Flask, render_template, request, Response, send_file
import time
import logging
import requests
import re

#Initialize the Flask app
app = Flask(__name__)

log = logging.getLogger("mylogger")
      
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/camera', methods=['POST'])
def camera():
    return render_template('camera.html')

@app.route('/video_feed')
def video_feed():
    res=requests.get('http://webapp-svc.face-recogn:5000/camera', stream=True)
    
    if res.status_code == 500:
        return send_file('error.png', mimetype='image/gif')
    
    return Response(res.iter_content(chunk_size=10*1024), mimetype='multipart/x-mixed-replace; boundary=frame')
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5080)
