import sqlite3

def get_db():
    db = sqlite3.connect('database.db', timeout=10)
    return db

class Config:

	def __init__(self):
		self.load()
		self.overall = 1
		self.p1_voip = 1
		self.p1_sms = 0
		self.p2_sms = 1
		self.p2_voip = 0
		self.p3_sms = 0
		self.p3_voip = 0

	def notify(self):
		return self.overall == 1

	def isP1SMSEnabled(self):
		return self.p1_sms == 1

	def isP1VoipEnabled(self):
		return self.p1_voip == 1

	def isP2SMSEnabled(self):
		return self.p2_sms == 1

	def isP2VoipEnabled(self):
		return self.p2_voip == 1

	def isP3SMSEnabled(self):
		return self.p3_sms == 1

	def isP3VoipEnabled(self):
		return self.p3_voip == 1


	def load(self):
		try:
			query = "select overall, p1_sms, p1_voip, p2_sms, p2_voip, p3_sms, p3_voip from config";
			cur = get_db().execute(query, [])
			self.overall, self.p1_sms, self.p1_voip, self.p2_sms, self.p2_voip, self.p3_sms, self.p3_voip = cur.fetchall()[0]
		except:
			pass