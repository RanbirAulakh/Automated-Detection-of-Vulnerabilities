from Utilities.Link import  Link
from bs4 import BeautifulSoup
import re
from Utilities.Input import Input
class Fuzzer(object):

    """
        This fuzz a page for all requires information about the page
        and create a link object which can then be used by all attack classes
    """
    guess = False
    browser = None
    links = None

    def __init__(self,browser):
        self.browser = browser
        self.links = []
        self.crawled = []
        self.toCrawl = []
        self.soup = None
        self.parser = 'html.parser'
        self.main = None

    def discover(self, url):
        response = self.browser.get(url)
        self.main = url
        #status code is 200 so we will continue
        if response.status_code:
            self.toCrawl.append(url)
            self.crawler(url)

    def set_beautifulSoup(self,text):
        self.soup = BeautifulSoup(text, self.parser)


    def parse_links(self,text):
        self.set_beautifulSoup(text)
        return self.soup.find_all('a')

    def parse_inputs(self,text):
        self.set_beautifulSoup(text)
        return self.soup.find_all('input')

    def get_fuzz_links(self):
        return self.links


    def crawler(self,url):
        print("CRAWLING")

        response = self.browser.get(url)
        if response.status_code == 200:
            linkObject = Link()
            linkObject.addUrl(url)
            content = response.text
            linkObject.addContent(content)

            #get all inputs
            for input in self.parse_inputs(content):
                linkObject.addInput(input)
            self.links.append(linkObject)





        """
        while self.toCrawl:
            print(url)
            if url not in self.crawled and self.main in url:
                response = self.browser.get(url)
                if response.status_code == 200:
                    self.crawled.append(url)
                    linkObject = Link()
                    linkObject.addUrl(url)
                    content = response.text
                    linkObject.addContent(content)

                    #get all input parameters
                    for input in self.parse_inputs(content):
                        linkObject.addInput(input)
                    self.links.append(linkObject)

                    #get the next links we can find from this page
                    for link in self.parse_links(content):
                        link = link.get('href')
                        if link:
                            if 'https' not in link and 'http' not in link and '#' not in link:
                                if link.startswith('/'):
                                    link = link[1:]
                                link = url + "/"+link

                            if link not in self.toCrawl:
                                self.toCrawl.append(link)

            #we are done with the recently crawled link so remove it
            self.toCrawl.remove(url)
            if self.toCrawl:
                url = self.toCrawl[0]
        """







