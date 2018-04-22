import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';

class App extends Component {
    constructor(props) {
        super(props);
        this.state = {
            words: {},
            data: require('./word_count.json')
        }
    }
    
    render() {
        console.log(this.state.data);
        return (
            <div className="App">
                <div className="jsonData">
                    {JSON.stringify(this.state.data)}
                </div> 
            </div>
        );
    }
}

export default App;
