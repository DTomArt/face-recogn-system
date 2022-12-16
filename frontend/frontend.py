#!/usr/bin/env python3

from flask import Flask, render_template, request, Response, send_file
import time
import logging
import requests
import re

import imageio

#Initialize the Flask app
app = Flask(__name__)

log = logging.getLogger("mylogger")
      
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/camera', methods=['POST'])
def camera():
    pod_ip = request.form['pod_ip']
    return render_template('camera.html', pod_ip=pod_ip)

@app.route('/<pod_ip>/video_feed')
def video_feed(pod_ip):
    # check if ip is valid
    # match = re.match(r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?):(6553[0-5]|655[0-2][0-9]|65[0-4][0-9][0-9]|6[0-4][0-9][0-9][0-9][0-9]|[1-5](\d){4}|[1-9](\d){0,3})$", pod_ip)
    # if bool(match) is False:
    #     print("IP address {} is not valid".format(pod_ip))
    #     return Response("bad_input", status=401, mimetype='application/json')

    res=requests.get('http://webapp-svc.default:5000/camera', stream=True)

    if not res:
        err=imageio.imread('error.png')
        return send_file(err, mimetype='image/gif')

    return Response(res.iter_content(chunk_size=10*1024), mimetype='multipart/x-mixed-replace; boundary=frame')

    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5080)

