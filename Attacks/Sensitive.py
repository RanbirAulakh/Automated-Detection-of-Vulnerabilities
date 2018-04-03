from Utilities.File import File
class Sensitive(object):

    def __init__(self, links):
        self.links = links
        self.file = File()
        self.sensitive = None
        self.vectors = self.file.getSensitiveVector()



    def search(self):
    	if self.links and self.vectors:

    		for link in self.links:
    			url = link.getUrl()
    			content = link.getContent()
    			for vector in self.vectors:
    				if vector in url:
    					print("match")


