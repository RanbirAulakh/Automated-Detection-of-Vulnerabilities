from Utilities.Requests import Requests
from Utilities.File import File

class PassiveSQLInjection(object):

	"""
		This open the passive sql vectors file and loop through all
		links object to see which link is vulnerable to passive sql injection
	"""

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
		vectors = self.file.getPassiveSQLInjectionVector()

		if self.links:
			for link in links:
				payload = {}
				url = link.getUrl()
				inputs  = link.getInputs()

				#prepare to load our attack vector in the empty inputs
				for vector in vectors:
					for input_tag in inputs:
						if input_tag:
							name = input_tag.get('name')
							value = input_tag.get('value')

							if not value:
								value = vector

							payload[name] = value

					
					#submit the payload with the injected value
					query = self.request.post(url,data=payload)
					#print(query.text)

					if "syntax" in query.text.lower():
						print("SQL INJECTION VULNERABILITY FOUND")
						print(payload)

					#try get
					query = self.request.get(url,data=payload)

					if "syntax" in query.text.lower():
						print("SQL INJECTION VULNERABILITY FOUND")
						print(payload)
				

			