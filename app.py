import os
import flask, flask_socketio

try:
    import json
except ImportError:
    import simplejson as json

app = flask.Flask(__name__)

socketio = flask_socketio.SocketIO(app)

@app.route('/')
def hello():
   return flask.render_template('index.html')
   
@socketio.on('connect')
def on_connect():
   print 'Someone connected!------------------------------------'
   
@socketio.on('send:message')
def handle_my_custom_event(data):
    print('received json: ' + json.dumps(data))
    socketio.emit('send:message', data, broadcast=True, include_self = False)
   
@socketio.on('connect', namespace='/')
def test_connect():
    socketio.emit('user:join', {'users': 'Sammy CAT'})

@socketio.on('disconnect', namespace='/')
def test_disconnect():
    socketio.emit('user:left', {'users': 'Sammy Cat'})

socketio.run(
    app,
    host=os.getenv('IP', '0.0.0.0'),
    port=int(os.getenv('PORT', 8080))
)
