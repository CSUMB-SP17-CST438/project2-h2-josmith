import * as React from 'react';

export class Message
extends React.Component {
    render() {
        return <li>{this.props.message}</li>;
    }
}