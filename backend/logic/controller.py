import os

import json


'''
# Initialize this project with firebase support
# KEYS file not shared for security reasons
key_object = {
    "type": os.environ.get('TYPE'),
    "project_id": os.environ.get('PROJECT_ID'),
    "private_key_id": os.environ.get('PRIVATE_KEY_ID'),
    "private_key": os.environ.get('PRIVATE_KEY').replace('\\n', '\n'),
    "client_email": os.environ.get('CLIENT_EMAIL'),
    "client_id": os.environ.get('CLIENT_ID'),
    "auth_uri": os.environ.get('AUTH_URI'),
    "token_uri": os.environ.get('TOKEN_URI'),
    "auth_provider_x509_cert_url": os.environ.get('AUTH_PROVIDER_X509_CERT_URL'),
    "client_x509_cert_url": os.environ.get('CLIENT_X509_CERT_URL')
}

USER_ID = "cldelahan@gmail.com"

cred = credentials.Certificate(key_object)

# Initialize the app to service account
try:
    firebase_admin.initialize_app(cred, {
        'databaseURL' : 'https://sightq-d333a.firebaseio.com/'
        # https://firebase.google.com/docs/database/admin/start#python
        # ^ how to initialize with separate security rules
    })
except:
    print("Duplicate Firebase Avoided")
# get data from reference
ref = db.reference("/meetings")

def get_meetings_helper():
    result = ref.get()
    output_mtgs = []
    for meeting_id in result:
        mtg_data = (result[meeting_id])["meeting"]
        mtg_stats = (result[meeting_id])["stats"]
        mtg_json = {
            "id": mtg_data["id"],
            "analyzed": mtg_data["analyzed"],
            "title": mtg_data["topic"],
            "duration": mtg_data["duration"],
            "imageUrl": mtg_data["speaker_vid_url"],
            "scores": {
                "complexity": mtg_stats["complexity"],
                "active_time": 1 - mtg_stats["silence"],
                "participation_score": mtg_stats["participation_score"],
                "engagement_score": mtg_stats["engagement_score"]
        }}
        output_mtgs.append(mtg_json)
    return output_mtgs

def get_specific_meeting_helper(meeting_id):
    result = ref.get()
    try:
        mtg_data = result[meeting_id]["meeting"]
        mtg_stats = result[meeting_id]["stats"]
    except:
        return None
    mtg_json = {
        "id": mtg_data["id"],
        "title": mtg_data["topic"],
        "duration": mtg_data["duration"],
        "imageUrl": mtg_data["speaker_vid_url"],
        "n_participation": mtg_data["n_participants"],
        "start_time": mtg_data["start_time"],
        "participants": mtg_data["participants"],
        "analyzed": mtg_data["analyzed"],
        "scores": {
            #"involvement": mtg_stats["involvement"],
            "complexity": mtg_stats["complexity"],
            "participation_score": mtg_stats["participation_score"],
            "engagement_score": mtg_stats["engagement_score"],
            "active_time": 1 - mtg_stats["silence"]
        },
        "properties": {
            "participation": mtg_stats["participation"],
            "engagement": mtg_stats["engagement"],
            "lowest_participants": mtg_stats["lowest_participants"],
            "unanswered": mtg_stats["unanswered"]
        }}
    return mtg_json

def get_historical_field(field):
    result = ref.get()
    output_mtgs = []
    for meeting_id in result:
        mtg_data = result[meeting_id]["meeting"]
        mtg_stats = result[meeting_id]["stats"]
        mtg_json = {
            "start_time": mtg_data["start_time"],
            "value": mtg_stats[field]
        }
        output_mtgs.append(mtg_json)
    return output_mtgs


def get_meeting_and_metrics(meeting_id):
    meetings = zp.get_all_meetings()
    for meeting in meetings:
        if meeting.meeting_id == meeting_id:
            metric = analysis.get_meeting_metrics(meeting)

'''