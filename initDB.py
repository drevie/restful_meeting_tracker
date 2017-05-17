import sqlite3

global fuzeDB


class Fuze_DB:

    def __init__(self, db, cursor):
        self.db = db
        self.cursor = self.db.cursor()

    def spinDB(self):

        self.cursor.execute('''
            CREATE TABLE hosts(
            id INTEGER PRIMARY KEY,
            email VARCHAR) ''')

        # Create a meetings table for this API with the cursor
        self.cursor.execute('''
            CREATE TABLE meetings(
            id INTEGER PRIMARY KEY,
            ownerID INTEGER,
            FOREIGN KEY(ownerID) REFERENCES hosts(id))''')

        self.cursor.execute('''
        CREATE TABLE recordings(
        url VARCHAR PRIMARY KEY,
        protectionLevel VARCHAR,
        password VARCHAR,
        meetingID INTEGER,
        FOREIGN KEY(meetingID) REFERENCES meetings(id))''')

        self.db.commit()

    def insertTestValues(self):
        meetings = [
            {
                'id': 1,
                'ownerID': 1
            },
            {
                'id': 2,
                'ownerID': 2
            },
            {
                'id': 3,
                'ownerID': 3
            },
            {
                'id': 4,
                'ownerID': 4
            }
        ]

        hosts = [
            {
                'id': 1,
                'email': u'test1@gmail.com'
            },
            {
                'id': 2,
                'email': u'test2@gmail.com'
            },
            {
                'id': 3,
                'email': u'test3@gmail.com'
            },
            {
                'id': 4,
                'email': u'test4@gmail.com'
            },
        ]

        recordings = [
            {
                'url': u'https://www.meeting1.com',
                'protectionLevel': True,
                'password': u'cats',
                'meetingID': 1
            },
            {
                'url': u'https://www.meeting2.com',
                'protectionLevel': False,
                'password': u'',
                'meetingID': 2
            },
            {
                'url': u'https://www.meeting3.com',
                'protectionLevel': True,
                'password': u'dogs',
                'meetingID': 3
            },
            {
                'url': u'https://www.meeting4.com',
                'protectionLevel': False,
                'password': u'',
                'meetingID': 4
            },
        ]

        # Populate meetings
        self.cursor.execute(''' INSERT INTO meetings(id, ownerID) VALUES (?,?)''', (meetings[0]['id'], meetings[0]['ownerID']))
        self.cursor.execute(''' INSERT INTO meetings(id, ownerID) VALUES (?,?)''', (meetings[1]['id'], meetings[1]['ownerID']))
        self.cursor.execute(''' INSERT INTO meetings(id, ownerID) VALUES (?,?)''', (meetings[2]['id'], meetings[2]['ownerID']))
        self.cursor.execute(''' INSERT INTO meetings(id, ownerID) VALUES (?,?)''', (meetings[3]['id'], meetings[3]['ownerID']))

        # Populate hosts
        self.cursor.execute(''' INSERT INTO hosts(id, email) VALUES (?,?) ''', (hosts[0]['id'], hosts[0]['email']))
        self.cursor.execute(''' INSERT INTO hosts(id, email) VALUES (?,?) ''', (hosts[1]['id'], hosts[1]['email']))
        self.cursor.execute(''' INSERT INTO hosts(id, email) VALUES (?,?) ''', (hosts[2]['id'], hosts[2]['email']))
        self.cursor.execute(''' INSERT INTO hosts(id, email) VALUES (?,?) ''', (hosts[3]['id'], hosts[3]['email']))

        # Populate recordings
        self.cursor.execute(''' INSERT INTO recordings(url, protectionLevel, password, meetingID) VALUES (?,?,?,?) ''', (recordings[0]['url'], recordings[0]['protectionLevel'], recordings[0]['password'], recordings[0]['meetingID']))
        self.cursor.execute(''' INSERT INTO recordings(url, protectionLevel, password, meetingID) VALUES (?,?,?,?) ''', (recordings[1]['url'], recordings[1]['protectionLevel'], recordings[1]['password'], recordings[1]['meetingID']))
        self.cursor.execute(''' INSERT INTO recordings(url, protectionLevel, password, meetingID) VALUES (?,?,?,?) ''', (recordings[2]['url'], recordings[2]['protectionLevel'], recordings[2]['password'], recordings[2]['meetingID']))
        self.cursor.execute(''' INSERT INTO recordings(url, protectionLevel, password, meetingID) VALUES (?,?,?,?) ''', (recordings[3]['url'], recordings[3]['protectionLevel'], recordings[3]['password'], recordings[3]['meetingID']))

    def testPrint(self):
        print("test print")


def init():
    global fuzeDB
    # Here we create a temporary db in RAM
    db = sqlite3.connect(':memory:', check_same_thread=False)

    # Create a curson for the db
    cursor = db.cursor()
    fuzeDB = Fuze_DB(db, cursor)
    fuzeDB.spinDB()
    fuzeDB.insertTestValues()
