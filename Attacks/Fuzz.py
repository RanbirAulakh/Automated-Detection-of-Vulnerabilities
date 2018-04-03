from Utilities.Link import  Link
from bs4 import BeautifulSoup
import re, logging
from url_normalize import url_normalize

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
        self.externalLinks = []
        self.internalLinks = []
        self.limit = 50

        self.tags = {
            "a": "href",
            "img": "src",
            "form": "action",
            "script": "src",
            "iframe": "src",
            "div": "src",
            "frame": "src",
            "embed": "src",
            "link": "href",
        }

        self.domain = None

    def display_msg_and_terminate(msg):
        if not msg:
            logging.error("You must supply a error message")
        
        else:
            logging.info(msg)

        exit()

    def set_beautiful_soup(self,text):
        if not text:
            self.display_msg_and_terminate("You must supply an text for the beautiful soup!")
        self.soup = BeautifulSoup(text,self.parser)

    def validate_url(self,url, msg="You must supply an url!"):
        if not url:
            self.display_msg_and_terminate(msg)

        try:
            query = self.browser.get(url)
            status = query.status_code
            if status!=200:
                err = "The url "+ url + " returned status code "+ status +". Program terminated"
                self.display_msg_and_terminate(err)
        except:
            err = "An error occured, ensure that you supplied an valid url and that the url you supplied is reachable"
            self.display_msg_and_terminate(err)


    def discover(self,url,limit=50):
        #ensure only valid url are allowed
        self.validate_url(url)
        self.domain = url
        self.toCrawl.append(url)

        self.crawler(url,limit)

    def return_path_last_directory(self,url):
        if url:
            length = url.count('/')
            if  length > 0:
                directory = ""
                count = 0
                for char in url:
                    directory+=char
                    if char=="/":
                        count+=1

                    if count==length:
                        break

                return directory



    def crawler(self,url,limit=50):
        logging.info("Fuzz/Crawling...")
        self.validate_url(url) #the very first url must be a valid url
        prevCrawled = url
        count = 0

        while self.toCrawl and count<limit:
            
            #crawler is restrict to only crawl internal links
            if url not in self.crawled:
                self.crawled.append(url)
                if self.domain in url:
                    response = self.browser.get(url)
                    if response.status_code == 200:
                        #make the redirect link also go to the list of link to visited if any
                        if response.url not in self.crawled:
                            self.toCrawl.append(response.url)
                        #make directory visitable too
                        linkObject = Link()
                        linkObject.addUrl(url)
                        content = response.text
                        linkObject.addContent(content)

                        #get all inputs we can parameters
                        for input in self.parse_inputs(content):
                            linkObject.addInput(input)
                        self.links.append(linkObject)


                        #get the links we can find from this page
                        for tag in self.tags:
                            elements = self.soup.find_all(tag)
                            if elements:
                                for element in elements:
                                    link = element.get(self.tags.get(tag))
                                    if link:
                                        directoryParentChecked = False
                                        prevToggled = False
                                        while not directoryParentChecked:
                                            if prevToggled:
                                                directoryParentChecked = True
                                            canonicalize_url = self.canonicalize_url(link,prevCrawled)
                                            if canonicalize_url:
                                                link = canonicalize_url
                                            
                                            
                                            normalize = url_normalize(link)
                                            if normalize:
                                                link = normalize
                                            


                                            if link not in self.toCrawl and '#' not in link and link not in self.crawled and "logout" not in link.lower():
                                                self.toCrawl.append(link)

                                            if not directoryParentChecked:
                                                prevCrawled = self.return_path_last_directory(url)
                                                prevToggled = True

                        #record the internal links(we are only interested in the success links)
                        if self.is_internal_link(url) and url not in self.internalLinks:
                            logging.info(url + " --> " + str(200))
                            self.internalLinks.append(url)

                #record the external links
                if url not in self.externalLinks and not self.is_internal_link(url):
                    try:
                        check = self.browser.get(url)
                        if check.status_code == 200:
                            self.externalLinks.append(url)
                    except:
                        pass
                    


            #we are done with the recently crawled link so remove it
            self.toCrawl.remove(url)
            prevCrawled = url
            if self.toCrawl:
                url = self.toCrawl[0]

            count+=1

        #print(self.links)

    def is_internal_link(self,url):
        return self.domain in url

    def canonicalize_url(self,link,parentUrl):
        if not link:
            self.display_msg_and_terminate("You must supply an link to use the canonicalize_url function")

        if 'https://' not in link and 'http://' not in link:
            if link.startswith('/'):
                link = link[1:]

            link = parentUrl+"/"+link

        return link


    def print_discovered_links(self):

        logging.info("Internal Links")
        for internal in self.internalLinks:
            logging.info(internal)

        logging.info("\nExternal Links")
        for external in self.externalLinks:
            logging.info(external)

    def parse_inputs(self,text):
        self.set_beautiful_soup(text)
        return self.soup.find_all('input')

    def get_fuzz_links(self):
        return self.links












