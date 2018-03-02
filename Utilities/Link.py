import Input.Input as InputClass

class Link(object):

    def __init__(self):
        self.url = None
        self.inputs = []

    def getInputs(self):
        return self.inputs

    def getUrl(self):
        return self.url

    def addUrl(self,url):
        self.url = url

    def addInput(self,input):
        if not isinstance(input,InputClass.Input):
            raise Exception(input + " must be an instance of " + InputClass.Input)
        self.inputs.append(input)

