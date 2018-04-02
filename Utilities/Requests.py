import requests

class Requests(object):
    request = None

    """
        The request object to be shared across all methods that
        needs it with the session stored
    """

    def __init__(self):
        self.request = requests.Session()

    def request(self):
        """
        Get request cookies, session, any info related to Request
        :return: request page
        """
        return self.request