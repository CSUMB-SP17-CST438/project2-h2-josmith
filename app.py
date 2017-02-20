import os
from flask import Flask, render_template, request
from flask_socketio import SocketIO

try:
    import json
except ImportError:
    import simplejson as json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

socket_ids = {}
@app.route('/')
def hello():
   return render_template('index.html')
@socketio.on('connect')
def on_connect():
   print 'Someone connected!------------------------------------'
   
@socketio.on('send:message')
def handle_my_custom_event(data):
    print('received json: ' + json.dumps(data))
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