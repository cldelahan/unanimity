from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from logic import controller

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
    print(votes)
    res = controller.vote(sessionID, votes)
    return jsonify({
        'success': res
    })



#######################
### SIGN IN METHODS ###
#######################

'''
# Sign-in methods
@app.route("/user/<uid>", methods = ["POST"])
def get_user(uid):
    return None


# Sign-in methods
@app.route("/sign-in", methods = ["POST"])
def sign_in():
    return None

# Process Recording
@app.route("/recording", methods = ["POST"])
def process_recording():
    data = request.get_json(force=True)
    assert(data['event'] == 'recording.completed')
    controller.get_meeting_and_metrics(data['payload']['object']['uuid'])
    return jsonify({
        'success': True
    })

# Process Transcript
@app.route("/transcript", methods = ["POST"])
def process_transcript():
    return None

'''

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