from Attacks.Fuzz import Fuzzer
from Utilities.Requests import Requests
from Attacks.ActiveSQLInjection import  ActiveSQLInjection
from Attacks.PassiveSQLInjection import PassiveSQLInjection
from Attacks.XSS import XSS
from timeit import default_timer as timer
from Attacks.BruteForce import BruteForce
from Utilities import Link
from Attacks.Sensitive import Sensitive
from Attacks.CSRF import CSRF
import logging

logging.basicConfig(format="%(asctime)s - %(levelname)s %(message)s", level = logging.INFO)

""""
    PERFORM A UNIT TEST ON BRUTE FORCE, ACTIVE AND PASSIVE SQL
"""

request = Requests()
request = request.request
url = "http://localhost/dvwa"


b = BruteForce(url, request)
flag, username, password, url = b.startBruteForce()

fuzz = Fuzzer(request)
fuzz.discover(url)
fuzz.print_discovered_links()
links = fuzz.get_fuzz_links()

"""
fuzz.print_discovered_links()

links = fuzz.get_fuzz_links()
"""

"""
p_sql = PassiveSQLInjection(request)
links = fuzz.get_fuzz_links()
p_sql.attack(links)

p_sql.sql_injection_result()
"""

"""
sensitive = Sensitive(links)
sensitive.search()
sensitive.display_sensitive_search_result()
"""


a_sql = ActiveSQLInjection(request)
links = fuzz.get_fuzz_links()
a_sql.attack(links)

a_sql.sql_injection_result()

#
# csrf = CSRF(links)
# csrf.scan()
# csrf.csrf_protection_result()







