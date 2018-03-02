import requests

class Requests(object):
    request = None

    def __init__(self):
        self.request = requests.Session()

    def request(self):
        return self.request