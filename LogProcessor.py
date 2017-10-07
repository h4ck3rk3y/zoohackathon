import csv
import time

from Alert import Alert
from TwilioClient import TwilioClient
from Rangers import Rangers

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
        sensor, sensor_id, time_reported, date_reported, location, label = line.split(',')
        alert = Alert(sensor, sensor_id, time_reported, date_reported, location, label)
        whoToCall = self.rangers.whoToCall(alert.location)['number']

        if alert.isHighLevelAlert():
            self.client.makeCall(whoToCall)
        else:
            self.client.sendMessage(whoToCall, alert.message())

    def processContinously(self):
        with open(self.alerts, 'rb') as alertsFile:
            alertLines = self.follow(alertsFile)
            for line in alertLines:
                self.processLine(line)

    def process(self):
        with open(self.alerts, 'rb') as alertsFile:
            for line in alertsFile:
                self.processLine(line)