import os
from flask import Flask, render_template, request
from flask_socketio import SocketIO
import requests
import random

try:
    import json
except ImportError:
    import simplejson as json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

socket_ids = {}
about = 'This is a chat app that was build in CSUMBs software engineering class in two weeks'
help = 'The options are help, say, spanish, and pic'
dont_recon = 'Sorry, I dont uderstand that command'
@app.route('/')



def hello():
    
    return render_template('index.html')
@socketio.on('connect')
def on_connect():
   print 'Someone connected!------------------------------------'
   
@socketio.on('send:message')
def handle_my_custom_event(data):
    
     socketio.sleep(seconds=0.1)
    
     the_text = json.dumps(data['text'])
     print the_text[1:2]
     socketio.sleep(seconds=0.1)
     
     if request.sid in socket_ids:
        socketio.emit('send:message', data, broadcast=True, include_self=False)
    
@socketio.on('facebook:athenticate', namespace='/')
def test_connect_facebook(data):
    socketio.emit('user:joinFB', {'fb': data}, broadcast=True, include_self=True)
    socketio.emit('user:meFB', {'fb': data}, room=request.sid)
    socket_ids[request.sid] = data['name'];
    
@socketio.on('google:athenticate', namespace='/')
def test_connect_google(data):
    socketio.emit('user:joinG', {'g': data['profileObj']}, broadcast=True, include_self=True)
    socketio.emit('user:meG', {'g': data['profileObj']}, room=request.sid)
    socket_ids[request.sid] = data['profileObj']['name'];

@socketio.on('disconnect', namespace='/')
def test_disconnect():
    socketio.emit('user:left', {'users': socket_ids[request.sid]}, broadcast=True, include_self = True)

socketio.run(
    app,
    host=os.getenv('IP', '0.0.0.0'),
    port=int(os.getenv('PORT', 8080))
)