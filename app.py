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



# @app.route('/')
# def hello():
#   return render_template('index.html')
# @socketio.on('connect')
# def on_connect():
#   print 'Someone connected!------------------------------------'
   
# @socketio.on('send:message')
# def handle_my_custom_event(data):
#     print('received json: ' + json.dumps(data))
#     socketio.send('send:message', data)
   
# @socketio.on('facebook:athenticate', namespace='/')
# def test_connect_facebook(data):
#     socketio.emit('user:joinFB', {'fb': data})

    
# @socketio.on('google:athenticate', namespace='/')
# def test_connect_google(data):
#     socketio.emit('user:joinG', {'g': data['profileObj']}, broadcast=True, include_self = False)


# @socketio.on('disconnect', namespace='/')
# def test_disconnect():
#     socketio.emit('user:left', {'users': 'hi'}, broadcast=True, include_self = False)

clients = []

@app.route('/')
def index():
    return app.send_static_file('index.html')
    
@socketio.on('connected')
def connected():
    print "%s connected" % (request.namespace.socket.sessid)
    clients.append(request.namespace)
    
@socketio.on('disconnect')
def disconnect():
    print "%s disconnected" % (request.namespace.socket.sessid)
    clients.remove(request.namespace)
    
def hello_to_random_client():
    import random
    from datetime import datetime
    if clients:
        k = random.randint(0, len(clients)-1)
        print "Saying hello to %s" % (clients[k].socket.sessid)
        clients[k].emit('message', "Hello at %s" % (datetime.now()))

if __name__ == '__main__':
    import thread, time
    thread.start_new_thread(lambda: socketio.run(app), ())
    
    while True:
        time.sleep(1)
        hello_to_random_client()
# socketio.run(
#     app,
#     host=os.getenv('IP', '0.0.0.0'),
#     port=int(os.getenv('PORT', 8080))
# )