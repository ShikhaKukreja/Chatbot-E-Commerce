require('../styles/ChatApp.css');

import React from 'react';
import io from 'socket.io-client';
import config from '../config';

import Messages from './Messages';
import ChatInput from './ChatInput';

class ChatApp extends React.Component {
  socket = {};
  constructor(props) {
    super(props);
    this.state = { messages: []};
    this.sendHandler = this.sendHandler.bind(this);   
  }

  componentDidMount()
  {
    const botMessageObject = {
      username: "Bot",
      message: JSON.stringify(this.props.message),
      fromMe: false
    };
    
    this.addMessage(botMessageObject);
  }

  createJsonMessage(message)
  {
    if(message.search("@reset") != -1)
      return { 'Text':'','action':'reset','userID':this.props.clientID }

    return { 'Text':message,'action':'','userID':this.props.clientID }
  }

  

  sendHandler(message) {    

    const jsonMessage = this.createJsonMessage(message);

    

    const messageObject = {
      username: "Me",
      message: JSON.stringify(jsonMessage)
    };
    
    fetch('http://127.0.0.1:5001/Input',{
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'text/plain'
      },
      body: JSON.stringify(jsonMessage)
    })
    .then( function(response) {
      return response;
    })
    .then( function(response) {
      setTimeout( function() {
      }, 300);
      return response.json();
    })
    .then( function(data) {
      console.log(data);

      const botMessageObject = {
      username: "Bot",
      message: JSON.stringify(data),
      fromMe: false
      };

      this.addMessage(botMessageObject);
    }.bind(this))
    .catch( function() {
    })
  

    messageObject.fromMe = true;
    this.addMessage(messageObject);
  }

  addMessage(message) {
    // Append the message to the component state
    const messages = this.state.messages;
    messages.push(message);
    this.setState({ messages: messages});
  }

  render() {
    return (
      <div className="container">
        <h3>Chatbot CMPE295 Project</h3>
        <Messages 
        messages={this.state.messages} 
        onSend={this.sendHandler} />
        <ChatInput onSend={this.sendHandler} />
      </div>
    );
  }

}
ChatApp.defaultProps = {
  username: 'Anonymous'
};

export default ChatApp;
