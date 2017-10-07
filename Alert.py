# -*- coding: utf-8 -*-

import utm
import re

class Alert:

	def __init__(self, sensor, sensor_id, time_reported, date_reported, location, label=""):
		self.sensor = sensor
		self.sensor_id = sensor_id
		self.time_reported = time_reported
		self.date_reported = date_reported
		self.location = self.parseLocation(location)
		self.label = label

	def parseLocation(self, location):
		if "UTM" in location:
			utm_, zone, northing, easting = location.split()
			zoneNumber = int(zone[:-1])
			easting = int(easting)
			northing = int(northing)
			zoneChar = zone[-1:]
			lat, lon = utm.to_latlon(northing, easting, zoneNumber, zoneChar)
			return (lat, lon)
		else:
			p = re.compile("\d+\.\d+")
			matches = re.findall(p, location)
			lat = -float(matches[0])
			lon = float(matches[1])
			return (lat, lon)

	def isHighLevelAlert(self):
		if "intruder".lower() in self.label.lower():
			return True
		return False

	def message(self):
		return "%s-%s %s-%s at %s with label %s"%(self.sensor, self.sensor_id, self.date_reported, self.time_reported, self.location, self.label)