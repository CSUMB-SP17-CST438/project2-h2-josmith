import os
from flask import Flask, render_template, request
from flask_socketio import SocketIO
from StringIO import StringIO
import requests
import random
from textblob import TextBlob

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
     
     if request.sid in socket_ids:
         socketio.emit('send:message', data, broadcast=True, include_self=False)
     
     the_text = json.dumps(data['text'], ensure_ascii=True)
     print the_text[4:10]
     if(the_text[1:3] == '!!'):
         if( the_text[4:len(the_text) -1] == "about"):
             socketio.sleep(seconds=0.1)
             socketio.emit('bot:message', about, broadcast=True, include_self=True)
         elif( the_text[4:len(the_text) -1] == "help"):
             socketio.sleep(seconds=0.1)
             socketio.emit('bot:message', help, broadcast=True, include_self=True)
         elif( the_text[4:10] == "spanish"):
             en_blob = TextBlob(the_text[4:len(the_text) -1])
             socketio.sleep(seconds=0.1)
             socketio.emit('bot:message', en_blob.translate(to='es'), broadcast=True, include_self=True)
         else:
             socketio.sleep(seconds=0.1)
             socketio.emit('bot:message', dont_recon, broadcast=True, include_self=True)

    
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