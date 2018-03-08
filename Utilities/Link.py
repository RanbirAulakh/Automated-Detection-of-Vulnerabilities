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
<<<<<<< HEAD
=======
        if not isinstance(input,InputClass.Input):
            raise Exception(input + " must be an instance of " + InputClass.Input)
>>>>>>> 1ddd9e4513fb6c8be3c955124bfbde87d767898c
        self.inputs.append(input)

    def addContent(self,content):
        self.content = content

    def getInputs(self):
        return self.inputs

    def getContent(self):
        return self.content

    def getUrl(self):
        return self.url


