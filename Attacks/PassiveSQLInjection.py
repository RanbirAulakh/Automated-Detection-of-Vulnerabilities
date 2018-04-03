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

		self.sql_errors = {"sql syntax","syntax error","Unclosed quotation mark","Drivers error","Client error","Unknown column"}
		self.vectors = self.file.getPassiveSQLInjectionVector()


	def attack(self,links):
		print("TESTING PASSIVE SQL")
		"""
		This function will attempt to perform the active sql injection
		:param links: a LINK class object with the inputs being an instance of beautiful soup
		:return:
		"""

		if links:
			for link in links:
				payload = {}
				if link.getUrl():
					url = link.getUrl().strip().lower()
					#do we have input?
					inputs = link.getInputs()
					for vector in self.vectors:
						payload = self.make_post_payload(payload,inputs,vector)
						self.has_sql_injection_vulnerability(payload,url)


						#do the get based have a sql vulnerability?
						if self.is_get_based_url(url):
							payload = {}
							fields = url.split("?")

							if fields:
								parameters = []
								url = fields[0]
								attributes = fields[1]

								#multiple attributes?
								if "&" in attributes:
									parameters = attributes.split("&")

								#single attributes
								else:
									parameter = parameter.append(attributes)

								for p in parameter:
									attributes = p.split("=")
									name = attributes[0]
									
									payload[name] = vector


								self.has_sql_injection_vulnerability(payload,url):
								

	def is_get_based_url(self,url):
		if not url:
			return False

		url = url.strip().lower()
		if "?" in url:
			return True

		return False

	def has_sql_injection_vulnerability(self,payload,url,method="post"):
		if not url or not method:
			print("The parameter method and payload cannot be empty!")
			exit()

		method = method.lower().strip()

		if method!="post" and method!="get":
			print("the parameter method must be get or post")
			exit()

		if not payload:
			return False

		if method=="post":
			query = self.request.post(url,data=payload)
		else:
			query = query = self.request.get(url,data=payload)

		if not query:
			return False

		res = query.text.strip().lower()

		if res:
			print(res)
			for err in self.sql_errors:
				err = err.strip().lower()
				if err in res:
					print("SQL injection founded!")
					return True

		return False


	def make_post_payload(self,payload,inputs,vector):
		if inputs:
			for input_tag in inputs:
				name = input_tag.get('name')
				value = input_tag.get('value')

				if not value:
					value = vector

				payload[name] = value

		return payload



			