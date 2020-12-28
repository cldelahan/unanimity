import React, {Component} from 'react';
import { BrowserRouter as Router, Route, Switch} from 'react-router-dom';

import { VotingPortal } from './VotingPortal';
import { Home } from './Home';
import {CreateSession} from "./CreateSession";


class App extends Component {
    render() {
        return (
            <React.Fragment>
                    <Router>
                        <Switch>
                            <Route path="/createsession/" component={CreateSession}/>
                            <Route path="/session/:key" component={VotingPortal}/>
                            <Route path="/" component={Home}/>
                        </Switch>
                    </Router>
            </React.Fragment>
        );
    }
}

export default App;