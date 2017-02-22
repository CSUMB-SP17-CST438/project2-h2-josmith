# -*- coding: utf-8 -*-

import os
from flask import Flask, render_template, request
from flask_socketio import SocketIO
import requests
import random
import flask_sqlalchemy
from flask import jsonify
from ast import literal_eval
from sqlalchemy.orm import load_only
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
about = 'This is a chat app that was build in CSUMBs software engineering class in two weeks'
help = 'The options are about, help, say: !! say <words to say>, mario, softkitty, yoshi, and kenny'
dont_recon = 'Sorry, I dont uderstand that command'
mario = """
__________________▄▄▄▀▀▀▀▀▀▀▄
_______________▄▀▀____▀▀▀▀▄____█
___________▄▀▀__▀▀▀▀▀▀▄___▀▄___█
__________█▄▄▄▄▄▄_______▀▄__▀▄__█
_________█_________▀▄______█____█_█
______▄█_____________▀▄_____▐___▐_▌
______██_______________▀▄___▐_▄▀▀▀▄
______█________██_______▌__▐▄▀______█
______█_________█_______▌__▐▐________▐
_____▐__________▌_____▄▀▀▀__▌_______▐_____________▄▄▄▄▄▄
______▌__________▀▀▀▀________▀▀▄▄▄▀______▄▄████▓▓▓▓▓▓▓███▄
______▌____________________________▄▀__▄▄█▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▄
______▐__________________________▄▀_▄█▓▓▓▓▓▓▓▓▓▓_____▓▓____▓▓█▄
_______▌______________________▄▀_▄█▓▓▓▓▓▓▓▓▓▓▓____▓▓_▓▓_▓▓__▓▓█
_____▄▀▄_________________▄▀▀▌██▓▓▓▓▓▓▓▓▓▓▓▓▓__▓▓▓___▓▓_▓▓__▓▓█
____▌____▀▀▀▄▄▄▄▄▄▄▄▀▀___▌█▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓__▓________▓▓___▓▓▓█
_____▀▄_________________▄▀▀▓▓▓▓▓▓▓▓█████████████▄▄_____▓▓__▓▓▓█
_______█▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓█▓▓▓▓▓██▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓██▄▄___▓▓▓▓▓█
_______█▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓█▓▓███▓▓▓▓████▓▓▓▓▓▓▓▓▓▓▓▓▓██▓▓▓▓▓▓█
________█▓▓▓▓▓▓▓▓▓▓▓▓▓▓█▓█▓▓██░░███████░██▓▓▓▓▓▓▓▓▓▓██▓▓▓▓▓█
________█▓▓▓▓▓▓▓▓▓▓▓▓▓▓██▓░░░░░█░░░░░██░░░░██▓▓▓▓▓▓▓▓▓██▓▓▓▓▌
________█▓▓▓▓▓▓▓▓▓▓▓▓▓▓███░░░░░░░░____░██░░░░░░░██▓▓▓▓▓▓▓██▓▓▌
________▐▓▓▓▓▓▓▓▓▓▓▓▓▓▓██░░░░░░░________░░░░░░░░░██████▓▓▓▓▓█▓▌
________▐▓▓▓▓▓▓▓▓▓▓▓▓▓▓██░░░░░░___▓▓▓▓▓░░░░░░░███░░███▓▓▓▓▓█▓▌
_________█▓▓▓▓▓▓▓▓▓▓▓▓▓██░░░░░___▓▓█▄▄▓░░░░░░░░___░░░░█▓▓▓▓▓█▓▌
_________█▓▓▓▓▓▓▓▓▓▓▓▓▓█░░█░░░___▓▓██░░░░░░░░▓▓▓▓__░░░░█▓▓▓▓██
_________█▓▓▓▓▓▓▓▓▓▓▓▓▓█░███░░____▓░░░░░░░░░░░█▄█▓__░░░░█▓▓█▓█
_________▐▓▓▓▓▓▓▓▓▓▓▓▓▓█░█████░░░░░░░░░░░░░░░░░█▓__░░░░███▓█
__________█▓▓▓▓▓▓▓▓▓▓▓▓█░░███████░░░░░░░░░░░░░░░▓_░░░░░██▓█
__________█▓▓▓▓▓▓▓▓▓▓▓▓█░░░███████░░░░░░░░░░░░░░_░░░░░██▓█
__________█▓▓▓▓▓▓▓▓▓▓▓▓█░░░███████░░░░░░░░░░░░░░░░░░░██▓█
___________█▓▓▓▓▓▓▓▓▓▓▓▓█░░░░███████░░░░░░░░░░░█████░██░
___________█▓▓▓▓▓▓▓▓▓▓▓▓█░░░░░░__███████░░░░░███████░░█░░
___________█▓▓▓▓▓▓▓▓▓▓▓▓▓█░░░░░░█▄▄▄▀▀▀▀████████████░░█░
___________▐▓▓▓▓▓▓▓▓▓▓▓▓█░░░░░░██████▄__▀▀░░░███░░░░░█
___________▐▓▓▓▓▓▓▓▓▓▓▓█▒█░░░░░░▓▓▓▓▓███▄░░░░░░░░░░░____________▄▄▄
___________█▓▓▓▓▓▓▓▓▓█▒▒▒▒█░░░░░░▓▓▓▓▓█░░░░░░░░░░░______▄▄▄_▄▀▀____▀▄
__________█▓▓▓▓▓▓▓▓▓█▒▒▒▒█▓▓░░░░░░░░░░░░░░░░░░░░░____▄▀____▀▄_________▀▄
_________█▓▓▓▓▓▓▓▓▓█▒▒▒▒█▓▓▓▓░░░░░░░░░░░░░░░░░______▐▄________█▄▄▀▀▀▄__█
________█▓▓▓▓▓▓▓▓█▒▒▒▒▒▒█▓▓▓▓▓▓▓░░░░░░░░░____________█_█______▐_________▀▄▌
_______█▓▓▓▓▓▓▓▓█▒▒▒▒▒▒███▓▓▓▓▓▓▓▓▓▓▓█▒▒▄___________█__▀▄____█____▄▄▄____▐
______█▓▓▓▓▓▓▓█_______▒▒█▒▒██▓▓▓▓▓▓▓▓▓▓█▒▒▒▄_________█____▀▀█▀▄▀▀▀___▀▀▄▄▐
_____█▓▓▓▓▓██▒_________▒█▒▒▒▒▒███▓▓▓▓▓▓█▒▒▒██________▐_______▀█_____________█
____█▓▓████▒█▒_________▒█▒▒▒▒▒▒▒▒███████▒▒▒▒██_______█_______▐______▄▄▄_____█
__█▒██▒▒▒▒▒▒█▒▒____▒▒▒█▒▒▒▒▒▒▒▒▒▒▒▒▒▒█▒____▒█▓█__▄█__█______▀▄▄▀▀____▀▀▄▄█
__█▒▒▒▒▒▒▒▒▒▒█▒▒▒████▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█_______█▓▓█▓▓▌_▐________▐____________▐
__█▒▒▒▒▒▒▒▒▒▒▒███▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█▒_______█▓▓▓█▓▌__▌_______▐_____▄▄____▐
_█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█▒▒_____█▓▓▓█▓▓▌__▌_______▀▄▄▀______▐
_█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒███████▓▓█▓▓▓▌__▀▄_______________▄▀
_█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒███▒▒▒▒▒▒▒██▓▓▓▓▓▌___▀▄_________▄▀▀
█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██▒▒▒▒▒▒▒▒▒▒▒▒▒█▓▓▓▓▓▀▄__▀▄▄█▀▀▀
█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██▓▓▓▓██▄▄▄▀
█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒████
█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█
_█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█▒▒▒█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█▄▄▄▄▄
_█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█▒▒▒▒█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒███▒▒▒▒▒▒██▄▄
__█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█▒▒▒▒█▒▒▒▒▒▒▒▒▒▒▒▒███▒▒▒▒▒▒▒▒▒▒▒▒▒█▄
__█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█▒▒▒▒█▒▒▒▒▒▒▒▒▒▒▒█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█
__█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█▒▒▒▒█▒▒▒▒▒▒▒▒▒██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█
___█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█▒▒▒▒█▒▒▒▒▒▒▒▒█▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░▒▒▒▒▒▒▌
____█▒▒▒▒▒▒▒▒▒▒▒▒▒██▒▒▒▒▒▒▒█▒▒▒▒█▒▒▒▒▒▒█▒▒▒▒▒▒▒▒▒░░░░░░░░░░░░░▒▒▌
____█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█████████████▒▒▒▒▒█▒▒▒▒▒▒▒▒░░░░▒▒▒▒▒▒▒▒▒▒▒░▒▌
_____█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█_______▐▒▒▒▒█▒▒▒▒▒▒▒░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░▌
______█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█________█▒▒█▒▒▒▒▒▒░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▌
_______█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█________█▒█▒▒▒▒▒▒░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▌
________█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█________█▒▒▒▒▒▒░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█
_________█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█________█▒▒▒▒░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█
_________█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█________█▒▒▒░░░░░░░▒▒▒▒▒▒▒▒▒▒▒▒▒▒█▀
__________█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█_______█▒░░░▒▒▒▒▒░░░░░░░░▒▒▒█▀▀▀
___________█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█_______█░▒▒▒▒▒▒▒▒▒▒▒▒▒░░░░█▀
____________█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█_______█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█▀
_____________█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█_______█▒▒▒▒▒▒▒▒▒▒▒▒█▀
_____________█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█_______▀▀▀███████▀▀
______________█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█
_______________█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█
________________█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█
_________________█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█
__________________█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒██▒█
___________________█▒▒▒▒▒▒▒▒▒▒▒▒▒██▒▒▒▒█
___________________█▒▒▒▒▒▒▒▒████▒▒▒▒▒▒▒█
___________________█████████▒▒▒▒▒▒▒▒▒▒▒█
____________________█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█
____________________█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█
_____________________█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░▌
_____________________█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░▌
______________________█▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░▌
_______________________█▒▒▒▒▒▒▒▒▒▒▒▒▒▒░░█
________________________█▒▒▒▒▒▒▒▒▒▒▒░░░█
__________________________██▒▒▒▒▒▒░░░█▀
_____________________________█░░░░░█▀
_______________________________▀▀▀▀


"""


softkitty = """
───────────────────────────────────────
───▐▀▄───────▄▀▌───▄▄▄▄▄▄▄─────────────
───▌▒▒▀▄▄▄▄▄▀▒▒▐▄▀▀▒██▒██▒▀▀▄──────────
──▐▒▒▒▒▀▒▀▒▀▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▀▄────────
──▌▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▄▒▒▒▒▒▒▒▒▒▒▒▒▀▄──────
▀█▒▒▒█▌▒▒█▒▒▐█▒▒▒▀▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▌─────
▀▌▒▒▒▒▒▒▀▒▀▒▒▒▒▒▒▀▀▒▒▒▒▒▒▒▒▒▒▒▒▒▒▐───▄▄
▐▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▌▄█▒█
▐▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒���▒▒▒▒▒▒▒▒▒▒▒▒█▒█▀─
▐▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒█▀───
▐▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▌────
─▌▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▐─────
─▐▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▌─────
──▌▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▐──────
──▐▄▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▄▌──────
────▀▄▄▀▀▀▀▀▄▄▀▀▀▀▀▀▀▄▄▀▀▀▀▀▄▄▀────────
"""

yoshi= """
───────────────────────────────
───────────────████─███────────
──────────────██▒▒▒█▒▒▒█───────
─────────────██▒────────█──────
─────────██████──██─██──█──────
────────██████───██─██──█──────
────────██▒▒▒█──────────███────
────────██▒▒▒▒▒▒───▒──██████───
───────██▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒▒███─
──────██▒▒▒▒─────▒▒▒▒▒▒▒▒▒▒▒▒█─
──────██▒▒▒───────▒▒▒▒▒▒▒█▒█▒██
───────██▒▒───────▒▒▒▒▒▒▒▒▒▒▒▒█
────────██▒▒─────█▒▒▒▒▒▒▒▒▒▒▒▒█
────────███▒▒───██▒▒▒▒▒▒▒▒▒▒▒▒█
─────────███▒▒───█▒▒���▒▒▒▒▒▒▒▒█─
────────██▀█▒▒────█▒▒▒▒▒▒▒▒██──
──────██▀██▒▒▒────█████████────
────██▀███▒▒▒▒────█▒▒██────────
█████████▒▒▒▒▒█───██──██───────
█▒▒▒▒▒▒█▒▒▒▒▒█────████▒▒█──────
█▒▒▒▒▒▒█▒▒▒▒▒▒█───███▒▒▒█──────
█▒▒▒▒▒▒█▒▒▒▒▒█────█▒▒▒▒▒█──────
██▒▒▒▒▒█▒▒▒▒▒▒█───█▒▒▒███──────
─██▒▒▒▒███████───██████────────
──██▒▒▒▒▒██─────██─────────────
───██▒▒▒██─────██──────────────
────█████─────███──────────────
────█████▄───█████▄────────────
──▄█▓▓▓▓▓█▄─█▓▓▓▓▓█▄───────────
──█▓▓▓▓▓▓▓▓██▓▓▓▓▓▓▓█──────────
──█▓▓▓▓▓▓▓▓██▓▓▓▓▓▓▓█──────────
──▀████████▀▀███████▀──────────


"""

kenny = """
___________________1111111111111__________________
______________1¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶1_____________
___________1¶¶¶¶¶¶111111111111111¶¶¶¶¶¶1__________
_________1¶¶¶11111111111111111111111¶1¶¶¶1________
_______1¶¶¶¶1111111111111111111111111111¶¶¶1______
______1¶¶1¶1111111111¶¶¶¶¶¶¶¶1111111111111¶¶1_____
_____¶¶¶11111111¶¶¶¶¶¶¶¶1_¶¶¶¶¶¶¶¶111111111¶¶¶____
____¶¶¶1111111¶¶¶¶¶¶¶¶1_____¶¶¶¶¶¶¶¶11111111¶¶¶___
___1¶¶111111¶¶¶¶¶¶¶¶1_________¶¶¶¶¶¶¶¶1111111¶¶1__
___¶¶11111¶¶¶¶¶¶¶¶1____________1¶¶¶¶¶¶¶¶111111¶¶1_
__¶¶11111¶¶¶¶¶¶¶¶¶¶¶¶¶_____¶¶¶¶¶1¶¶¶¶¶¶¶¶111111¶¶_
__¶¶1111¶¶¶¶¶¶¶¶_____¶¶¶¶_¶¶_____1¶¶¶¶¶¶¶¶11111¶¶_
__¶¶1111¶¶¶¶¶¶¶1________¶¶________¶¶¶¶¶¶1¶¶1111¶¶_
__¶1111¶¶¶¶¶¶¶¶_______¶¶_¶_¶¶______¶¶¶¶¶¶1¶11111¶_
__¶¶111¶1¶¶¶¶¶¶_______¶¶_¶_¶¶______¶¶¶¶¶¶1¶11111¶_
__¶1111¶¶1¶¶¶¶¶¶________¶¶¶_______1¶¶¶¶¶11¶11111¶_
__¶¶111¶¶1¶¶¶¶¶¶1_____¶¶¶_¶¶______¶¶¶¶¶¶1¶¶1111¶¶_
__1¶¶111¶11¶¶¶¶¶¶¶¶¶¶¶¶_____¶¶¶¶_¶¶¶¶¶¶11¶1111¶¶1_
___¶¶¶11¶¶11¶¶¶¶¶¶¶1___________¶¶¶¶¶¶¶11¶¶111¶¶¶__
___1¶¶111¶¶111¶¶¶¶¶¶¶________1¶¶¶¶¶¶111¶¶1111¶¶1__
____1¶¶1111¶¶111¶¶¶¶¶¶¶1___¶¶¶¶¶¶¶111¶¶¶1111¶¶1___
_____1¶¶¶111¶¶¶11111¶¶¶¶¶¶¶¶¶¶11111¶¶¶11111¶¶1____
______1¶¶¶1111¶¶¶¶¶1111¶¶¶11111¶¶¶¶¶11111¶¶¶1_____
________1¶¶111111¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶1111111¶¶1_______
__________¶¶1111111111¶¶¶¶1111111111111¶1_________
__________¶¶¶11111111¶¶11¶¶11111111111¶¶¶_________
________1¶¶11¶1¶¶111111111¶111111¶¶¶¶¶11¶¶________
_______1¶¶111111¶¶¶¶¶1¶1¶¶¶¶¶¶¶¶¶¶1111111¶¶_______
_______¶¶¶11111111111111¶¶11¶1111111111111¶¶______
______1¶1111¶11111111111¶¶11111111111111111¶1_____
______¶¶111¶111111111111¶¶1111111111111¶111¶¶_____
_____1¶111¶¶111111111111¶¶1111111111111¶1111¶1____
_____¶¶¶¶¶¶¶111111111111¶¶1111111111111¶¶¶¶¶¶¶____
____¶¶¶¶¶¶¶¶¶11111111111¶¶111111111111¶¶¶¶¶¶¶¶¶___
____¶¶¶¶¶¶¶¶¶11111111111¶¶111111111111¶¶¶¶¶¶¶¶¶___
____1¶¶¶¶¶¶1111111111111¶¶11111111111111¶¶¶¶¶¶1___
______1111¶1111111111111¶¶11111111111111¶1111_____
__________¶¶¶11111111111¶¶111111111111¶¶¶_________
__________¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶_________
________1¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶1¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶¶1_______

"""
@app.route('/')

def hello():
    
    return render_template('index.html')
@socketio.on('connect')
def on_connect():
  print 'Someone connected!------------------------------------'
  try:
      #print the past messsages
      messages = models.Message.query.all()
      new = json.loads(str(messages[0]))
      for message in messages:
          new = json.loads(str(message))
          socketio.sleep(seconds=0.2)
          socketio.emit('send:message', new, room=request.sid)
          socketio.sleep(seconds=0.2)
          
          
          the_text = str(new['text'])
          if(the_text[0:2] == '!!'):
             if( the_text[3:len(the_text)] == "about"):
                 socketio.sleep(seconds=0.1)
                 socketio.emit('bot:message', about, broadcast=True, include_self=True)
             elif( the_text[3:len(the_text)] == "help"):
                 socketio.sleep(seconds=0.1)
                 socketio.emit('bot:message', help, broadcast=True, include_self=True)
             elif( the_text[3:6] == "say"):
                 socketio.sleep(seconds=0.1)
                 socketio.emit('bot:message', the_text[7:len(the_text) -1], broadcast=True, include_self=True)
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
          
  except ImportError:
    print "error im in the connect method"
       
@socketio.on('send:message')
def handle_my_custom_event(data):
     
     socketio.sleep(seconds=0.1)
     massage = models.Message(json.dumps(data, ensure_ascii=False))
     models.db.session.add(massage)
     models.db.session.commit()
     
     if request.sid in socket_ids:
         socketio.sleep(seconds=0.1)
         socketio.emit('send:message', data, broadcast=True, include_self=False)
     
     the_text = json.dumps(data['text'], ensure_ascii=False)
     
     if(the_text[1:3] == '!!'):
         if( the_text[4:len(the_text) -1] == "about"):
             socketio.sleep(seconds=0.1)
             socketio.emit('bot:message', about, broadcast=True, include_self=True)
         elif( the_text[4:len(the_text) -1] == "help"):
             socketio.sleep(seconds=0.1)
             socketio.emit('bot:message', help, broadcast=True, include_self=True)
         elif( the_text[4:7] == "say"):
             socketio.sleep(seconds=0.1)
             socketio.emit('bot:message', the_text[7:len(the_text) -1], broadcast=True, include_self=True)
         elif( the_text[4:len(the_text) -1] == "mario"):
             socketio.sleep(seconds=0.1)
             socketio.emit('bot:message', mario, broadcast=True, include_self=True)
         elif( the_text[4:len(the_text) -1] == "softkitty"):
             socketio.sleep(seconds=0.1)
             socketio.emit('bot:message', softkitty, broadcast=True, include_self=True)
         elif( the_text[4:len(the_text) -1] == "yoshi"):
             socketio.sleep(seconds=0.1)
             socketio.emit('bot:message', yoshi, broadcast=True, include_self=True)
         elif( the_text[4:len(the_text) -1] == "kenny"):
             socketio.sleep(seconds=0.1)
             socketio.emit('bot:message', kenny, broadcast=True, include_self=True)
         else:
             socketio.sleep(seconds=0.1)
             socketio.emit('bot:message', dont_recon, broadcast=True, include_self=True)

    
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

if __name__ == '__main__':
    print db
    socketio.run(
        app,
        host=os.getenv('IP', '0.0.0.0'),
        port=int(os.getenv('PORT', 8080))
    )