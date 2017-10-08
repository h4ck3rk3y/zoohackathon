import time

import sqlite3

from Alert import Alert
from TwilioClient import TwilioClient
from Rangers import Rangers
from Config import Config

def get_db():
    db = sqlite3.connect('database.db', timeout=10)
    return db

def clean(text):
    return ''.join([i if ord(i) < 128 else '.' for i in text])

class LogProcessor:

    def __init__(self, alerts="Alerts.csv"):
        self.alerts = alerts
        self.client = TwilioClient()
        self.rangers = Rangers()

    def follow(self, alertsFle):
        alertsFle.seek(0,2)
        while True:
            line = alertsFle.readline()
            if not line:
                time.sleep(0.1)
                continue
            yield line

    def processLine(self, line):
        config = Config()
        sensor, sensor_id, time_reported, date_reported, location, label = line.split(',')
        alert = Alert(sensor, sensor_id, time_reported, date_reported, location, label)
        whoToCall = self.rangers.whoToCallDB(alert.location)['number']

        if config.notify():
            if alert.isHighLevelAlert():
                print "[HIGH]%s"%(alert.message())
                if config.isP1SMSEnabled():
                    self.client.sendMessage(whoToCall, alert.message())
                if config.isP1VoipEnabled():
                    self.client.makeCall(whoToCall)
            elif alert.isMediumLevelAlert():
                print "[MEDIUM]%s"%(alert.message())
                if config.isP2SMSEnabled():
                    self.client.sendMessage(whoToCall, alert.message())
                if config.isP2VoipEnabled():
                    self.client.makeCall(whoToCall)
            else:
                print "[LOW]%s"%(alert.message())
                if config.isP3SMSEnabled():
                    self.client.sendMessage(whoToCall, alert.message())
                if config.isP3VoipEnabled():
                    self.client.makeCall(whoToCall)
        else:
            print "----"
            print alert.message()
            print whoToCall
            print "----"

    def processContinously(self):
        with open(self.alerts, 'rb') as alertsFile:
            alertLines = self.follow(alertsFile)
            for line in alertLines:
                self.processLine(line)

    def process(self):
        with open(self.alerts, 'rb') as alertsFile:
            for line in alertsFile:
                self.processLine(line)


    def processDB(self):
        query = "select rowid,* from  logs where status=0";
        cur = get_db().execute(query, [])
        logs = cur.fetchall()
        queries = []
        for log in logs:
            queries.append("update logs set status=1 where rowid=%s;"%(log[0]))
            log = [clean(x) if x else "" for x in log[1:-1]]
            logLine = ','.join(log).replace('"','')
            self.processLine(logLine)