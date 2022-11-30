#!/usr/bin/env python3

from flask import Flask, render_template, Response
import time
import logging
import requests

#Initialize the Flask app
app = Flask(__name__)

log = logging.getLogger("mylogger")
      
@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/redir')
# def redir():
#     return redirect(url_for('camera'))
    
@app.route('/camera')
def camera():
    return render_template('camera.html')

@app.route('/video_feed')
def video_feed():
    res=requests.get('http://webapp:5000/camera', stream=True)
    print(res)
    return Response(res.iter_content(chunk_size=10*1024), mimetype='multipart/x-mixed-replace; boundary=frame')
    # return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')
    
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5080)
    
    
#pip install markupsafe==2.0.1
#pip install Werkzeug==2.0.3
