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

        self.extensions = {
            ".php",
            ".js",
            ".php3",
            ".shtml",
            ".shtm",
            ".asp"
            ".asp.net",
            ".cfm",

        }

        self.domain = None

    def display_msg_and_terminate(self,msg):
        if not msg:
            logging.error("You must supply a error message")
        
        else:
            logging.info(msg)

        exit()

    def set_beautiful_soup(self,text):
        """
        Store HTML content
        :param text: HTML content
        :return: None
        """
        if not text:
            self.display_msg_and_terminate("You must supply an text for the beautiful soup!")
        self.soup = BeautifulSoup(text,self.parser)

    def validate_url(self,url, msg="You must supply an url!"):
        """
        Validate the URL
        :param url: website URL
        :param msg: error message if any
        :return: None
        """
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
        """
        Limit # links to crawl
        :param url: website URL
        :param limit: # of links
        :return: None
        """
        #ensure only valid url are allowed
        self.validate_url(url)
        self.domain = self.strip_index(url)
        self.toCrawl.append(url)

        self.crawler(url,limit)

    def return_path_last_directory(self,url):
        """
        Returns path last directory
        :param url: website URL
        :return: path last directory
        """
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
        """
        Crawl and search for all possible links and search if there
        are any input fields within that page
        :param url: website url
        :param limit: # of links to crawl
        :return: None
        """
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
                            logging.debug(url + " --> " + str(200))
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

    def strip_index(self,url):
        """
        Strips the index
        :param url: website URL
        :return: website URL
        """
        for ext in self.extensions:
            index = "index"+ext
            index = index.lower()
            url = url.lower()

            if index in url:
                url = url.replace(index,"")

        return url


    def is_internal_link(self,url):
        """
        Check to see if its an internal link
        :param url: website url
        :return: bool
        """
        return self.domain in url

    def canonicalize_url(self,link,parentUrl):
        """
        Normalize the URLs
        :param link: website URL
        :param parentUrl: main domain
        :return: link
        """
        if not link:
            self.display_msg_and_terminate("You must supply an link to use the canonicalize_url function")

        if 'https://' not in link and 'http://' not in link:

            #clean up the parent link if need
            parentUrl = self.strip_index(parentUrl)

            if link.startswith('/'):
                link = link[1:]

            link = parentUrl+"/"+link

        return link


    def print_discovered_links(self):
        """
        Prints out the results
        :return: None
        """
        logging.debug("Internal Links")
        for internal in self.internalLinks:
            logging.debug(internal)
        logging.info("# of Internal Links: " + str(len(self.internalLinks)))

        logging.debug("\nExternal Links")
        for external in self.externalLinks:
            logging.debug(external)
        logging.info("# of External Links: " + str(len(self.externalLinks)))

    def parse_inputs(self,text):
        """
        Parse Inputs
        :param text: HTML content
        :return: list of inputs
        """
        self.set_beautiful_soup(text)
        return self.soup.find_all('input')

    def get_fuzz_links(self):
        """
        Get Fuzz Links
        :return: Fuzz Links
        """
        return self.links












