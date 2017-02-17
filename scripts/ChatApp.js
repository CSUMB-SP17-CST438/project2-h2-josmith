import * as React from 'react';
import { Socket } from './Socket';
import GoogleLogin from 'react-google-login';
import FacebookLogin from 'react-facebook-login';

var UsersList = React.createClass({
	render() {
		return (
			<div className='users'>
				<h3> Online Users </h3>
				<ul>
					{
						this.props.users.map((user, i) => {
							return (
								<li key={i}>
									{user}
								</li>
							);
						})
					}
				</ul>				
			</div>
		);
	}
});

var Message = React.createClass({
	render() {
		return (
			<div className="message">
			<img src={this.props.image} />
				<strong>{this.props.user} :</strong> 
				<div><p>{this.props.text}</p></div>		
			</div>
		);
	}
});

var UserCount = React.createClass({
	render() {
		return (
			<div className="user_count">
				<strong>Current Users: {this.props.users.length}</strong> 
			</div>
		);
	}
});

var MessageList = React.createClass({
	render() {
		return (
			<div className='messages'>
				<h2> Conversation: </h2>
				{
					this.props.messages.map((message, i) => {
						return (
							<Message
								key={i}
								image={message.image}
								user={message.user}
								text={message.text} 
							/>
						);
					})
				} 
			</div>
		);
	}
});

var MessageForm = React.createClass({

	getInitialState() {
		return {text: ''};
	},

	handleSubmit(e) {
		e.preventDefault();
		var message = {
			image :this.props.image, 
			user : this.props.user,
			text : this.state.text
		};
		this.props.onMessageSubmit(message);	
		this.setState({ text: '' });
	},

	changeHandler(e) {
		this.setState({ text : e.target.value });
	},

	render() {
		return(
			<div className='message_form'>
				<h3>Write New Message</h3>
				<form onSubmit={this.handleSubmit}>
					<input
						onChange={this.changeHandler}
						value={this.state.text}
					/>
				</form>
			</div>
		);
	}
});

const responseGoogle = (response) => {
  console.log(response);
  alert(response['picture']['data']['url']);
  
  if(!response){
  	  Socket.emit('google:athenticate', response);
  }
};

 
const responseFacebook = (response) => {
  console.log(response);
 // alert(response['picture']['data']['url']);
    if(response['picture']['data']['url'] != ""){
  	  Socket.emit('google:athenticate', response);
  }
};

var ChatApp = React.createClass({

	getInitialState() {
		return {image: [], users: [], messages:[], text: ''};
	},

	componentDidMount() {
		Socket.on('init', this._initialize);
		Socket.on('send:message', this._messageRecieve);
		Socket.on('user:join', this._userJoined);
		Socket.on('user:left', this._userLeft);
	},

	_initialize(data) {
		var {users, name} = data;
		this.setState({users, user: name});
	},

	_messageRecieve(message) {
		var {messages} = this.state;
		messages.push(message);
		this.setState({messages});
	},
	_userJoined(data) {
		var {users, messages} = this.state;
		var the_name = data['users'];
		var name = the_name['name'];
		var the_image = data['users'];
		var image = the_image['picture']['data']['url'];
		console.log(image);
		users.push(name);
		messages.push({
			user: 'APPLICATION BOT',
			text : name +' Joined'
		});
		this.setState({image, name, users, messages});
	},

	_userLeft(data) {
		var {users, messages} = this.state;
		var name = data['users'];
		var index = users.indexOf(name);
		users.splice(index, 1);
		messages.push({
			user: 'APPLICATION BOT',
			text : name +' Left'
		});
		this.setState({users, messages});
	},

	handleMessageSubmit(message) {
		var {messages} = this.state;
		//console.log(messages);
		messages.push(message);
		this.setState({messages});
		Socket.emit('send:message', message);
	},

	render() {
		return (
			<div>
			  <GoogleLogin
			    clientId="339887222847-7237f4eqsp22ddnj9h44chgbnoq1s8mk.apps.googleusercontent.com"
			    buttonText="Login"
			    onSuccess={responseGoogle}
			    onFailure={responseGoogle}
			  />
			    <FacebookLogin
				    appId="252733528514405"
				    autoLoad={true}
				    fields="name,email,picture"
				    callback={responseFacebook}
				/>
			   <UserCount
					users={this.state.users}
				/>
				<UsersList
					users={this.state.users}
				/>
				<div id="device">
				<div className="chat">
				   <MessageList
					   messages={this.state.messages}
				   />
				</div>
				<MessageForm
					onMessageSubmit={this.handleMessageSubmit}
					user={this.state.name}
					image={this.state.image}
				/>
				</div>
			{console.log(this.state.image)}

			</div>
		);
	}
});

Socket.on('connect', function() {
  //  console.log('Connecting to the server!');
});

export default ChatApp;