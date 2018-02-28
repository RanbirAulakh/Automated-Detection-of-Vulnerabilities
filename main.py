import sys
import argparse


from Attacks.BruteForce import BruteForce
from Attacks.PassiveSQLInjection import PassiveSQLInjection
from Attacks.ActiveSQLInjection import ActiveSQLInjection
from Utilities.Requests import Requests

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

	print("URL: " + args.url)
	print("VUL: " + args.vulnerability)


	# awful implementation
	r = Requests()
	r = r.request

	if args.vulnerability is None:
		choicesDescriptions()
	elif args.vulnerability == "ALL":
		pass
	elif args.vulnerability == "BRUTE":
		BruteForce.printTest()
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