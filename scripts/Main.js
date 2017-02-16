import * as React from 'react';
import * as ReactDOM from 'react-dom';
import { Socket } from './Socket';
import ChatApp from './ChatApp';
import GoogleLogin from 'react-google-login';

const responseGoogle = (response) => {
  console.log(response);
};

ReactDOM.render(
  <GoogleLogin
    clientId="339887222847-7237f4eqsp22ddnj9h44chgbnoq1s8mk.apps.googleusercontent.com"
    buttonText="Login"
    onSuccess={responseGoogle}
    onFailure={responseGoogle}
  />,
  document.getElementById('googleButton')
);

ReactDOM.render(<ChatApp />, document.getElementById('content'));
Socket.on('connect', function() {
    console.log('Connecting to the server!');
});
