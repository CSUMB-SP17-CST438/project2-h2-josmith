import * as React from 'react';
import { Message } from './Message';

export class MessageList
extends React.Component {
   render() {
        const listItems = this.props.message.map((m) => {
            return <Message key={m} message={m} />;
        });
        return (
            <div>
            My favorive Animals:
            <ul>{listItems}</ul>
            </div>
            );
    }
}
