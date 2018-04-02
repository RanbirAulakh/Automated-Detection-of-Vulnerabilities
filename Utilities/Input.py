class Input(object):
    """
    Gets the Input form, returns the name, value, and the method
    """

    method = None

    def __init__(self,name,value,method=None):
        self.name = name
        self.value = value

        if method:
            method = method.lower()

            if method is "post" or method is "get":
                self.method = method

    def getName(self):
        """
        Get the name of the inputs
        :return: name
        """
        return self.name

    def getValue(self):
        """
        Get the value of the inputs
        :return: value
        """
        return self.value

    def getMethod(self):
        """
        Get the method of the inputs
        :return: method
        """
        return self.method
