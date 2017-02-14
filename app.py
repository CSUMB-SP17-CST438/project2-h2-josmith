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
def handle_json(json):
    print('received json: ' + json['text'])
    
    
socketio.run(
    app,
    host=os.getenv('IP', '0.0.0.0'),
    port=int(os.getenv('PORT', 8080))
)
