#!/usr/bin/env python
from flask import Flask, flash, redirect, render_template, request, session, abort, render_template_string, Response,request
from camera_pi import Camera
import requests
import wiringpi
import sys, os
app = Flask(__name__)

wiringpi.wiringPiSetupGpio()
wiringpi.pinMode(18, wiringpi.GPIO.PWM_OUTPUT)
wiringpi.pwmSetMode(wiringpi.GPIO.PWM_MODE_MS)
wiringpi.pwmSetClock(192)
wiringpi.pwmSetRange(2000)

URL = sys.argv[1]
password = sys.argv[2]

@app.route('/%s' % URL)
def home():
    if not session.get('logged_in'):
        return render_template('login.html', _url = URL)
    else:
        return render_template('index.html')

@app.route('/%s' % URL, methods=['POST'])
def login():
    if request.form['password'] == password:
        session['logged_in'] = True
    else:
        flash('Password incorrecta!')
    return home()

def rotation_camara(value):
    angle = 60 + value
    wiringpi.pwmWrite(18,angle)

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/def_cerrar', methods=['POST'])
def shutdown():
    rotation_camara(90)
    shutdown_server()
    return 'Server shutting down...'

@app.route('/movimiento_camara_derecha')
def movimiento_camara_derecha():
    rotation_camara(45)
    print "movimiento_camara_derecha"
    return ""

@app.route('/movimiento_camara_izquierda')  
def movimiento_camara_izquierda():
    rotation_camara(135)
    print "movimiento_camara_izquierda"
    return ""

@app.route('/movimiento_camara_centro')  
def movimiento_camara_centro():
    rotation_camara(90)
    print "movimiento_camara_centro"
    return ""

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(host='0.0.0.0', debug=True,port=5000, threaded=True)
