import * as React from 'react';
import * as ReactDOM from 'react-dom';
import { Socket } from './Socket';
import ChatApp from './ChatApp';


ReactDOM.render(<ChatApp />, document.getElementById('content'));
Socket.on('connect', function() {
    console.log('Connecting to the server!');
});
