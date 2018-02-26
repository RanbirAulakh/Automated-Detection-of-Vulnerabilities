class Input(object):

    method = None

    def __init__(self,name,value,method=None):
        self.name = name
        self.value = value

        if method:
            method = method.lower()

            if method is "post" or method is "get":
                self.method = method

    def getName(self):
        return self.name

    def getValue(self):
        return self.value

    def getMethod(self):
        return self.method
