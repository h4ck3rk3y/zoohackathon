from twilio.rest import TwilioRestClient
from keys import FROM_NUMBER, AUTH_SID, AUTH_TOKEN


class TwilioClient:

	def __init__(self, from_number=FROM_NUMBER, auth_token=AUTH_TOKEN, auth_sid=AUTH_SID):
		self.client = TwilioRestClient(auth_sid, auth_token)
		self.from_number = from_number

	def sendMessage(self, receiver, message):
		print "Sending message to %s"%(receiver)
		message = self.client.messages.create(self.from_number, body=message, to=receiver)

	def makeCall(self, receiver):
		print "Making Call to %s"%(receiver)
		self.client.calls.create(to=receiver, from_=self.from_number, url="https://gyani.net/data/zone1.xml", method="GET")