import React from 'react';
import Messages from './Messages';

class Message extends React.Component {

  constructor(props) {
    super(props);
    this.onClickButton = this.onClickButton.bind(this);
  }

  renderText()
  {
    const fromMe = this.props.fromMe ? 'from-me' : '';
    const message = JSON.parse(this.props.message)
    console.log(message);
    const buttonText = message.Button;
    const text = message.Text;
    if (text.length >= 1) {
      return (
        <span>
          {message.Text}
        </span>
      );
    };
  }

  onClickButton(button)
  {
      //this.state.disabled = true;
      this.props.onSend(button);
      
  }

  render() {
    // Was the message sent by the current user. If so, add a css class
    const fromMe = this.props.fromMe ? 'from-me' : '';
    const message = JSON.parse(this.props.message)
    console.log(message);
    const buttonText = message.Button;
    console.log(buttonText);
    const text = message.Text;

    const buttonTry =  [];
    if (message.Button) {
      console.log(buttonText.length);
      if (buttonText.length !== 0) {
        for (let i = 0; i < buttonText.length; i++ ) {
          buttonTry.push(message.Button[i]);
          console.log(buttonTry);
        }
      }
    }

    
    return (
      <div className={`message ${fromMe}`}>
        <div className='username'>
          { this.props.username }
        </div>
        <div className='message-body'>
          { this.renderText() }
       </div>
       
       <div>
       { buttonTry.map(function(buttonTry1) { 
         return React.createElement("button", { onClick: this.onClickButton.bind(null,buttonTry1)}, buttonTry1);
       }.bind(this)) }
       </div>
      
      </div>
    );
  }

  renderElements(){

  }
}

Message.defaultProps = {
  message: '',
  username: '',
  fromMe: false
};

export default Message;