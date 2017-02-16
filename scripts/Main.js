import * as React from 'react';
import * as ReactDOM from 'react-dom';
import { Socket } from './Socket';
import ChatApp from './ChatApp';
import GoogleLogin from 'react-google-login';
import FacebookLogin from 'react-facebook-login';

const responseGoogle = (response) => {
  console.log(response);
  alert(response);
};

 
const responseFacebook = (response) => {
  console.log(response);
  alert(response);
};
 
ReactDOM.render(
  <FacebookLogin
    appId="252733528514405"
    autoLoad={true}
    fields="name,email,picture"
    callback={responseFacebook}

    />,
  document.getElementById('facebook')
);

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
