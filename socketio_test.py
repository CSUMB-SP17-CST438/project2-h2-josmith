# socketio_tests.py
import app, unittest

msg = {u'El': u'107506963085422233753', u'profileObj': {u'name': u'Joshua Smith', u'imageUrl': u'https://lh3.googleusercontent.com/-H8IRQHmytYk/AAAAAAAAAAI/AAAAAAAAABg/zkX47w5SgmQ/s96-c/photo.jpg', u'familyName': u'Smith', u'givenName': u'Joshua', u'email': u'josmith@csumb.edu', u'googleId': u'107506963085422233753'}, u'Zi': {u'idpId': u'google', u'first_issued_at': 1488740411048, u'session_state': {u'extraQueryParams': {u'authuser': u'0'}}, u'access_token': u'ya29.GlwFBA3e5IkJgYMx6N0lHnX44ANWyE99trDNf-wNvgcFN4ywxN5FRXZheywnhyVtHFnhzW6-i9gLfJHXTSKlf8uTsHeiq_V12ZkAsbqAr_hspdFAa-JKsw6QFBmTFw', u'id_token': u'eyJhbGciOiJSUzI1NiIsImtpZCI6IjU5ZDNkNmE1MDIzYmVmYzJhZGVmZGZkNDJiZTJlOGJmODk0YzQ3NjgifQ.eyJpc3MiOiJhY2NvdW50cy5nb29nbGUuY29tIiwiaWF0IjoxNDg4NzQwNDEwLCJleHAiOjE0ODg3NDQwMTAsImF0X2hhc2giOiJkVmhMeEt2YkY2VWV1S0xLUUtIS3BBIiwiYXVkIjoiMzM5ODg3MjIyODQ3LTcyMzdmNGVxc3AyMmRkbmo5aDQ0Y2hnYm5vcTFzOG1rLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwic3ViIjoiMTA3NTA2OTYzMDg1NDIyMjMzNzUzIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImF6cCI6IjMzOTg4NzIyMjg0Ny03MjM3ZjRlcXNwMjJkZG5qOWg0NGNoZ2Jub3Exczhtay5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsImhkIjoiY3N1bWIuZWR1IiwiZW1haWwiOiJqb3NtaXRoQGNzdW1iLmVkdSIsIm5hbWUiOiJKb3NodWEgU21pdGgiLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tLy1IOElSUUhteXRZay9BQUFBQUFBQUFBSS9BQUFBQUFBQUFCZy96a1g0N3c1U2dtUS9zOTYtYy9waG90by5qcGciLCJnaXZlbl9uYW1lIjoiSm9zaHVhIiwiZmFtaWx5X25hbWUiOiJTbWl0aCIsImxvY2FsZSI6ImVuIn0.Nyck31jFzxRYeCIhZ_ajdIn_yyEuzrUOcc4maLV3juWw1_-sT8enCVO21rtxl5QQDKa8n6EllM4jFkac5TiaV_aYkQIgcxuQzoK3SfNmLjwOxEbTJ8cmOze7v7oT-tejM3__aUn2RCCaH22Nfk17-SWd8zh9xF-ct18i3YKJDmVimB-sOjViYGeBFoGVVuVSXXjJM9gh5EsBBI8TMzn4xkqx57qJDggZ4UHI1LtTG-V72TFizJQU7fgOPCL1yGVrWd57o5qmBDihEj_0HdKMOuTg0ktH1MBl1309k1bGbSDxr5NRKZDELdTlsk48_kmt9lULTXgP36fc3IO1SvsgPA', u'login_hint': u'AJDLj6JLG81BXtr3aKLveJkqXTNbI4-XkGGVRpQz_dzUDjFY8McgTrutttqAdpImKqkcUb2B-kkL1DBWc62ba4bGGADIPu_QnTnQqYNT-4JfO-gDeN-np8Q', u'expires_in': 3600, u'expires_at': 1488744011048, u'token_type': u'Bearer', u'scope': u'https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/plus.me openid email profile'}, u'accessToken': u'ya29.GlwFBA3e5IkJgYMx6N0lHnX44ANWyE99trDNf-wNvgcFN4ywxN5FRXZheywnhyVtHFnhzW6-i9gLfJHXTSKlf8uTsHeiq_V12ZkAsbqAr_hspdFAa-JKsw6QFBmTFw', u'tokenId': u'eyJhbGciOiJSUzI1NiIsImtpZCI6IjU5ZDNkNmE1MDIzYmVmYzJhZGVmZGZkNDJiZTJlOGJmODk0YzQ3NjgifQ.eyJpc3MiOiJhY2NvdW50cy5nb29nbGUuY29tIiwiaWF0IjoxNDg4NzQwNDEwLCJleHAiOjE0ODg3NDQwMTAsImF0X2hhc2giOiJkVmhMeEt2YkY2VWV1S0xLUUtIS3BBIiwiYXVkIjoiMzM5ODg3MjIyODQ3LTcyMzdmNGVxc3AyMmRkbmo5aDQ0Y2hnYm5vcTFzOG1rLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwic3ViIjoiMTA3NTA2OTYzMDg1NDIyMjMzNzUzIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImF6cCI6IjMzOTg4NzIyMjg0Ny03MjM3ZjRlcXNwMjJkZG5qOWg0NGNoZ2Jub3Exczhtay5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsImhkIjoiY3N1bWIuZWR1IiwiZW1haWwiOiJqb3NtaXRoQGNzdW1iLmVkdSIsIm5hbWUiOiJKb3NodWEgU21pdGgiLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tLy1IOElSUUhteXRZay9BQUFBQUFBQUFBSS9BQUFBQUFBQUFCZy96a1g0N3c1U2dtUS9zOTYtYy9waG90by5qcGciLCJnaXZlbl9uYW1lIjoiSm9zaHVhIiwiZmFtaWx5X25hbWUiOiJTbWl0aCIsImxvY2FsZSI6ImVuIn0.Nyck31jFzxRYeCIhZ_ajdIn_yyEuzrUOcc4maLV3juWw1_-sT8enCVO21rtxl5QQDKa8n6EllM4jFkac5TiaV_aYkQIgcxuQzoK3SfNmLjwOxEbTJ8cmOze7v7oT-tejM3__aUn2RCCaH22Nfk17-SWd8zh9xF-ct18i3YKJDmVimB-sOjViYGeBFoGVVuVSXXjJM9gh5EsBBI8TMzn4xkqx57qJDggZ4UHI1LtTG-V72TFizJQU7fgOPCL1yGVrWd57o5qmBDihEj_0HdKMOuTg0ktH1MBl1309k1bGbSDxr5NRKZDELdTlsk48_kmt9lULTXgP36fc3IO1SvsgPA', u'w3': {u'wea': u'Smith', u'ofa': u'Joshua', u'U3': u'josmith@csumb.edu', u'Paa': u'https://lh3.googleusercontent.com/-H8IRQHmytYk/AAAAAAAAAAI/AAAAAAAAABg/zkX47w5SgmQ/s96-c/photo.jpg', u'Eea': u'107506963085422233753', u'ig': u'Joshua Smith'}, u'tokenObj': {u'idpId': u'google', u'first_issued_at': 1488740411048, u'session_state': {u'extraQueryParams': {u'authuser': u'0'}}, u'access_token': u'ya29.GlwFBA3e5IkJgYMx6N0lHnX44ANWyE99trDNf-wNvgcFN4ywxN5FRXZheywnhyVtHFnhzW6-i9gLfJHXTSKlf8uTsHeiq_V12ZkAsbqAr_hspdFAa-JKsw6QFBmTFw', u'id_token': u'eyJhbGciOiJSUzI1NiIsImtpZCI6IjU5ZDNkNmE1MDIzYmVmYzJhZGVmZGZkNDJiZTJlOGJmODk0YzQ3NjgifQ.eyJpc3MiOiJhY2NvdW50cy5nb29nbGUuY29tIiwiaWF0IjoxNDg4NzQwNDEwLCJleHAiOjE0ODg3NDQwMTAsImF0X2hhc2giOiJkVmhMeEt2YkY2VWV1S0xLUUtIS3BBIiwiYXVkIjoiMzM5ODg3MjIyODQ3LTcyMzdmNGVxc3AyMmRkbmo5aDQ0Y2hnYm5vcTFzOG1rLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwic3ViIjoiMTA3NTA2OTYzMDg1NDIyMjMzNzUzIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImF6cCI6IjMzOTg4NzIyMjg0Ny03MjM3ZjRlcXNwMjJkZG5qOWg0NGNoZ2Jub3Exczhtay5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsImhkIjoiY3N1bWIuZWR1IiwiZW1haWwiOiJqb3NtaXRoQGNzdW1iLmVkdSIsIm5hbWUiOiJKb3NodWEgU21pdGgiLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tLy1IOElSUUhteXRZay9BQUFBQUFBQUFBSS9BQUFBQUFBQUFCZy96a1g0N3c1U2dtUS9zOTYtYy9waG90by5qcGciLCJnaXZlbl9uYW1lIjoiSm9zaHVhIiwiZmFtaWx5X25hbWUiOiJTbWl0aCIsImxvY2FsZSI6ImVuIn0.Nyck31jFzxRYeCIhZ_ajdIn_yyEuzrUOcc4maLV3juWw1_-sT8enCVO21rtxl5QQDKa8n6EllM4jFkac5TiaV_aYkQIgcxuQzoK3SfNmLjwOxEbTJ8cmOze7v7oT-tejM3__aUn2RCCaH22Nfk17-SWd8zh9xF-ct18i3YKJDmVimB-sOjViYGeBFoGVVuVSXXjJM9gh5EsBBI8TMzn4xkqx57qJDggZ4UHI1LtTG-V72TFizJQU7fgOPCL1yGVrWd57o5qmBDihEj_0HdKMOuTg0ktH1MBl1309k1bGbSDxr5NRKZDELdTlsk48_kmt9lULTXgP36fc3IO1SvsgPA', u'login_hint': u'AJDLj6JLG81BXtr3aKLveJkqXTNbI4-XkGGVRpQz_dzUDjFY8McgTrutttqAdpImKqkcUb2B-kkL1DBWc62ba4bGGADIPu_QnTnQqYNT-4JfO-gDeN-np8Q', u'expires_in': 3600, u'expires_at': 1488744011048, u'token_type': u'Bearer', u'scope': u'https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/plus.me openid email profile'}, u'googleId': u'107506963085422233753'}
msg2 = {u'expiresIn': 4617, u'picture': {u'data': {u'url': u'https://scontent.xx.fbcdn.net/v/t1.0-1/p50x50/14457456_10210934688542219_8214757857053421347_n.jpg?oh=02d55879a8cd409c31643867940a082a&oe=596D9AA0', u'is_silhouette': False}}, u'name': u'Hsoj Htims', u'accessToken': u'EAADl3Bwwn2UBABZCZASptXEwd7skFfXsGGgnPwmdGJ0jd7d3vAZCk4XXH8XqE0ZBEmIjgtqYz6p9Jp8kJmN45SZAn3vrOFFULTGFbZAcx3i4oS26klK8rpuNFKW5a0l8R5bm7ECvEIQ1AEp6ZBuQnKpdpu3nNF1WZCI3vKp0xukspZBlEy6oDZC2AzpSBttnZBjP0EZD', u'userID': u'10212379381058629', u'signedRequest': u'kTjiiRRinZOTdmSgpEsy_n4DQ1HDxhpGaeZLXSu6DQU.eyJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImNvZGUiOiJBUUJUSm4tYkVFSlZvXzNMa2p6d0xaN3JMTTF3ci14ekFYbTFoWWFvWmZaTW83SmduNzR6YWphRWowZUluNGxBVzBOZUtRaU9lSVBCTlZKeFBYdXZsR29pdlItdVJrV0tHR09GdmJQSzg4aE9iZGc1dVJGV2lBMF9iRGxtaW1pc0stR3ZvYUhlQ0JkLWUtdnBMWUVBeEpyTlNxcnBvVXZTVWJKX3ljNjgxSlY2NVBpUU93VzVZakIySWJJUDlzeWVfbVlER181Wm40MllSMGVIQi03Vm9BNTE3R3p0c2RjckpqWDdkQkJJRnVCVGQzZWxmbW1ET3JIemlRVEZESUtIUWZsNm5PVFNXVTVVWWZjU1V5Tmx5bEQyRTVCMnU2UUZyVDJSTW1fRmVsaWF3cnFSS0NmME11OVJ0OGZ0cW02M1ZsWFVJYlh6Q1dpQzdHQ1VSNkNFaHd5LSIsImlzc3VlZF9hdCI6MTQ4ODc0Mjk4MywidXNlcl9pZCI6IjEwMjEyMzc5MzgxMDU4NjI5In0', u'email': u'jsmithwoodworm@yahoo.com', u'id': u'10212379381058629'}
msg3 = {u'text': u'!! help', u'image': u'https://lh3.googleusercontent.com/-H8IRQHmytYk/AAAAAAAAAAI/AAAAAAAAABg/zkX47w5SgmQ/s96-c/photo.jpg', u'user': u'Joshua Smith'}
msg4 = {u'text': u'!! about', u'image': u'https://lh3.googleusercontent.com/-H8IRQHmytYk/AAAAAAAAAAI/AAAAAAAAABg/zkX47w5SgmQ/s96-c/photo.jpg', u'user': u'Joshua Smith'}
msg5 = {u'text': u'!! say testing hi', u'image': u'https://lh3.googleusercontent.com/-H8IRQHmytYk/AAAAAAAAAAI/AAAAAAAAABg/zkX47w5SgmQ/s96-c/photo.jpg', u'user': u'Joshua Smith'}
class SocketIOTestCase(unittest.TestCase):
    
    def test_server_sends_hello(self):
        client = app.socketio.test_client(app.app)
        
        client.get_received()

        client.emit('google:athenticate', msg)
        r = client.get_received()
        # print r[1]['args'][0]['g']['name']
        # print len(r)
        # print r[0]['name']
        # print r[1]['args'][0]['g']['name']
        self.assertEquals(len(r), 2)
        from_server = r[1]['args'][0]['g']
        self.assertEquals(
            from_server['name'],
            'Joshua Smith'
        )
        data = from_server
        self.assertEquals(
            data['email'],
            'josmith@csumb.edu'
        )
        
class SocketIOTestFb(unittest.TestCase):
    
    def test_server_sends_FB(self):
        client = app.socketio.test_client(app.app)
        
        client.get_received()

        client.emit('facebook:athenticate', msg2)
        r = client.get_received()
        # print r[1]['args'][0]['fb']['name']
        # print len(r)
        self.assertEquals(len(r), 2)
        from_server = r[1]['args'][0]['fb']
        self.assertEquals(
            from_server['name'],
            'Hsoj Htims'
        )
        data = from_server
        self.assertEquals(
            data['email'],
            'jsmithwoodworm@yahoo.com'
        )

class SocketIOTestMessageHelp(unittest.TestCase):
    def test_server_sends_message_help(self):
        client = app.socketio.test_client(app.app)
        client.get_received()
        client.emit('facebook:athenticate', msg2)
        client.get_received()
        client.emit('send:message', msg3)
        r = client.get_received()
        # print r[0]['args'][0]
        # print len(r)
        self.assertEquals(len(r), 1)
        from_server = r[0]['args'][0]
        self.assertEquals(
            from_server,
            'The options are about, help, say: !! say <words to say>, mario, softkitty, yoshi, text: !! text <message>, and kenny'
        )
        
class SocketIOTestMessagAbout(unittest.TestCase):
    def test_server_sends_message_about(self):
        client = app.socketio.test_client(app.app)
        client.get_received()
        client.emit('facebook:athenticate', msg2)
        client.get_received()
        client.emit('send:message', msg4)
        r = client.get_received()
        # print r[0]['args'][0]
        # print len(r)
        self.assertEquals(len(r), 1)
        from_server = r[0]['args'][0]
        self.assertEquals(
            from_server,
            'This is a chat app that was build in CSUMBs software engineering class in two weeks'
            )
        
class SocketIOTestMessagSay(unittest.TestCase):
    def test_server_sends_message_say(self):
        client = app.socketio.test_client(app.app)
        client.get_received()
        client.emit('facebook:athenticate', msg2)
        client.get_received()
        client.emit('send:message', msg5)
        r = client.get_received()
        # print r[0]['args'][0]
        # print len(r)
        self.assertEquals(len(r), 1)
        from_server = r[0]['args'][0]
        self.assertEquals(
            from_server,
            'testing hi'
            )
          
        
if __name__ == '__main__':
    unittest.main()