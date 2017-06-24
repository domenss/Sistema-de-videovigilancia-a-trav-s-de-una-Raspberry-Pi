from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort, render_template_string, Response
import os
from camera_pi_streaming import Camera
from PIL import Image
app = Flask(__name__)
WIDTH = 500
HEIGHT = 350


def getImages():
    images = []
    for root, dirs, files in os.walk('/home/pi/flask/static/data'):
        files = sorted(files)
        for name in files:
            if name.endswith('.jpg'):
                im = Image.open('/home/pi/flask/static/data/'+name)
                w, h = im.size
                aspect = 1.0*w/h
                if aspect > 1.0*WIDTH/HEIGHT:
                    width = min(w, WIDTH)
                    height = width/aspect
                else:
                    height = min(h, HEIGHT)
                    width = height*aspect
                images.append({'titulo':name[:name.find('.')] ,'src': name, 'width': int(width), 'height': int(height)})

            elif name.endswith('.mp4'):
                images.append({'titulo':name[:name.find('.')] ,'src': name})
            else:
                pass
    return images
 
@app.route('/')
def home():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('index.html', **{'images': getImages()})

@app.route("/video_stream")
def video_stream():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('stream_video.html') 


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/', methods=['POST'])
def do_admin_login():
    if request.form['password'] == 'admin' and request.form['username'] == 'admin':
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

@app.route('/def_cerrar', methods=['POST'])
def def_cerrar():
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        return home()

 
if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True, host='0.0.0.0', threaded=True)

