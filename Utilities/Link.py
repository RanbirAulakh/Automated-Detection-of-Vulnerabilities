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
        """
        Get Inputs
        :return: return list of inputs
        """
        return self.inputs

    def addInput(self,input):
        """
        Add Inputs to the list
        :param input: inputs
        :return: None
        """
        self.inputs.append(input)

    def getUrl(self):
        """
        Get URL
        :return: returns URL
        """
        return self.url

    def addUrl(self,url):
        """
        Set URL
        :param url: URL
        :return: None
        """
        self.url = url

    def addContent(self,content):
        """
        Set current webpage content
        :param content: webpage content
        :return: None
        """
        self.content = content

    def getContent(self):
        """
        Get webpage content
        :return: webpage content
        """
        return self.content





