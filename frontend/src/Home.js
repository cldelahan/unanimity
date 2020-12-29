import './Home.css';
import ServerWrapper from "./logic/ServerWrapper";
import {Component} from "react";
import ReactCodeInput from 'react-verification-code-input';

class Home extends Component {

    constructor(props) {
        super(props);
        this.state = {
            'loaded': false,
            'data': "Loading Content"
        };
        this.loadContent().then(r => {
        }, r => {
            alert("Loading page failed: " + r);
        });
        this.onCodeInput = this.onCodeInput.bind(this);
    }

    async loadContent() {
        const result = await ServerWrapper.getServerStatus();
        console.log(result);
        this.setState({
            'loaded': true,
            'data': result ? result : "Server Error"
        });
    }

    onCodeInput(e) {
        console.log(e);
        window.location = '/session/' + e;
    }

    render() {
        return (
            <>
                <div className="App">
                    <header className="App-header">
                        <h1> Unanimity </h1>
                        {this.state.data}
                        <ReactCodeInput
                            className={'Code-input'}
                            type={'text'}
                            fields={7}
                            title={'Enter Invite Code Below'}
                            onComplete={this.onCodeInput}
                        />
                        <a
                            className={'App-link'}
                            href='/createsession'
                        >
                            Create New Session
                        </a>

                    </header>
                </div>
            </>
        );
    }
}

export {Home};
