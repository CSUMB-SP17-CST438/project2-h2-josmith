import os
from flask import Flask, render_template, request
import requests
import random
import flask_sqlalchemy
from flask import jsonify
from ast import literal_eval
from sqlalchemy.orm import load_only
from flask_socketio import SocketIO
from testart import mario, softkitty, yoshi, kenny, minion, obama
import middleware

# for twilio
account_sid = "ACf8a0a19a076e5b5cfb46bcb1a2800a02"
auth_token = "8fcaaf3a59fc15c79a156f55db92d38a"

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
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://smitjb45:Goldfish83-@localhost/postgres'
db = flask_sqlalchemy.SQLAlchemy(app)


import models

socket_ids = {}
@app.route('/')

def hello():
    
    return render_template('index.html')

@socketio.on('new message')
def on_new_message(data):
    socketio.emit('got your message', {
        'your message': data['my message']
})
@socketio.on('connect')
def on_connect():
#   print 'Someone connected!------------------------------------'
  try:
      #print the past messages
      messages = models.Message.query.order_by(models.Message.id.desc()).limit(10).from_self().order_by(models.Message.id.asc())
      new = json.loads(str(messages[0]))
      
      for message in messages:
          new = json.loads(str(message))
          socketio.sleep(seconds=0.2)
          socketio.emit('send:message', new, room=request.sid)
        #   print new
          
          the_text = str(new['text'])
          if(the_text[0:2] == '!!'):
             response = bot(new)
             if(response == "mario"):
                 response = mario
             elif(response == "softkitty"):
                 response = softkitty
             elif(response == "yoshi"):
                 response = yoshi
             elif(response == "kenny"):
                 response = kenny
             elif(response == "minion"):
                 response = minion
             elif(response == "obama"):
                 response = obama
             socketio.emit('bot:message', response, broadcast=True, include_self=True)
          
  except ImportError:
    print "error im in the connect method"
       
@socketio.on('send:message')
def handle_my_custom_event(data):
     
     if request.sid in socket_ids:
         socketio.sleep(seconds=0.1)
         massage = models.Message(json.dumps(data, ensure_ascii=False))
        #  models.db.session.add(massage)
        #  models.db.session.commit()
         
         socketio.sleep(seconds=0.1)
         socketio.emit('send:message', data, broadcast=True, include_self=False)
         the_text = str(data['text'])
         if(the_text[0:2] == '!!'):
             response = bot(data)
             if(response == "mario"):
                 response = mario
             elif(response == "softkitty"):
                 response = softkitty
             elif(response == "yoshi"):
                 response = yoshi
             elif(response == "kenny"):
                 response = kenny
             elif(response == "minion"):
                 response = minion
             elif(response == "obama"):
                 response = obama
             socketio.emit('bot:message', response, broadcast=True, include_self=True)
    
@socketio.on('facebook:athenticate', namespace='/')
def test_connect_facebook(data):
    # print data
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
    #  print json.dumps(data)
     the_text = str(data['text'])
     if(the_text[0:2] == '!!'):
        if( the_text[3:len(the_text)] == "about"):
            return 'This is a chat app that was build in CSUMBs software engineering class in two weeks'
        elif( the_text[3:len(the_text)] == "help"):
            return 'The options are about, help, say: !! say <words to say>, mario, softkitty, yoshi, text: !! text <message>, and kenny'
        elif( the_text[3:6] == "say"):
            return the_text[7:len(the_text)]
        elif( the_text[3:len(the_text)] == "mario"):
            return "mario"
        elif( the_text[3:len(the_text)] == "softkitty"):
            return "softkitty"
        elif( the_text[3:len(the_text)] == "yoshi"):
            return "yoshi"
        elif( the_text[3:len(the_text)] == "kenny"):
            return "kenny"
        elif( the_text[3:len(the_text)] == "minion"):
            return "minion"
        elif( the_text[3:len(the_text)] == "obama"):
            return "obama"
        elif( the_text[3:7] == "text"):
            client = middleware.TwilioRestClient(account_sid,auth_token)
            message = client.messages.create(to="+18314285108", from_="+18312010628",
                                     body=the_text[8:len(the_text)])
            return "Text sent"
        else:
         return 'Sorry, I dont uderstand that command'

if __name__ == '__main__':
    print db
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080))
    )