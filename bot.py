from app import socketio
from testart import mario, softkitty, yoshi, kenny

about = 'This is a chat app that was build in CSUMBs software engineering class in two weeks'
help = 'The options are about, help, say: !! say <words to say>, mario, softkitty, yoshi, and kenny'
dont_recon = 'Sorry, I dont uderstand that command'

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