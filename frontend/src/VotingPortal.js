import {Component} from "react";
import ServerWrapper from "./logic/ServerWrapper";
import {Col, Row, Button} from "react-bootstrap";


class VotingPortal extends Component {

    constructor(props) {
        super(props);
        this.state = {
            'sessionID': props.match.params.key,
            'loaded': false,
            'data': {
                title: "",
                userName: "",
                userIDs: [],
                names: [],
                canVote: false
            },
            'votes': {}
        }
        this.loadContent().then(r => {
        }, r => {
            alert("Loading page failed: " + r);
        });
        this.onPercentChange = this.onPercentChange.bind(this);
        this.submitVotes = this.submitVotes.bind(this);
    }

    async loadContent() {
        const result = await ServerWrapper.getSessionInformation(this.state.sessionID);
        this.setState({
            'data': result
        })
    }

    onPercentChange(e) {
        console.log(e.target.id);
        console.log(e.target.value);
        const userID = this.state.data.userIDs[e.target.id];
        this.state.votes[userID] = parseInt(e.target.value);
        console.log(this.state.votes);
    }

    async submitVotes() {
        let sum = 0;
        const votePerc = Object.values(this.state.votes);
        for (let i = 0; i < votePerc.length; i++) {
            sum += votePerc[i];
        }

        if (sum !== 100) {
            if (window.confirm("Your percentages do not sum to 100%. Would you like to normalize? " +
                " (Notice: Hitting OK will submit the normalized percentages. This process cannot be undone)")) {
                // Normalize, submit, and leave the page
                window.location = "/";
            } else {
                // Do nothing
            }
        } else {
            if (window.confirm("Are you sure you want to submit. Notice: this action cannot be undone. ")) {
                // Submit and leave the page
                await ServerWrapper.postVotesToDatabase(this.state.sessionID, this.state.votes);
            } else {
                // Do nothing
            }
        }

        console.log(votePerc);
    }


    render() {
        return (
            <>
                <div className="App">
                    <header className="App-header">
                        <h1> {this.state.data.title} </h1>
                        <h2> Welcome {this.state.data.userName} </h2>
                        <p>
                            {!this.state.data.canVote ? <>Sorry, you have already casted your vote for this
                                    session </> :
                                <>Please vote below</>
                            }
                        </p>

                        {this.state.data.canVote ?
                            <>
                                {/* Creating boxes for each name */}
                                <Row style={{"display": "inline"}}>

                                    {this.state.data.names.map((name, index) => {
                                        return (
                                            <Col>
                                                {name} <br/>
                                                <input id={index} type={"number"} onChange={this.onPercentChange} min="0"
                                                       max="100" required/> (%)
                                            </Col>);
                                    })
                                    }
                                </Row>

                                <br/>
                                <Button onClick={this.submitVotes}>Submit Vote</Button>

                            </> : <></>}

                    </header>
                </div>
            </>
        );
    }
}

export {VotingPortal};
