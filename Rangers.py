from functools import partial
from collections import defaultdict
import csv
import sqlite3

def get_db():
    db = sqlite3.connect('database.db', timeout=10)
    return db

class Rangers:

	def __init__(self, rangersFile="Rangers.csv"):
		self.rangersFile = rangersFile
		self.rangers = defaultdict(list)
		self.rangerPos = []
		self.load()

	def load(self):
		with open(self.rangersFile, 'rb') as rfile:
			rangerReader = csv.reader(rfile, delimiter=',', quotechar='|')
			for row in rangerReader:
				self.rangers[(float(row[0]), float(row[1]))].append({'name': row[2], 'number': row[3]})
		self.rangerPos = self.rangers.keys()

	def findClosest(self, listOfRangers, ranger):
		dist=lambda s,d: (s[0]-d[0])**2+(s[1]-d[1])**2
		return min(listOfRangers, key=partial(dist, ranger))

	def whoToCall(self, alerLoc):
		pair = self.findClosest(self.rangerPos, alerLoc)
		return self.rangers[pair][0]

	def whoToCallDB(self, alerLoc):
		query = "select * from rangers"
		cur = get_db().execute(query, [])
		rangersDB = cur.fetchall()
		rangers = defaultdict(list)
		for row in rangersDB:
			rangers[(float(row[0]), float(row[1]))].append({'name': row[2], 'number': row[3]})
		if rangers:
			pos = rangers.keys()
			pair = self.findClosest(pos, alerLoc)
			return rangers[pair][0]
		else:
			return self.whoToCall(alerLoc)