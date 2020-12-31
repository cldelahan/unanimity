import {Component} from "react";
import ServerWrapper from "./logic/ServerWrapper";
import {Col, Row, Button, Form} from "react-bootstrap";


class CreateSession extends Component {

    constructor(props) {
        super(props);
        this.state = {
            'title': "",
            'names': [],
            'emails': [],
            'loaded': false,
            'numVoters': 0
        }
        this.onChangeNumVoters = this.onChangeNumVoters.bind(this);
        this.onChangeTitle = this.onChangeTitle.bind(this);
        this.handleFormChange = this.handleFormChange.bind(this);
        this.submitForm = this.submitForm.bind(this);
    }

    onChangeNumVoters(e) {
        this.setState({'numVoters': e.target.value});
        console.log(e.target.value);
    }

    onChangeTitle(e) {
        this.setState({'title': e.target.value});
        console.log(e.target.value);
    }

    handleFormChange(e) {
        if (e.target.name % 2 == 1) {
            this.state.emails[(e.target.name - 1) / 2] = e.target.value;
        } else {
            this.state.names[e.target.name / 2] = e.target.value;
        }
    }

    async submitForm() {
        console.log(this.state.names);
        console.log(this.state.emails);
        if (window.confirm("Are you sure you want to submit. Please check that all data are correct. ")) {
            // Post names to database and have emails be sent out
            await ServerWrapper.createNewSession(this.state.names, this.state.emails, this.state.title);
            window.location = "/";
        } else {
            // Do nothing
        }
    }

    generateForm() {
        // Reset to size 0
        this.state.names = [];
        this.state.emails = [];
        let formHTML = [];
        for (let i = 0; i < this.state.numVoters; i++) {
            // Get sizing correct
            this.state.names.push("");
            this.state.emails.push("");
            formHTML.push(
                <Row>
                        <Form.Control key = {i * 2} name={i * 2} onChange={this.handleFormChange} placeholder="Name"/>
                        <Form.Control key = {i * 2 + 1} name={i * 2 + 1} onChange={this.handleFormChange} placeholder="Email"/>
                </Row>);
        }
        return (<Form>
            {formHTML}
            <Button variant="primary" onClick={this.submitForm}>
                Submit
            </Button>
        </Form>);
    }

    render() {
        return (
            <>
                <div className="App">
                    <header className="App-header">
                        <h1> Unanimity </h1>
                        <p> Session Title </p>
                        <input id={'title'} type={"text"} placeholder={"Enter Title"} onChange={this.onChangeTitle} required/>
                        <p> Number of Voters</p>
                        <input id={'numUsers'} type={"number"} onChange={this.onChangeNumVoters} min="0"
                               max="10" required/>
                        <br/>
                        {this.generateForm()}

                        <br/>

                    </header>
                </div>
            </>
        );
    }
}

export {CreateSession};
