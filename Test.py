from Attacks.Fuzz import Fuzzer
from Utilities.Requests import Requests
from Utilities import Link

# import requests
# import Link.Link as LinkClass
#
# r = requests.get("URL")
#
# link = LinkClass.Link()
#
#
#
#
#
# print(r.text)


url = "http://hostjams.com"
request = Requests()
request = request.request
fuzz = Fuzzer(request)
fuzz.discover(url)