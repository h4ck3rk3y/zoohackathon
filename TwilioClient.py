from twilio.rest import TwilioRestClient
from keys import *


class TwilioClient:

	def __init__(self, from_number=FROM_NUMBER, auth_token=AUTH_TOKEN, auth_sid=AUTH_SID):
		self.client = TwilioRestClient(auth_sid, auth_token)
		self.from_number = from_number

	def sendMessage(self, receiver, message):
		message = self.client.messages.create(self.from_number, body=message, to=receiver)