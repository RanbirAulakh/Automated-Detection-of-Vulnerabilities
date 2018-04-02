from Attacks.Fuzz import Fuzzer
from Utilities.Requests import Requests
from Attacks.ActiveSQLInjection import  ActiveSQLInjection
from Attacks.PassiveSQLInjection import PassiveSQLInjection
from timeit import default_timer as timer
from Attacks.BruteForce import BruteForce
from Utilities import Link
from Attacks.crawler import Crawl

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
"""
start = timer()
b = BruteForce(url, request)
flag, username, password, url = b.startBruteForce()
end = timer()
"""

# url = 'http://localhost/dvwa/vulnerabilities/brute/'
url = "https://hostjams.com"
#url="https://hostjams.com"
fuzz = Fuzzer(request)
#fuzz.restrict_domain(url)
fuzz.discover(url)
fuzz.print_discovered_links()



"""
activeSql = ActiveSQLInjection(request)
activeSql.attack(fuzz.get_fuzz_links())

passiveSql = PassiveSQLInjection(request)
passiveSql.attack(fuzz.get_fuzz_links())
"""