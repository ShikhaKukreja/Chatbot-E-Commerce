require('../styles/App.css');
require('../styles/Login.css');

import React from 'react';
import ChatApp from './ChatApp';

class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = { domainName: '' };

    // Bind 'this' to event handlers. React ES6 does not do this by default
    this.domainChangeHandler = this.domainChangeHandler.bind(this);
    this.domainSubmitHandler = this.domainSubmitHandler.bind(this);
  }

  domainChangeHandler(event) {
    this.setState({ domainName: event.target.value });
  }

  domainSubmitHandler(event) {
    event.preventDefault();
    fetch('http://127.0.0.1:5001/',{
      method: 'POST',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'text/plain'
      },
      body: JSON.stringify({
        "Domain":this.state.domainName
      })
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
      console.log(data.clientID);
      this.setState({submitted: true, clientID: data.clientID, message:data});
    }.bind(this))
    .catch( function() {
    })
    
  }

  render() {
    if (this.state.submitted) {
      // Form was submitted, now show the main App
      return (
        <ChatApp domainName={this.state.domainName} clientID={this.state.clientID} message={this.state.message} />
      );
    }

    // Initial page load, show a simple login form
    return (
      <form onSubmit={this.domainSubmitHandler} className="username-container">
        <h1>Welcome to Chatbot Project</h1>
        <div>
          <input
            type="text"
            onChange={this.domainChangeHandler}
            placeholder="Enter a domain name..."
            required />
        </div>
        <input type="submit" value="Submit" />
      </form>
    );
  }

}
App.defaultProps = {
};

export default App;
