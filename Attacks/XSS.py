from Utilities.Requests import Requests
from Utilities.File import File

class XSS(object):
	
	def __init__(self, request):
		self.file = File()
		self.request = request
		
		
	#Takes in list of inputs that can be modified to store information
	def attackStored(self, links):
		self.links = links
		print("TESTING STORED XSS ATTACK")
		#self.forms = forms
		if self.links:
			for link in self.links:
				testScript = "<script>alert(123)</script>"
				url = link.getUrl()
				inputs = link.getInputs()
				payload = {}
				
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
				print(payload)
				query = self.request.post(url,data=payload)
				print(query.url)
                
				#Check for script execution? 
				print(query.text)
				if testScript in query.text.lower():
					print("XSS Stored Vulnerability found")
		return
        
	def attackReflect(self, links):
		print("TESTING REFLECTED XSS ATTACK")
		self.links = links
		
		#Load in examples of XSS scripts from some file, much like the Active SQL
		#This is stored in as vectors? Similar to ActiveSQLInjection
		
		if self.links:
			for link in self.links:
				testScript = "<script>alert(123)</script>"
				url = link.getUrl()
				inputs = link.getInputs()
				payload = {}
				
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
				print(payload)
				query = self.request.post(url,data=payload)
				print(query.url)
                
				#Check for script execution? 
				#print(query.text)
				if testScript in query.text.lower():
					print("XSS Reflected Vulnerability found")
            
				#Check result of running this on website, what do we get back?
				#We'll just match with whatever value we sent in, if we get it back,
				#then the script ran.
				#print(query.text.lower())
			
			
			
