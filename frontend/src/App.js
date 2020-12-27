import './App.css';
import ServerWrapper from "./logic/ServerWrapper";
import {Component} from "react";

class App extends Component {

    constructor(props) {
        super(props);
        this.state = {
            'loaded': false,
            'data': "Loading Content"
        };
        this.loadContent().then(r => {}, r => {
            alert("Loading page failed: " + r);
        });
    }

    async loadContent() {
        const result = await ServerWrapper.getServerStatus();
        console.log(result);
        this.setState({
            'loaded': true,
            'data': result ? result : "Server Error"
        });
    }

    render() {
        return (
            <div className="App">
                <header className="App-header">
                    {this.state.data}
                    <p>
                        Edit <code>src/App.js</code> and save to reload.
                    </p>
                    <a
                        className="App-link"
                        href="https://reactjs.org"
                        target="_blank"
                        rel="noopener noreferrer"
                    >
                        Learn React
                    </a>
                </header>
            </div>
        );
    }
}

export default App;
