import React from 'react';

class Message extends React.Component {
  render() {
    // Was the message sent by the current user. If so, add a css class
    const fromMe = this.props.fromMe ? 'from-me' : '';
    const message = JSON.parse(this.props.message)

    return (
      <div className={`message ${fromMe}`}>
        <div className='username'>
          { this.props.username }
        </div>
        <div className='message-body'>
          { message.Text }
        </div>
        <div className='message-body'>
          { message.Button }
        </div>
        <div className='message-body'>
          { message.Template }
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
