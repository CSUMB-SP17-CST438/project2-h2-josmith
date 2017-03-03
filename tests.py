# tests.py
# import random_functions
import app
import unittest

try:
    import json
except ImportError:
    import simplejson as json


class ChatbotTestCase(unittest.TestCase):
    def test_bangbang_means_command(self):
        msg = {"text": "!! h"}
        r = app.bot(msg)
        self.assertEquals(r, 'Sorry, I dont uderstand that command')

class ChatBotTestHelp(unittest.TestCase):
    def test_bangbang_means_command(self):
        msg = {"text": "!! help"}
        r = app.bot(msg)
        self.assertEquals(r, 'The options are about, help, say: !! say <words to say>, mario, softkitty, yoshi, and kenny')
    
    # def test_no_bangbang_means_no_command(self):
    #     r = random_functions.get_chatbot_response('hi')
    #     self.assertEquals(r, 'Not a command')

if __name__ == '__main__':
    unittest.main()