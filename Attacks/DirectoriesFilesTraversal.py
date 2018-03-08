from bs4 import BeautifulSoup
from Utilities.File import File

class DirectoriesFilesTraversal(object):

	def __init__(self, url, request):
		self.url = url
		self.request = request

	def startScanningDirectoriesFiles(self):
		"""
		Get the textfile, and loop through every possible
		directories and files and append it to URL. 
		If the URL response is 200, that means it's accessible. 
		@args self
		@return list of directories and files that are accessible
		"""
		textfile = File()
		textfile = textfile.getDirectoriesLinks()

		successDirectories = []
		successFiles = []

		print("[INFO] Scanning Directories...")
		for i in textfile:
			url = self.url + "/" + i.strip()
			r = self.request.get(url)

			# 200 means it is successfull and be able to reach the page
			if(r.status_code == 200):
				print("[INFO] Can access " + url)
				successDirectories.append(url)

			# close session
			r = self.request.close()

		print("[INFO] Scanning Files...")
		textfile = File()
		textfile = textfile.getFilesLinks()
		for i in textfile:
			url = self.url + "/" + i.strip()
			r = self.request.get(url)

			# 200 means it is successfull and be able to reach the page
			if(r.status_code == 200):
				print("[INFO] Can access " + url)
				successFiles.append(url)

			# close session
			r = self.request.close()


		return successDirectories, successFiles