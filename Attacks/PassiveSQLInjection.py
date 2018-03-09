from Utilities.Requests import Requests
from Utilities.File import File

class PassiveSQLInjection(object):

	def __init__(self,request):
		self.file = File()
		self.request = request


	def attack(self,links):
		print("TESTING PASSIVE SQL")
		"""
		This function will attempt to perform the active sql injection
		:param links: a LINK class object with the inputs being an instance of beautiful soup
		:return:
		"""
		self.links = links
		vectors = self.file.getActiveSQLInjection()

		if self.links:
			for link in self.links:
				url = link.getUrl()
				inputs = link.getInputs()
				payload = {}
				for vector in vectors:
					for input in inputs:
						if input:
							name = input.get('name')
							value = input.get('value')

							#if it has no value, give it the sql injection vector value
							if not value:
								value = vector

							payload[name] = value

					#submit and test
					print(payload)
					query = self.request.post(url,data=payload)

					if "sql syntax" in query.text.lower():
						print("SQL INJECTION VULNERABILITY FOUND")
						print(payload)
						exit()