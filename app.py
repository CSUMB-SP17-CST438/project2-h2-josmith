import os
from flask import Flask, render_template, request
import requests
import random
import flask_sqlalchemy
from flask import jsonify
from ast import literal_eval
from sqlalchemy.orm import load_only
from flask_socketio import SocketIO
from testart import mario, softkitty, yoshi, kenny

try:
    import json
except ImportError:
    import simplejson as json

app = Flask(__name__)

# socket io stuff
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# database stuff

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://smitjb45:Goldfish83-@localhost/postgres'
db = flask_sqlalchemy.SQLAlchemy(app)

about = 'This is a chat app that was build in CSUMBs software engineering class in two weeks'
help = 'The options are about, help, say: !! say <words to say>, mario, softkitty, yoshi, and kenny'
dont_recon = 'Sorry, I dont uderstand that command'

import models

socket_ids = {}
@app.route('/')

def hello():
    
    return render_template('index.html')
@socketio.on('connect')
def on_connect():
  print 'Someone connected!------------------------------------'
  try:
      #print the past messsages
    #   messages = models.Message.query.order_by(models.Message.id.desc()).limit(15).from_self().order_by(models.Message.id.asc())
      messages = models.Message.query.all()
      new = json.loads(str(messages[0]))
      for message in messages:
          new = json.loads(str(message))
          socketio.sleep(seconds=0.2)
          socketio.emit('send:message', new, room=request.sid)
          socketio.sleep(seconds=0.2)
          bot(new)
          
  except ImportError:
    print "error im in the connect method"
       
@socketio.on('send:message')
def handle_my_custom_event(data):
     
     socketio.sleep(seconds=0.1)
    #  massage = models.Message(json.dumps(data, ensure_ascii=False))
    #  models.db.session.add(massage)
    #  models.db.session.commit()
     
     if request.sid in socket_ids:
         socketio.sleep(seconds=0.1)
         socketio.emit('send:message', data, broadcast=True, include_self=False)
         bot(data)
    
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
    
    if request.sid in socket_ids:
         socketio.sleep(seconds=0.1)
         socketio.emit('user:left', {'users': socket_ids[request.sid]}, broadcast=True, include_self = True)
         
def bot(data):
     the_text = str(data['text'])
          
     if(the_text[0:2] == '!!'):
        if( the_text[3:len(the_text)] == "about"):
            socketio.sleep(seconds=0.1)
            socketio.emit('bot:message', about, broadcast=True, include_self=True)
        elif( the_text[3:len(the_text)] == "help"):
            socketio.sleep(seconds=0.1)
            socketio.emit('bot:message', help, broadcast=True, include_self=True)
        elif( the_text[3:6] == "say"):
            socketio.sleep(seconds=0.1)
            socketio.emit('bot:message', the_text[7:len(the_text)], broadcast=True, include_self=True)
        elif( the_text[3:len(the_text)] == "mario"):
            socketio.sleep(seconds=0.1)
            socketio.emit('bot:message', mario, broadcast=True, include_self=True)
        elif( the_text[3:len(the_text)] == "softkitty"):
            socketio.sleep(seconds=0.1)
            socketio.emit('bot:message', softkitty, broadcast=True, include_self=True)
        elif( the_text[3:len(the_text)] == "yoshi"):
            socketio.sleep(seconds=0.1)
            socketio.emit('bot:message', yoshi, broadcast=True, include_self=True)
        elif( the_text[3:len(the_text)] == "kenny"):
            socketio.sleep(seconds=0.1)
            socketio.emit('bot:message', kenny, broadcast=True, include_self=True)
        else:
         socketio.sleep(seconds=0.1)
         socketio.emit('bot:message', dont_recon, broadcast=True, include_self=True)

if __name__ == '__main__':
    print db
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080))
    )