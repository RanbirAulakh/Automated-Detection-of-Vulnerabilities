import sys
import argparse
import logging
from Attacks.BruteForce import BruteForce
from Attacks.DirectoriesFilesTraversal import DirectoriesFilesTraversal
from Attacks.PassiveSQLInjection import PassiveSQLInjection
from Attacks.ActiveSQLInjection import ActiveSQLInjection
from Attacks.XSS import XSS
from Attacks.Fuzz import Fuzzer
from Utilities.Requests import Requests
from Utilities.Classification import Classification
from timeit import default_timer as timer
from collections import OrderedDict
from Attacks.Sensitive import Sensitive
from Attacks.CSRF import CSRF

def choicesDescriptions():
	return """
Vulnerability supports the following (multiple vulnerabilities? seperate by comma):
	BRUTE		- Brute Force Every Possible Inputs (LOGIN)
	A-SQL		- Active SQL Injection
	P-SQL		- Passive SQL Injection
	XSS		- Cross Site Scripting
	CSRF		- Cross Site Forgery
	DIR-TRA		- Directories/Files Traversal (Failure to restrict files, folders, and URL access)
	SENSITIVE	- Check for any sensitive data such as web configuration 
	"""

def main():

	parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter, epilog=choicesDescriptions())
	parser.add_argument(
		"-v", '--vulnerability',
		help='Vulnerabilities Choices. See below...',
		metavar='',
		required=True
	)
	parser.add_argument(
	   "-u", '--url', 
	   help='Website you want to attack',
		metavar='',
	   required=True
	)
	# parser.add_argument(
	#    "-f", '--file',
	#    help='Specific textfiles to use for attacking. Otherwise will use defaults.',
	# 	metavar='',
	#    required=False
	# )
	parser.add_argument(
	   "-d", '--debug',
	   help='Enabled Debugging, otherwise Info',
	   required=False,
		action="store_true"
	)
	args = parser.parse_args()

	if args.debug:
		logging.basicConfig(format="%(asctime)s - %(levelname)s %(message)s", level = logging.DEBUG)
	else:
		logging.basicConfig(format="%(asctime)s - %(levelname)s %(message)s", level = logging.INFO)

	url = args.url
	vul = args.vulnerability

	request = Requests()
	request = request.request

	fuzz = Fuzzer(request)

	try:
		fuzz.discover(url)
		fuzz.print_discovered_links()
		links = fuzz.get_fuzz_links()
	except:
		logging.error("Cannot connect to URL!")
		sys.exit(0)

	classification = Classification()
	if vul is None or url is None:
		choicesDescriptions()
		sys.exit(0)

	boolData = OrderedDict({"BRUTE":{"bool": False, "name":"Brute Force"},
							"DIR-TRA":{"bool": False,"name":"Directories/Files Traversal"},
							"A-SQL":{"bool": False, "name":"Active SQL Injection"},
							"P-SQL":{"bool": False, "name":"Passive SQL Injection"},
							"XSS":{"bool": False, "name":"Cross-Site Scripting (XSS)"},
							"SENSITIVE":{"bool": False, "name":"Sensitive Files Disclosure"},
							"CSRF":{"bool": False, "name":"Cross Site Forgery (CSRF)"}})
	data = OrderedDict({"BRUTE":"", "DIR-TRA":"", "A-SQL":"", "P-SQL":"", "XSS":"", "CSRF":"", "SENSITIVE":""})

	#if fFile is not None and len(args.vulnerability.split(",")) > 0:
	#	logging.error("Only use --file (-f) command for specific vulnerability!")
	#	sys.exit(0)

	for i in args.vulnerability.split(","):
		i = i.strip()
		if i == "DIR-TRA":
			start = timer()
			logging.info("Starting to search for any access to directories and files...")
			dft = DirectoriesFilesTraversal(url, request)
			directoriesLst, filesLst = dft.startScanningDirectoriesFiles()
			end = timer()

			if(len(directoriesLst) > 0 or len(filesLst) > 0):
				boolData[i]["bool"] = True
				data[i] = {"Directories\n--------": directoriesLst, "Files\n--------": filesLst,
							"--- Completed in %.3f ms" % (end - start): ""}
			else:
				logging.info("Nothing found when performing a traversal directories or files!")

		elif i == "BRUTE":
			start = timer()
			logging.info("Brute forcing " + url + "...")
			b = BruteForce(url, request)
			flag, username, password, new_url = b.startBruteForce()
			end = timer()

			logging.info("Brute Force Cracked? " + str(flag))

			if flag:
				boolData[i]["bool"] = True
				data[i] = {"Cracked?":str(flag), "Before URL:":url, "After Login URL:": new_url, "Username:":username,
						   "Password:":password, "--- Completed in %.3f ms" % (end - start):""}

		elif i == "A-SQL":
			start = timer()

			url = args.url

			b = BruteForce(url, request)
			flag, username, password, url = b.startBruteForce()

			fuzz = Fuzzer(request)
			fuzz.discover(url)
			fuzz.print_discovered_links()
			links = fuzz.get_fuzz_links()

			a_sql = ActiveSQLInjection(request)
			links = fuzz.get_fuzz_links()
			a_sql.attack(links)

			inject_vulnerabilities_list = a_sql.sql_injection_result()
			end = timer()

			if len(inject_vulnerabilities_list) > 0:
				boolData[i]["bool"] = True
				data[i] = {"Active SQL Injection:\n--------":inject_vulnerabilities_list,
						   "Password:":password, "--- Completed in %.3f ms" % (end - start):""}

		elif i == "P-SQL":
			start = timer()

			url = args.url

			b = BruteForce(url, request)
			flag, username, password, url = b.startBruteForce()

			fuzz = Fuzzer(request)
			fuzz.discover(url)
			fuzz.print_discovered_links()

			links = fuzz.get_fuzz_links()
			p_sql = PassiveSQLInjection(request)
			links = fuzz.get_fuzz_links()
			p_sql.attack(links)

			inject_vulnerabilities_list = p_sql.sql_injection_result()

			end = timer()

			if len(inject_vulnerabilities_list) > 0:
				boolData[i]["bool"] = True
				data[i] = {"Passive SQL Injection:\n--------":inject_vulnerabilities_list,
						   "Password:":password, "--- Completed in %.3f ms" % (end - start):""}

		elif i == "XSS":
			start = timer()
			x = XSS(request)

			xRf = x.attackReflect(fuzz.get_fuzz_links())
			xStr = x.attackStored(fuzz.get_fuzz_links())
			end = timer()

			if xRf == 1 or xStr == 1:
				boolData[i]["bool"] = True
				data[i] = {"Vulnerability Found":True, "--- Completed in %.3f ms" % (end - start):""}

		elif i == "CSRF":
			start = timer()

			url = args.url

			b = BruteForce(url, request)
			flag, username, password, url = b.startBruteForce()

			fuzz = Fuzzer(request)
			fuzz.discover(url)
			fuzz.print_discovered_links()
			links = fuzz.get_fuzz_links()

			csrf = CSRF(links)

			csrfToken = input("Enter your CSRF Token (Don't have any? Press Enter): ")
			if csrfToken is not None or csrfToken != "":
				csrf.add_token(csrfToken)

			csrf.scan()
			vulnUrls, vulnInputs = csrf.csrf_protection_result()

			end = timer()

			if len(vulnUrls) > 0 or len(vulnInputs) > 0:
				total_vuln = len(vulnUrls) + len(vulnInputs)
				boolData[i]["bool"] = True
				data[i] = {"# of potiential issue due to no CSRF protection:":total_vuln,
						   "Vulnerability URLS:\n--------":vulnUrls, "Vulnerability Inputs:\n--------":vulnInputs,
						   "--- Completed in %.3f ms" % (end - start):""}

		elif i == "SENSITIVE":
			start = timer()
			fuzz.print_discovered_links()

			links = fuzz.get_fuzz_links()

			sensitive = Sensitive(links)
			sensitive.search()
			sensitiveLst = sensitive.display_sensitive_search_result()
			end = timer()

			if len(sensitiveLst) > 0:
				boolData[i]["bool"] = True
				data[i] = {"Potential Sensitive Breach:\n--------":sensitiveLst,
						   "--- Completed in %.3f ms" % (end - start):""}

		else:
			logging.error(i + " is an invalid command!")

	for i in data:
		if data[i] != "":
			if boolData[i]["bool"]:
				print("\n" + boolData[i]["name"] + " Stats\n==================")
				for j in data[i]:
					if type(data[i][j]) is list:
						print(j)
						for x in data[i][j]:
							print(x)
						print("\n")
					else:
						print("{0} {1}".format(j, data[i][j]))
				classification.vulnerability(i, boolData[i]["name"])
			else:
				print("This vulnerability, {0}, does not exist!".format(boolData[i]["name"]))



main()
