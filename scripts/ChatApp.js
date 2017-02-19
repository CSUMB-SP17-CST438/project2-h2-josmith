import * as React from 'react';
import { Socket } from './Socket';
import GoogleLogin from 'react-google-login';
import FacebookLogin from 'react-facebook-login';

var Social = React.createClass({
	getInitialState() {
		return {showResults: true};
	},

	handleSubmit(e) {
		e.preventDefault();
		this.setState({ showResults: false });
	},
    
    render: function() {
    	
        return (
            	<div className="social" onClick={this.Social}>
			<GoogleLogin
			    clientId="339887222847-7237f4eqsp22ddnj9h44chgbnoq1s8mk.apps.googleusercontent.com"
			    buttonText="Login"
			    scope="profile email"
			    onSuccess={responseGoogle}
			    onFailure={responseGoogle}
			  />
			    <FacebookLogin
				    appId="252733528514405"
				    autoLoad={false}
				    fields="name,email,picture"
				    callback={responseFacebook}
				/>
				</div>
			
    )}
});




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

const responseGoogle = (response) => {

  //response['picture']['data']['url'];
  //response['name'];
  
  if(response['profileObj']['name'] != ""){
  	  Socket.emit('google:athenticate', response);
  }
};


const responseFacebook = (response) => {

 // alert(response['picture']['data']['url']);
    if(response['picture']['data']['url'] != ""){
  	  Socket.emit('facebook:athenticate', response);
  	  
  }
};


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



var ChatApp = React.createClass({

	getInitialState() {
		return {images: [], users: [], messages:[], text: ''};
	},

	componentDidMount() {
		Socket.on('init', this._initialize);
		Socket.on('send:message', this._messageRecieve);
		Socket.on('user:joinFB', this._userJoinedFB);
		Socket.on('user:joinG', this._userJoinedG);
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
	_userJoinedFB(data) {
		var {users, messages, images} = this.state;
		var name2 = '';
		var image2 = '';
		var the_name = data['fb'];
		var name = the_name['name'];
		var the_image = data['fb'];
		var image = the_image['picture']['data']['url'];
        
		users.push(name);
		if(users.length > 1){
			name2 = name;
			image2 = image;
		}
		images.push(image);
		messages.push({
			user: 'APPLICATION BOT',
			text : name +' Joined'
		});
		console.log(this.state);
		this.setState({name2, image2, images, users, messages});
	},
		_userJoinedG(data) {
		var {users, messages, images} = this.state;
		var the_name = data['g'];
		var name = the_name['name'];
		var the_image = data['g'];
		var image = the_image['imageUrl'];
		
		var name2 = '';
		var image2 = '';

		if(users.length > 1){
			name2 = name;
			image2 = image;
		}
		
		users.push(name);
		images.push(image);
		messages.push({
			user: 'APPLICATION BOT',
			text : name +' Joined'
		});
		console.log(this.state);
		this.setState({name2, image2, images, users, messages});
		
	},


	handleMessageSubmit(message) {
		var {messages} = this.state;
		messages.push(message);
		this.setState({messages});
		Socket.emit('send:message', message);
	},

	render() {
		return (
			<div>
		
		        <Social />
				<div >
				   <UserCount
						users={this.state.users}
					/>
					<UsersList
						users={this.state.users}
					/>
				</div>
				<div id="device" className="user-stat">
				<div className="chat">
				   <MessageList
					   messages={this.state.messages}
				   />
				</div>
				<MessageForm
					onMessageSubmit={this.handleMessageSubmit}
					user={this.state.name2}
					image={this.state.images[this.state.image2]}
				/>
			    
				</div>

			</div>
		);
	}
});

Socket.on('connect', function() {
  //  console.log('Connecting to the server!');
});

export default ChatApp;