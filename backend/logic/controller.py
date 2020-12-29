import os
import json
import pymongo
from decouple import config
from bson.objectid import ObjectId

MONGODB_KEY = config('MONGODB_KEY')
DB_NAME = config('DB_NAME')
SESS_COL = config('SESS_COL')
USER_COL = config('USER_COL')

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
    if (userID not in doc['voting']):
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
    if (userID not in doc['voting']):
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

