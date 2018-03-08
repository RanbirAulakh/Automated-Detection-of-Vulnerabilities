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

    def addInput(self,input):
        self.inputs.append(input)

    def addContent(self,content):
        self.content = content

    def getInputs(self):
        return self.inputs

    def getContent(self):
        return self.content

    def getUrl(self):
        return self.url


