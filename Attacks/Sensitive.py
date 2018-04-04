from Utilities.File import File
from collections import defaultdict
import logging

class Sensitive(object):
    """
    Check to see if there is any sensitive configuration files such as phpinfo, config.ini, etcetera.
    """

    def __init__(self, links):
        self.links = links
        self.file = File()
        self.sensitive = defaultdict(list)
        self.vectors = self.file.getSensitiveVector()

    def sensitve_information_disclosure(self,vector,content):
        """
        It checks fot the content, if sensitive word exist in the
        contents, it could be a breach...
        :param vector: URLS
        :param content: website page
        :return: if there is any information disclosed
        """
        if content and vector:
            vector = vector.strip().lower()
            content = content.strip().lower()

            if vector in content:
                return True

        return False


    def search(self):
        """
        Search for sensitive keywords in a page
        :return: None
        """
        if self.links and self.vectors:

            for link in self.links:
                url = link.getUrl().strip().lower()
                content = link.getContent().strip().lower()

                # go through all sensitive vector and see if any is disclosured
                for vector in self.vectors:
                    vector = vector.strip().lower()
                    #disclosured in the html content?
                    if self.sensitve_information_disclosure(vector,content):
                        msg = vector + " appeared in the html content of "+url
                        self.sensitive[vector].append(msg)

                    #disclosured in the url itself? example.config.php
                    if self.sensitve_information_disclosure(vector,url):
                        msg = vector + " appeared in the url of "+url
                        self.sensitive[vector].append(msg)


    def display_sensitive_search_result(self):
        """
        Displays the results
        :return: None
        """
        if self.sensitive:
            logging.info("Potential Sensitive breached result")
        for breach in self.sensitive:
            logging.info("Below are the vector breach: " + breach)
            for loc in self.sensitive.get(breach):
                logging.info(loc)

        return self.sensitive




