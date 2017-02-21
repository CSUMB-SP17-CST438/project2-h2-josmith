
import * as React from 'react';
import { Socket } from './Socket';
import GoogleLogin from 'react-google-login';
import FacebookLogin from 'react-facebook-login';
import ToggleDisplay from 'react-toggle-display';

var Social = React.createClass({
  
    getInitialState: function() {
        return {
            show: true
        };
    },
    handleClick: function() {
        this.setState({ show: !this.state.show });
    },
    
    render: function() {
        return (
        <div className="social">
            <ToggleDisplay show={this.state.show}>
               <div onClick={ this.handleClick }>
			      <GoogleLogin
			          clientId="339887222847-7237f4eqsp22ddnj9h44chgbnoq1s8mk.apps.googleusercontent.com"
			          buttonText="Google"
			          scope="profile email"
			          onSuccess={responseGoogle}
			          onFailure={responseGoogle}
			     />
			  </div>
			  <div onClick={ this.handleClick }>
			     <FacebookLogin  show={this.state.show}
				     appId="252733528514405"
				     autoLoad={false}
				     fields="name,email,picture"
				     callback={responseFacebook}
				     textButton="Facebook"
				 />
				</div>
		    </ToggleDisplay>
		</div>
        );
    }
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
  console.log(response['profileObj']);

  //response['picture']['data']['url'];
  //response['name'];
  //    Socket.on('chat', function (data) {
  //    Socket.sockets.socket(data.clientid).emit('chat', {
  //        msg: data.msg,
  //        senderid : Socket.id
  //    }); 
  //});
  
  if(response['profileObj']['name'] != ""){
  	  Socket.emit('google:athenticate', response);
  }
};

const responseFacebook = (response) => {
  console.log(response);
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
	    Socket.on('user:meFB', this._meJoinedFB);
		Socket.on('user:meG', this._meJoinedG);
		Socket.on('user:left', this._userLeft);
		Socket.on('bot:message', this._botMessage);
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
		var {users, messages} = this.state;
		var the_name = data['fb'];
		var name = the_name['name'];
		users.push(name);
		messages.push({
			user: 'Cooper BOT',
			image: 'http://cdn.mysitemyway.com/etc-mysitemyway/icons/legacy-previews/icons-256/matte-white-square-icons-business/124810-matte-white-square-icon-business-robot.png',
			text : '\n' + name +' Joined for Facebook'
		});
		this.setState({users, messages});
	},
		_meJoinedFB(data) {
		var {name, image} = this.state;
		var the_name = data['fb'];
		name = the_name['name'];
		var the_image = data['fb'];
		image = the_image['picture']['data']['url'];
		
		this.setState({name, image});
	},
		_userJoinedG(data) {
		var {users, messages} = this.state;
		var the_name = data['g'];
		var name = the_name['name'];
		users.push(name);
		messages.push({
			user: 'Copper BOT',
			image: 'http://cdn.mysitemyway.com/etc-mysitemyway/icons/legacy-previews/icons-256/matte-white-square-icons-business/124810-matte-white-square-icon-business-robot.png',
			text : '\n' + name +' Joined from Google'
		});
		this.setState({users, messages});
	},
	_meJoinedG(data) {
		var {name, image} = this.state;
		var the_name = data['g'];
		name = the_name['name'];
		var the_image = data['g'];
		image = the_image['imageUrl'];
		this.setState({name, image});
	},
	_userLeft(data) {
		var {users, messages} = this.state;
		var name = data['users'];
		var index = users.indexOf(name);
		users.splice(index, 1);
		messages.push({
			user: 'Copper BOT',
			image: 'http://cdn.mysitemyway.com/etc-mysitemyway/icons/legacy-previews/icons-256/matte-white-square-icons-business/124810-matte-white-square-icon-business-robot.png',
			text : name +' Left'
		});
		this.setState({users, messages});
	},
	_botMessage(message) {
		var {messages} = this.state;
		messages.push({
			user: 'Copper BOT',
			image: 'http://cdn.mysitemyway.com/etc-mysitemyway/icons/legacy-previews/icons-256/matte-white-square-icons-business/124810-matte-white-square-icon-business-robot.png',
			text : '\n' + message 
		});
		this.setState({messages});
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
					user={this.state.name}
					image={this.state.image}
				/>
				</div>
				<Social />
			</div>
		);
	}
});

Socket.on('connect', function() {
  //  console.log('Connecting to the server!');
});

export default ChatApp;