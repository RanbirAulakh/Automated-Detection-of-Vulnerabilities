from Attacks.Fuzz import Fuzzer
from Utilities.Requests import Requests
from Attacks.ActiveSQLInjection import  ActiveSQLInjection
from Attacks.PassiveSQLInjection import PassiveSQLInjection
from Attacks.XSS import XSS
from timeit import default_timer as timer
from Attacks.BruteForce import BruteForce
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

""""
    PERFORM A UNIT TEST ON BRUTE FORCE, ACTIVE AND PASSIVE SQL
"""


url = "http://localhost/dvwa/login.php"



request = Requests()
request = request.request
start = timer()

b = BruteForce(url, request)
flag, username, password, url = b.startBruteForce()

end = timer()

url = 'http://localhost/dvwa/vulnerabilities/sqli/'
fuzz = Fuzzer(request)
fuzz.discover(url)


activeSql = ActiveSQLInjection(request)
activeSql.attack(fuzz.get_fuzz_links())
"""
passiveSql = PassiveSQLInjection(request)
passiveSql.attack(fuzz.get_fuzz_links())"""

print("")

#url = 'http://localhost/dvwa/vulnerabilities/xss_r/?name=<script>alert(123)<%2Fscript>#'
url = 'http://localhost/dvwa/vulnerabilities/xss_r/'


xfuzz = Fuzzer(request)
xfuzz.discover(url)

xss = XSS(request)
xss.attackReflect(xfuzz.get_fuzz_links())

url = 'http://localhost/dvwa/vulnerabilities/xss_s/'
xrfuzz = Fuzzer(request)
xrfuzz.discover(url)

sxss = XSS(request)
sxss.attackStored(xrfuzz.get_fuzz_links())
