class CSRF(object):

	links = None

	def __init__(self,links):
		self.links = links
		self.tokens= {
			"csrftoken",
			"token",
			"csrf-token",
			"csrf_token",
			"XSRF-TOKEN",
			"X-XSRF-TOKEN",
			"csrf_protection",
			"X-CSRF-Token"
		}
		self.vuln_inputs = []
		self.vuln_urls = []

	def add_token(self,token):
		if not token:
			print("Token cannot be empty!")
			exit()

		self.tokens.append(token)

	def scan(self):
		if self.links:
			print("Scanning for csrf protection")
			for link in self.links:
				#only focus on those that have input parameters
				inputs = link.getInputs()
				url = link.getUrl().strip()
				if inputs:
					content = link.getContent()
					if content:
						content = content.lower().strip()
						self.has_csrf_token(content,url)

				#get based url?
				if "?" in url:
					url = url.lower()
					self.has_csrf_token(url,url,False)



	def has_csrf_token(self,content,url,is_input=True):
		if content:
			content = content.strip()
			for token in self.tokens:
				token = token.lower().strip()
				if token not in content:
					if is_input:
						vul = "inputs at "+url+ " is missing csrf token"
						if vul not in self.vuln_inputs:
							self.vuln_inputs.append(vul)
					else:
						vul = "the url "+url+" parameters is missing csrf token"
						if vul not in self.vuln_urls:
							self.vuln_urls.append(vul)


	def csrf_protection_result(self):
		if self.vuln_urls or self.vuln_inputs:
			print("Found "+str(len(self.vuln_inputs) + len(self.vuln_urls)) + " potiential issue due to no csrf protection")
			
			for vul in self.vuln_inputs:
				print(vul)
			for vul in self.vuln_urls:
				print(vul)

