from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import controller

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

'''
@app.route('/trends/<field>')
def get_trends_for_field(field):
    trends = controller.get_historical_field(field)
    return jsonify({
        'success': True,
        'trends': trends,
        'field': field
    })
'''

# Check that server is online
@app.route("/", methods = ["GET"])
def index():
    return jsonify({
        'success': True,
        'data': 'Server is Live!'})


#########################################
############  GET METHODS  ##############
#########################################


# Given an email, return all relevant session information
# TODO
@app.route("/user/<email>", methods = ["GET"])
def get_all_sessions():
    return jsonify({
            'success': True,
            'data': 'Server is Live!'})



# Given a sessionID, return the content for the voting screen
@app.route("/session/<sessionID>", methods = ["GET"])
def get_session_screen(sessionID):
    result = controller.get_session_screen_data(sessionID)
    if (result == None):
        return jsonify({
            'success': False,
            })
    return jsonify({
            'success': True,
            'data': result
        })


# Given a sessionID, the voterID, and the votes, cast the votes for that user
@app.route("/session/<sessionID>", methods = ["POST"])
def post_vote(sessionID):
    # print(request.json)
    votes = request.get_json()
    res = controller.vote(sessionID, votes)
    return jsonify({
        'success': res
    })


# Given a list of names and emails, create a session and send out emails
@app.route("/session", methods = ["POST"])
def create_session():
    # print(request.json)
    data = request.get_json()
    names = data['names']
    emails = data['emails']
    title = data['title']
    ## Put users and emails into database (and get the objectIDs out)
    userIDs = controller.put_into_user_database(names, emails)
    print(userIDs)
    ## Create the session and return its id + the keys for each user
    [session_objectID, sessionIDs] = controller.create_session(userIDs, title)
    print(session_objectID)
    print(sessionIDs)
    # Send emails to users with the sessionIDs
    controller.send_emails(names, emails, sessionIDs, title)


    return jsonify({
        'success': True
    })


@app.errorhandler(400)
def not_found(error):
    return jsonify({
        "success": False,
        "error_code": 400,
        "message": "Bad Request"
    }), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error_code": 404,
        "message": "Not Found"
    }), 404

@app.errorhandler(500)
def not_found(error):
    return jsonify({
        "success": False,
        "error_code": 500,
        "message": "Internal Server Error"
    }), 500

if __name__ == "__main__":
    app.run(debug=True)