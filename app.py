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
   
@socketio.on('facebook:athenticate', namespace='/')
def test_connect_facebook(data):
    socketio.emit('user:joinFB', {'fb': data})
    # global name
    # name = data['name']
    
    # global image
    # image = data['picture']['data']['url']
    
@socketio.on('google:athenticate', namespace='/')
def test_connect_google(data):
    socketio.emit('user:joinG', {'g': data['profileObj']})


@socketio.on('disconnect', namespace='/')
def test_disconnect():
    socketio.emit('user:left', {'users': 'hi'})


socketio.run(
    app,
    host=os.getenv('IP', '0.0.0.0'),
    port=int(os.getenv('PORT', 8080))
)