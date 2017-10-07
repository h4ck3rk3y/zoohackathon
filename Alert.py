# Models an alert

class Alert:

	def __init__(self, sensor, sensor_id, time_reported, date_reported, location, label=""):
		self.sensor = sensor
		self.sensor_id = sensor_id
		self.time_reported = time_reported
		self.date_reported = date_reported
		self.location = location
		self.label = label

	def isHighLevelAlert(self):
		if "intruder".lower() in self.label.lower():
			return True
		return False

	def message(self):
		return "%s-%s %s-%s at %s with label %s"%(self.sensor, self.sensor_id, self.date_reported, self.time_reported, self.location, self.label)

	def ranger(self):
		return "+447526704419"