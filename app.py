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


# Object that represents a socket connection
class Socket:
    def __init__(self, sid):
        self.sid = sid
        self.connected = True

    # Emits data to a socket's unique room
    def emit(self, event, data):
        socketio.emit(event, data, room=self.sid)


socket_ids = {}
@app.route('/')
def hello():
   return render_template('index.html')
@socketio.on('connect')
def on_connect():
   print 'Someone connected!------------------------------------'
   print request.sid
   socket_ids[request.sid] = Socket(request.sid)
   
@socketio.on('send:message')
def handle_my_custom_event(data):
    print('received json: ' + json.dumps(data))
    socketio.emit('send:message', data, broadcast=True, include_self=False)
    print request.sid
    
@socketio.on('facebook:athenticate', namespace='/')
def test_connect_facebook(data):
    socketio.emit('user:joinFB', {'fb': data}, broadcast=True, include_self=False)
    socketio.emit('user:meFB', {'fb': data}, room=request.sid)
    
@socketio.on('google:athenticate', namespace='/')
def test_connect_google(data):
    socketio.emit('user:joinG', {'g': data['profileObj']}, broadcast=True, include_self=False)
    socketio.emit('user:meG', {'g': data['profileObj']}, room=request.sid)
    

# @socketio.on('disconnect', namespace='/')
# def test_disconnect():
#     socketio.emit('user:left', {'users': 'hi'}, broadcast=True, include_self = False)


socketio.run(
    app,
    host=os.getenv('IP', '0.0.0.0'),
    port=int(os.getenv('PORT', 8080))
)