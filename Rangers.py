from scipy import spatial
from collections import defaultdict
import csv
import sqlite3

def get_db():
    db = sqlite3.connect('database.db', timeout=10)
    return db

class Rangers:

	def __init__(self, rangersFile="Rangers.csv.bk"):
		self.rangersFile = rangersFile
		self.rangers = defaultdict(list)
		self.rangerPos = []
		self.kdtree = []
		self.load()

	def load(self):
		with open(self.rangersFile, 'rb') as rfile:
			rangerReader = csv.reader(rfile, delimiter=',', quotechar='|')
			for row in rangerReader:
				self.rangers[(float(row[0]), float(row[1]))].append({'name': row[2], 'number': row[3]})
		self.rangerPos = self.rangers.keys()
		self.kdtree = spatial.KDTree(self.rangerPos)

	def whoToCall(self, alerLoc):
		distance, index = self.kdtree.query(alerLoc)
		pair = self.rangerPos[index]
		return self.rangers[pair][0]

	def whoToCallDB(self, alerLoc):
		query = "select * from rangers"
		cur = get_db().execute(query, [])
		rangers = cur.fetchall()
		rangers = defaultdict(list)
		for ranger in rangers:
			rangers[(float(row[0]), float(row[1]))].append({'name': row[2], 'number': row[3]})
		pos = rangers.keys()
		kdtree = spatial.kdtree(pos)
		distance, index = kdtree.query(alerLoc)
		pair = pos[index]
		return rangers[pair][0]