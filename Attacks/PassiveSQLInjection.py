from Utilities.Requests import Requests
from Utilities.File import File
import logging

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
		self.inject_vulnerabilities_list = []


	def attack(self,links):
		"""
		This function will attempt to perform the active sql injection
		:param links: a LINK class object with the inputs being an instance of beautiful soup
		:return: None
		"""

		logging.info("Executing Passive SQL Injection...")

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

						#not a get based but go ahead and try if we can get vul this way either
						self.has_sql_injection_vulnerability(payload,url,"get")


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
									parameters = parameters.append(attributes)

								if parameters:
									for p in parameters:
										attributes = p.split("=")
										name = attributes[0]
										
										payload[name] = vector


									self.has_sql_injection_vulnerability(payload,url,"get")
								

	def is_get_based_url(self,url):
		"""
		Check to see if there is any PHP "characters" in URL
		:param url: website URL
		:return: bool
		"""
		if not url:
			return False

		url = url.strip().lower()
		if "?" in url:
			return True

		return False

	def has_sql_injection_vulnerability(self,payload,url,method="post",skip_login=True):
		"""
		Check to see if SQL injection exists
		:param payload: POST/GET data
		:param url: website URL
		:param method: form
		:param skip_login: if still on login page
		:return: if sql injection is successful
		"""
		if not url or not method:
			logging.error("The parameter method and payload cannot be empty!")
			exit()

		method = method.lower().strip()

		if method!="post" and method!="get":
			logging.error("the parameter method must be get or post")
			exit()

		if not payload:
			return False

		if skip_login and "login" in url.lower():
			return False

		if method=="post":
			query = self.request.post(url,data=payload)
		else:
			query = query = self.request.get(url,data=payload)

		if not query:
			return False

		res = query.text.strip().lower()

		if res:
			for err in self.sql_errors:
				err = err.strip().lower()
				if err in res:
					vul = "url:"+url+"\npayload:"+str(payload)
					self.inject_vulnerabilities_list.append(vul)
					return True

		return False


	def make_post_payload(self,payload,inputs,vector):
		"""
		Execute POST data to website
		:param payload: POST/GET data
		:param inputs: form inputs fields
		:param vector: urls
		:return: POST/GET data
		"""
		if inputs:
			for input_tag in inputs:
				name = input_tag.get('name')
				value = input_tag.get('value')

				if not value:
					value = vector

				payload[name] = value

		return payload


	def sql_injection_result(self):
		"""
		Prints out the results
		:return: list of results
		"""
		if self.inject_vulnerabilities_list:
			logging.info("Found "+ str(len(self.inject_vulnerabilities_list)) + " passive sql injection potientials")
			for vul in self.inject_vulnerabilities_list:
				logging.debug(vul)
			
		return self.inject_vulnerabilities_list
