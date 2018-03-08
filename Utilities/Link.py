from Utilities import Input

class Link(object):

    def __init__(self):
        self.url = None
        self.inputs = []
        self.content = None

    def getInputs(self):
        return self.inputs

    def getUrl(self):
        return self.url

    def addUrl(self,url):
        self.url = url


    def addContent(self,content):
        self.content = content

    def getContent(self):
        return self.content



