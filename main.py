import sys
import argparse

from Attacks.BruteForce import BruteForce
from Attacks.PassiveSQLInjection import PassiveSQLInjection
from Attacks.ActiveSQLInjection import ActiveSQLInjection
from Utilities.Requests import Requests

from timeit import default_timer as timer

def choicesDescriptions():
	return """
Vulnerability supports the following:
	ALL		- Execute All Vulnerabilities
	BRUTE		- Brute Force Every Possible Inputs (LOGIN)
	A-SQL		- Active SQL Injection
	P-SQL		- Passive SQL Injection
	XSS		- Cross Site Scripting
	CSRF		- Cross Site Forgery
	"""

def getChoices():
	return ["ALL", "BRUTE", "A-SQL", "P-SQL", "XSS", "CSRF"]


def main():
	parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, epilog=choicesDescriptions())
	parser.add_argument(
	   "-u", '--url', 
	   help='Website you want to attack',
	   required=True
	)
	parser.add_argument(
	   "-v", '--vulnerability', 
	   help='Vulnerabilities Choices. See the choices options below: '+', '.join(getChoices()), metavar='',
	   required=True
	)
	args = parser.parse_args()

	url = args.url
	vul = args.vulnerability


	# awful implementation
	request = Requests()
	request = request.request

	if args.vulnerability is None:
		choicesDescriptions()
	elif args.vulnerability == "ALL":
		# get all possible links


		# brute force login page
		b = BruteForce(url, request)
		flag, username, password, url = b.startBruteForce()

		pass


	elif args.vulnerability == "BRUTE":
		start = timer()
		b = BruteForce(url, request)
		flag, username, password, url = b.startBruteForce()
		end = timer()

		print("\nBRUTE FOCE STATS\n=========")
		print("Cracked? " + str(flag))
		print("URL: " + url)
		print("After Login URL: " + url)
		print("Username: " + username)
		print("Password: " + password)
		print("Score: <Work-In-Progress>")
		print("Security Principles Violation: <Work-In-Progress>")
		print("--- Completed in %.3f ms" % (end - start))

		pass


	elif args.vulnerability == "A-SQL":
		a_sql = ActiveSQLInjection()

		pass
	elif args.vulnerability == "P-SQL":
		p_sql = PassiveSQLInjection()


		pass
	elif args.vulnerability == "XSS":
		pass
	elif args.vulnerability == "CSRF":
		pass



main()