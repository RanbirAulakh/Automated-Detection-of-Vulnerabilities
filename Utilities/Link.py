from Utilities import Input

class Link(object):

    """
    This is the link object that contain information about a link such as
    url, input parameters and page content
    """

    def __init__(self):
        self.url = None
        self.inputs = []
        self.content = None

    def getInputs(self):
        return self.inputs

    def addInput(self,input):
        self.inputs.append(input)

    def getUrl(self):
        return self.url

    def addUrl(self,url):
        self.url = url

    def addContent(self,content):
        self.content = content

    def getContent(self):
        return self.content





