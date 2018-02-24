class Sensitive(object):

    def __init__(self, request):
        self.content = None
        self.sensitive = None
        self.link = None
        self.request = request

    def setLink(self, link):
        self.link = link
