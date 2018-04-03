from Attacks.Fuzz import Fuzzer
from Utilities.Requests import Requests
from Attacks.ActiveSQLInjection import  ActiveSQLInjection
from Attacks.PassiveSQLInjection import PassiveSQLInjection
from Attacks.XSS import XSS
from timeit import default_timer as timer
from Attacks.BruteForce import BruteForce
from Utilities import Link
from Attacks.Sensitive import Sensitive
import logging

logging.basicConfig(format="%(asctime)s - %(levelname)s %(message)s", level = logging.INFO)


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

request = Requests()
request = request.request
url = "http://localhost/dvwa"
b = BruteForce(url, request)
flag, username, password, url = b.startBruteForce()

fuzz = Fuzzer(request)
#fuzz.restrict_domain(url)
fuzz.discover(url)
fuzz.print_discovered_links()

links = fuzz.get_fuzz_links()

"""
p_sql = PassiveSQLInjection(request)
links = fuzz.get_fuzz_links()
p_sql.attack(links)
"""

sensitive = Sensitive(links)
sensitive.search()







