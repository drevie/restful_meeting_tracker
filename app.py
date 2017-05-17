from flask import Flask, jsonify, abort, make_response, request
import sqlite3
import initDB

"""
Things we need in this task

1. SQLite DB
    a. Meeting
    b. Recording
    c. Host
2. REST API
    a. GET
    b. POST
    c. UPDATE
    d. DELETE
"""


app = Flask(__name__)


""" GET METHODS """
''' Here we create methods to retrieve varioud information about the meeting from the RESTful API '''


@app.route('/Fuze_Meetings/api/v1/meetings', methods=['GET'])
def get_meetings():
    initDB.fuzeDB.cursor.execute(''' SELECT id, ownerID FROM meetings''')
    meetings = initDB.fuzeDB.cursor.fetchall()
    return jsonify({'meetings': meetings})


@app.route('/Fuze_Meetings/api/v1/meetings/<int:meetingID>', methods=['GET'])
def get_meeting(meetingID):
    initDB.fuzeDB.cursor.execute(''' SELECT id, ownerID FROM meetings WHERE id=?''', (meetingID,))
    meeting = initDB.fuzeDB.cursor.fetchone()

    if(len(meeting) == 0):
        # Meeting not found
        abort(404)

    return jsonify({'meeting': meeting})


# Here we access a meetings recording url with a password if it is required
@app.route('/Fuze_Meetings/api/v1/recordings/<int:meetingID>/<string:meetingPassword>', methods=['GET'])
def getRecording(meetingID, meetingPassword):
    initDB.fuzeDB.cursor.execute(''' SELECT url, password, protectionLevel FROM recordings WHERE(meetingID=?)''', (meetingID,))
    url = initDB.fuzeDB.cursor.fetchone()

    if(url is None):
        abort(404)
    if(len(url) == 0):
        abort(404)

    if(int(url[2]) == 0):
        print(url[2])
        return jsonify({'url': url[0]})

    elif(int(url[2]) == 1):
        if(url[1] == meetingPassword):
            return jsonify({'url': url[0]})
        else:
            abort(404)


@app.errorhandler(404)
def notFound(error):
    return make_response(jsonify({'error': 'Invalid Request!'}), 404)


""" POST METHODS """
''' Here we define post methods to insert new meeting item into the DB '''


@app.route('/Fuze_Meetings/api/v1/meetings', methods=['POST'])
def createNewMeeting():
    # We must make sure this is a properly formed meeting requrest as the title is required
    if not request.json or not 'ownerID' in request.json:
        abort(400)

    ownerID = request.json['ownerID']

    initDB.fuzeDB.cursor.execute(''' INSERT INTO meetings(id, ownerID) VALUES(?,?)''', (None, int(ownerID)))

    return jsonify({'meeting': ownerID}), 201


@app.route('/Fuze_Meetings/api/v1/recordings', methods=['POST'])
def createNewRecording():
    # We must make sure this is a properly formed meeting requrest as the title is required
    if not request.json or 'protectionLevel' not in request.json or 'meetingID' not in request.json:
        abort(400)

    newRecording = {
        'url': request.json['url'],
        'protectionLevel': request.json['protectionLevel'],
        'password': request.json['password'],
        'meetingID': request.json['meetingID']
    }

    initDB.fuzeDB.cursor.execute(''' INSERT INTO recordings(url, protectionLevel, password, meetingID) VALUES(?,?,?,?)''', (newRecording['url'], newRecording['protectionLevel'], newRecording['password'], newRecording['meetingID']))

    return jsonify({'meeting': newRecording}), 201


""" UPDATE METHODS """
''' Here we define the methods to update the data '''


@app.route('/Fuze_Meetings/api/v1/meetings/<int:meetingID>', methods=['PUT'])
def updateMeeting(meetingID):

    ''' Now we will catch all of the edge cases to prevent a bad update request '''

    ownerID = request.json['ownerID']

    if not request.json:
        abort(400)
    if 'ownerID' in request.json and type(request.json['ownerID']) is not int:
        abort(400)

    initDB.fuzeDB.cursor.execute(''' UPDATE meetings SET ownerId=? WHERE id=?''', (ownerID, meetingID))

    return jsonify({'ownerID updated': ownerID})


""" DELETE METHODS """
''' Here we define our methods to delete meetings '''


@app.route('/Fuze_Meetings/api/v1/meetings/<int:meetingID>')
def deleteMeeting(meetingID):
    initDB.fuzeDB.cursor.execute(''' DELETE FROM meetings WHERE id=?''', (meetingID,))

    return jsonify({"deleted": True})


if __name__ == "__main__":
    initDB.init()
    app.run(debug=True)
