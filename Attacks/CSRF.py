import logging

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
		self.user_defined_token = None
		self.vuln_inputs = []
		self.vuln_urls = []

	def add_token(self,token):
		"""
		Add tokens to the list
		:param token: CSRF token
		:return: None
		"""
		if not token:
			logging.error("Token cannot be empty!")
			exit()

		self.user_defined_token = token.lower()

	def scan(self):
		"""
		Go through every webpage (links) and uses has_csrf_token to scan
		if there is any CSRF protection in webpage
		:return: None
		"""
		if self.links:
			logging.info("Scanning for CSRF Protection...")
			for link in self.links:
				#only focus on those that have input parameters
				inputs = link.getInputs()
				url = link.getUrl().strip()
				if inputs:
					content = ""
					for input_tag in inputs:
						name = input_tag.get("name")
						if name:
							content+=name

					if content:
						content = content.lower().strip()
						self.has_csrf_token(content,url)

				#get based url?
				if "?" in url:
					url = url.lower()
					self.has_csrf_token(url,url,False)



	def has_csrf_token(self,content,url,is_input=True):
		"""
		Checks to see if CSRF is missing
		:param content: webpage HTML
		:param url: website URL
		:param is_input: check if there is inputs
		:return: None
		"""
		if content:
			protected = False
			content = content.strip()
			for token in self.tokens:
				token = token.lower().strip()
				if token in content or token in self.user_defined_token:
					protected = True
			
			if not protected:
				if is_input:
					vul = "inputs at "+url+ " is missing csrf token"
					if vul not in self.vuln_inputs:
						self.vuln_inputs.append(vul)
				else:
					vul = "the url "+url+" parameters is missing csrf token"
					if vul not in self.vuln_urls:
						self.vuln_urls.append(vul)


	def csrf_protection_result(self):
		"""
		CSRF results
		:return: CSRF results
		"""
		if self.vuln_urls or self.vuln_inputs:
			logging.info("Found "+ str(len(self.vuln_inputs) + len(self.vuln_urls)) + " potiential issue due to no csrf protection")
			
			for vul in self.vuln_inputs:
				logging.debug(vul)
			for vul in self.vuln_urls:
				logging.debug(vul)

		return self.vuln_urls, self.vuln_inputs