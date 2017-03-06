import sys
sys.path.append('..')
import app
import unittest

try:
    import json
except ImportError:
    import simplejson as json


class ChatbotTestCase(unittest.TestCase):
    def test_chatbot_command(self):
        msg = {"text": "!! h"}
        r = app.bot(msg)
        self.assertEquals(r, 'Sorry, I dont uderstand that command')

class ChatBotTestHelp(unittest.TestCase):
    def test_chatbot_command_hi(self):
        msg = {"text": "!! help"}
        r = app.bot(msg)
        self.assertEquals(r, 'The options are about, help, say: !! say <words to say>, mario, softkitty, yoshi, text: !! text <message>, and kenny')
        
class ChatBotTestSay(unittest.TestCase):
    def test_chatbot_command_say(self):
        msg = {"text": "!! say hi"}
        r = app.bot(msg)
        self.assertEquals(r, 'hi')
        
class ChatBotTestAbout(unittest.TestCase):
    def test_chatbot_command_about(self):
        msg = {"text": "!! about"}
        r = app.bot(msg)
        self.assertEquals(r, 'This is a chat app that was build in CSUMBs software engineering class in two weeks')

class ChatBotTestMario(unittest.TestCase):
    def test_chatbot_command_mario(self):
        msg = {"text": "!! mario"}
        r = app.bot(msg)
        self.assertEquals(r, 'mario')
        
class ChatBotTestYoshi(unittest.TestCase):
    def test_chatbot_command_yoshi(self):
        msg = {"text": "!! yoshi"}
        r = app.bot(msg)
        self.assertEquals(r, 'yoshi')
        
class ChatBotTestKenny(unittest.TestCase):
    def test_chatbot_command_kenny(self):
        msg = {"text": "!! kenny"}
        r = app.bot(msg)
        self.assertEquals(r, 'kenny')

class ChatBotText(unittest.TestCase):
    def test_chatbot_command_text(self):
        msg = {"text": "!! text hi"}
        r = app.bot(msg)
        self.assertEquals(r, 'Text sent')
        
class ChatBotTestMinion(unittest.TestCase):
    def test_chatbot_command_minion(self):
        msg = {"text": "!! kenny"}
        r = app.bot(msg)
        self.assertEquals(r, 'kenny')

class ChatBotObama(unittest.TestCase):
    def test_chatbot_command_obama(self):
        msg = {"text": "!! text hi"}
        r = app.bot(msg)
        self.assertEquals(r, 'Text sent')
    
    # def test_no_bangbang_means_no_command(self):
    #     r = random_functions.get_chatbot_response('hi')
    #     self.assertEquals(r, 'Not a command')

if __name__ == '__main__':
    unittest.main()