#!/usr/bin/env python3

from flask import Flask, render_template, request, Response
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

# @app.route('/redir')
# def redir():
#     return redirect(url_for('camera'))


@app.route('/camera', methods=['POST'])
def camera():
    pod_ip = request.form['pod_ip']
    return render_template('camera.html', pod_ip=pod_ip)

@app.route('/<pod_ip>/video_feed')
def video_feed(pod_ip):
    # check if ip is valid
    match = re.match(r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$", pod_ip)
    if bool(match) is False:
        print("IP address {} is not valid".format(pod_ip))
        return Response("bad_input", status=401, mimetype='application/json')
    
    res=requests.get('http://' + pod_ip +':5000/camera', stream=True)
    print(res)
    return Response(res.iter_content(chunk_size=10*1024), mimetype='multipart/x-mixed-replace; boundary=frame')

    
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5080)
    
    
#pip install markupsafe==2.0.1
#pip install Werkzeug==2.0.3
