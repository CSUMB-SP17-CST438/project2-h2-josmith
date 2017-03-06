  # integration_tests.py
import app, unittest, flask_testing, requests
import urllib2

msg = """<html>
    <head>
          <link rel="stylesheet" href="static/styles.css">
          <link href="https://fonts.googleapis.com/css?family=Inconsolata" rel="stylesheet">
    </head>
    <body>
        
        <div id="content"></div>
          </div>
        <script type="text/javascript" src="/static/script.js"></script>
    </body>
</html>"""

class ServerIntegrationTestCase(
    flask_testing.LiveServerTestCase
):
    def create_app(self):
        return app.app
    
    def test_server_sends_hello(self):
        r = requests.get(self.get_server_url())
        print r.text
        self.assertEquals(r.text, msg)
        
class TestNotRenderTemplates(flask_testing.LiveServerTestCase):

    def create_app(self):
        return app.app

    def test_assert_mytemplate_used(self):
        r = urllib2.urlopen(self.get_server_url())
        self.assertEqual(r.code, 200)
    
if __name__ == '__main__':
    unittest.main()