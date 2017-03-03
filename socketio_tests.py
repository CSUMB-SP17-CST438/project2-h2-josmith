import app, unittest

class SocketIOTestCase(unittest.TestCase):
    def test_server_sends_hello(self):
        
        client = app.socketio.test_client(app.app)
        
        r = client.get_received()
        
        # print r
        
        self.assertEquals(len(r), 1)
        
        from_server = r[0]
        
        self.assertEquals(
            from_server['name'],
            'hello to client'
        )
        
        data = from_server['args'][0]
        self.assertEquals(data['message'], 'Hey there!')

if __name__ == '__main__':
    unittest.main()