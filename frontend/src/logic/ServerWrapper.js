/*
    This file acts as a wrapper for server calls. Encapsulates error handling, data formatting,
    and retrieval for front end functions.

    Author: Conner Delahanty

 */
import axios from 'axios';

const qs = require('qs');

export default class ServerWrapper {

    static hostURL = 'http://localhost:5000/';

    /*
        Get all functions, and server status functions
    */

    static getServerStatus = async () => {
        const response = (await axios.get(this.hostURL)).data;
        if (!response.success) { return null; }
        return response.data;
    }

    static getSessionInformation = async (sessionID) => {
        const response = (await axios.get(this.hostURL + "session/" + sessionID)).data;
        if (!response.success) { return null; }
        return response.data;
    }


    /*
        Post functions
     */

    static postVotesToDatabase = async (sessionID, votes) => {
        const response = (await axios.post(this.hostURL + "session/" + sessionID, votes)).data;
        if (!response.success) { return null; }
        return response.data;
    }

    static createNewSession = async (names, emails, title) => {
        const response = (await axios.post(this.hostURL + "session", {"names": names, "emails" : emails, "title": title})).data;
        if (!response.success) { return null; }
        return response.data;
    }
}