from Utilities.Requests import Requests
from Utilities.File import File

class XSS(object):
	
	def __init__(self, request):
		self.file = File()
		self.request = request
		
		
	#Takes in list of inputs that can be modified to store information
	def attackStored(self, forms):
		self.forms = forms
		#for form in forms:
			#Iterate through all possible forms using test inputs to see if we get a reaction. This is a bit harder to automate, as we have to update the page and check for specific reactions.
		return
        
	def attackReflect(self, links):
		print("TESTING REFLECTED XSS ATTACK")
		self.links = links
		
		#Load in examples of XSS scripts from some file, much like the Active SQL
		#This is stored in as vectors? Similar to ActiveSQLInjection
		
		if self.links:
			for link in self.links:
				url = link.getUrl()
				inputs = link.getInputs()
				payload = {}
				
				#Attempt to find something in all URLs that we can inject a script into
				for input in inputs:
					if input:
						name = input.get('name')
						value = input.get('value')
						
						if not value:
							#Set some default value 
							value = "<script>alert(123)</script>"
							
						payload[name] = value
				
				#Submit and test payload
				print(payload)
				query = self.request.post(url,data=payload)
				
				#Check result of running this on website, what do we get back?
				#How do we determine the script ran?
				print(type(query))
				print(query.text.lower())
			
			
