import requests


class Request(object):
    request = None

    def __init__(self):
        self.request = requests.session()

    def request(self):
        return self.request