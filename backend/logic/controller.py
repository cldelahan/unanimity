import os
import json
import pymongo
import string
import random
# To read from .env
from decouple import config
from bson.objectid import ObjectId
# For email sending
from smtplib import SMTP
from email.mime.text import MIMEText

MONGODB_KEY = config('MONGODB_KEY')
DB_NAME = config('DB_NAME')
SESS_COL = config('SESS_COL')
USER_COL = config('USER_COL')
EMAIL_OUT = config('EMAIL_OUT')
EMAIL_PASS = config('EMAIL_PASS')
EMAIL_SERVER = config('EMAIL_SERVER')
EMAIL_OUT_PORT = config('EMAIL_OUT_PORT')

try:
    client = pymongo.MongoClient(MONGODB_KEY)
    db = client[DB_NAME]
except:
    client = None
    db = None


'''
Determines if a sessionID has already voted
'''
def is_vote_eligible(sessionID):
    if (db == None):
        return None
    sess_col = db[SESS_COL]
    query = {'sessionIDs.' + sessionID : {"$exists" : True}}
    doc = sess_col.find(query).next() # get the first (TODO: Handle if many)
    if (doc == None):
        return False
    userID = doc["sessionIDs"][sessionID]
    if ('voting' not in doc or userID not in doc['voting']):
        return True
    return False


'''
Return a JSON with :
    {
        title: VoteName
        userName: Name0
        names: [Name1, Name2, ...],
        canVote: True / False
        _id: ID
    }
'''
def get_session_screen_data(sessionID):
    if (db == None):
        return None
    sess_col = db[SESS_COL]
    query = {'sessionIDs.' + sessionID : {"$exists" : True}}
    doc = sess_col.find(query).next() # get the first (TODO: Handle if many)
    if (doc == None):
        return None
    userID = doc["sessionIDs"][sessionID]
    voterIDs = doc["voters"]
    canVote = False
    print(doc)
    if ('voting' not in doc or userID not in doc['voting']):
        canVote = True
    voterNames = turn_obj_ids_to_name(voterIDs)
    retVoterIDs = []
    for i in voterIDs:
        retVoterIDs.append(i.__str__())

    print(userID)
    print(voterIDs)
    print(voterNames)

    index = voterIDs.index(ObjectId(userID))


    result = {
        "_id" : doc["_id"].__str__(),
        "title" : doc["title"],
        "userName" : voterNames[index],
        "canVote": canVote,
        "names": voterNames,
        "userIDs": retVoterIDs
    }
    return result


'''
Takes an array of IDs and turns them into names.
Input:
    [OBJID1, OBJID2]

Output:
    [Name1, Name2]
'''
def turn_obj_ids_to_name(ids):
    if (db == None):
        return None
    user_col = db[USER_COL]
    names = []
    for i in ids: # i is an ObjectID
        query = {"_id": i}
        result = user_col.find(query)
        if (result == None):
            names.append("")
        for r in result:
            names.append(r["name"])
    return names


'''
Takes a sessionID, and a voting JSON object, and sets the vote
INPUT:
    sessionID, userID, { user1: percent1, user2: percent2 }
OUTPUT: True / False

'''
def vote(sessionID, votes):
    if (db == None):
        return None
    sess_col = db[SESS_COL]
    query = {'sessionIDs.' + sessionID : {"$exists" : True}}
    doc = sess_col.find(query).next() # get the first (TODO: Handle if many)
    if (doc == None):
        return False
    # doc is the database json document with the sessionID
    docID = doc['_id']
    userID = doc['sessionIDs'][sessionID]

    print(userID)
    print(doc['voting'])

    if (userID in doc['voting']):
        return False
    else:
        voting = doc['voting']
        print(voting)
        voting[userID] = votes
        print(voting)

        print(userID)
        print(doc['voting'])
        sess_col.update({"_id": ObjectId(docID)}, {"$set" : {"voting" : voting}})
        return True

'''
Takes an array of names and emails, and inserts the names / emails into the
'Users' collection (if they don't already exist). ObjectIDs to access
each user are returned.
'''
def put_into_user_database(names, emails):
    if (db == None):
        return None
    if (not len(names) == len(emails)):
        return None
    user_col = db[USER_COL]
    objectIDs = []
    for i in range (len(names)):
        print(names[i], emails[i])
        query = {"email": emails[i]}
        result = list(user_col.find(query))
        if (len(result) == 0):
            # Insert into database and then get the new _id
            res = user_col.insert_one({"name" : names[i], "email" : emails[i], "sessions" : []})
            objectIDs.append(res.inserted_id)
        else:
            # There is at least 1 user in the database with that email
            # We need to enforce that there is only one, but for now
            # ... we assume 1 and return the first element
            objectIDs.append(result[0]["_id"])
    return objectIDs


'''
Generates a random string of length size for a session ID
'''
def generateString(length):
    output = ""
    for i in range(length):
        output += random.choice(string.ascii_uppercase)
    return output

'''
This takes an array of userIDs and a title, and
1) Creates the sessionID codes for each user
2) Creates the session
3) Assigns the sessionIDs and other data to the session
The new session _id (mongodb) and the sessionID keys are returned
'''
def create_session(userIDs, title):
    if (db == None):
        return None
    sess_col = db["Sessions"]
    user_col = db["Users"]

    sessionIDs_arr = []
    sessionIDs = {}
    for i in userIDs:
        temp_id = generateString(7)
        sessionIDs[temp_id] = i.__str__()
        sessionIDs_arr.append(temp_id)
    insertJSON = {
        "title" : title,
        "voters": userIDs,
        "sessionIDs": sessionIDs
    }
    res = sess_col.insert_one(insertJSON)

     # For each user, append this new session to their session's array
    for i in userIDs:
        query = {"_id": i}
        doc = user_col.find(query).next()
        sessions = doc["sessions"]
        sessions.append(res.inserted_id)
        user_col.update({"_id": i}, {"$set" : {"sessions" : sessions}})

    return [res.inserted_id, sessionIDs_arr]


'''
Takes a list of names, a list of emails, a list of sessionIDs,
and the title of the event and sends emails to each person
informing them of the voting and of their sessionID.
'''
def send_emails(names, emails, sessionIDs, title):
    if (not len(names) == len(emails) or not len(emails) == len(sessionIDs)):
        return None
    smtp = SMTP()
    smtp.connect(EMAIL_SERVER, EMAIL_OUT_PORT)
    smtp.ehlo()
    smtp.starttls()
    smtp.ehlo()
    smtp.login(EMAIL_OUT, EMAIL_PASS)
    for i in range(len(names)):
        content = "Hello " + names[i] + "\n"
        content += "You have been invited to a unanimity voting session: " + title + "\n"
        content += "Please visit www.unanimity.com and use your personalized sessionID: \n"
        content += sessionIDs[i] + "\n"
        content += "Thank you,\n"
        content += "The Unanimity Team"
        smtp.sendmail(
            EMAIL_OUT,
            emails[i],
            content)
    smtp.quit()
