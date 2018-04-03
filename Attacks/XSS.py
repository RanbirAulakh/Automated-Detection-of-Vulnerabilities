from Utilities.Requests import Requests
from Utilities.File import File
import logging

class XSS(object):
	
	def __init__(self, request):
		self.file = File()
		self.request = request
		
		
	#Takes in list of inputs that can be modified to store information
	def attackStored(self, links):
		"""
		Go through every form on links given, then execute malicious code.
		:param links: website URL
		:return: vulnerability found
		"""
		self.links = links
		logging.info("Performing stored XSS attack")
		vectors = self.file.getXSSScripts()
		#self.forms = forms
		if self.links:
			for link in self.links:
				#testScript = "<script>alert(123)</script>"
				url = link.getUrl()
				inputs = link.getInputs()
				payload = {}
				for vector in vectors:
					#print(vector)
					#Attempt to find something in all URLs that we can inject a script into
					for input in inputs:
						if input:
							name = input.get('name')
							value = input.get('value')
						
							if not value:
								value = vector

							payload[name] = value
				
				
					#Submit and test payload
					logging.debug(payload)
					query = self.request.post(url,data=payload)
					#print(query.url)
					#Check to see if the script was stored in html as-is without sanitization
					if vector.rstrip() in query.text.lower():
						logging.info("XSS Stored Vulnerability found!")
						return 1
		logging.info("No vulnerability in XSS stored!")
		return 0
        
	def attackReflect(self, links):
		"""
		Go through every form on links given, then execute malicious code.
		:param links: website URL
		:return: vulnerability found
		"""
		logging.info("Performing reflect XSS attack")
		self.links = links
		vectors = self.file.getXSSScripts()
		#Load in examples of XSS scripts from some file, much like the Active SQL
		#This is stored in as vectors? Similar to ActiveSQLInjection
		
		if self.links:
			for link in self.links:
				testScript = "<script>alert(123)</script>"
				url = link.getUrl()
				inputs = link.getInputs()
				payload = {}
				
				for vector in vectors:
				
					#Attempt to find something in all URLs that we can inject a script into
					for input in inputs:
						if input:
							name = input.get('name')
							value = input.get('value')
						
							if not value:
								value = testScript
							#Set some default value 
						#value = "<script>alert(123)</script>"
							
							payload[name] = value
				
				#Submit and test payload
					logging.debug(payload)
					query = self.request.post(url,data=payload)
					logging.debug(query.url)
				#Check for script execution? 
				#print(query.text)
					if testScript.rstrip() in query.text.lower():
						logging.info("XSS Reflected Vulnerability found")
						return 1

		logging.info("No vulnerability in XSS reflected!")
		return 0
			
			
