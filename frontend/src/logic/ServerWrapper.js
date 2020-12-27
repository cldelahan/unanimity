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
        console.log(response);
        if (!response.success) { return null; }
        return response.data;
    }
}