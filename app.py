import os
from flask import Flask, render_template, request
from flask_socketio import SocketIO
from textblob import TextBlob
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
    
     if request.sid in socket_ids:
        text_list = TextBlob(data['text'])
        the_list = text_list.words
        
        if(the_list[0] == '!!'):
           if(the_list[1] == 'about'): 
               socketio.emit('message:bot', about, broadcast=True, include_self=True)
           elif(the_list[1] == 'help'):
               socketio.emit('message:bot', help, broadcast=True, include_self=True)
           elif(the_list[1] == 'say'):
               the_list.pop(0)
               the_list.pop(0)
               the_data = ', '.join(the_list).translate(to='es')
               socketio.emit('message:bot', the_data, broadcast=True, include_self=True)
           elif(the_list[1] == 'spanish'):
               the_list.pop(0)
               the_list.pop(0)
               the_data = ', '.join(the_list).translate(to='es')
               socketio.emit('message:bot', the_data, broadcast=True, include_self=True)
           elif(the_list[1] == 'pic'):
               
               image_url = "https://media.gettyimages.com/photos/-id"

               url_test = 'https://api.gettyimages.com/v3/search/images?fields=id,title,referral_destinations&sort_order=best&phrase=surfing'
               headers = {'Api-Key' : 'hns6ee6gtcnf9frgssyefkyg'}
               r = {'fields' : 'comp'}
               res = requests.get(url_test, headers=headers)
               images_url = res.json()
               rand_num2 = random.randint(0, len(images_url['images']) - 1)
               image_url = images_url['images'][rand_num2]['display_sizes'][0]['uri']
               
               socketio.emit('message:bot', image_url, broadcast=True, include_self=True)
           else:
               socketio.emit('message:bot', dont_recon, broadcast=True, include_self=True)
        else:
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