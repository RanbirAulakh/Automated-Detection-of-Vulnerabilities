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

def choicesDescriptions():
	return """
Vulnerability supports the following (multiple vulnerabilities? seperate by comma):
	ALL			- Execute all vulnerabilities listed below
	BRUTE		- Brute Force Every Possible Inputs (LOGIN)
	A-SQL		- Active SQL Injection
	P-SQL		- Passive SQL Injection
	XSS		- Cross Site Scripting
	CSRF		- Cross Site Forgery
	DIR-TRA		- Directories/Files Traversal (Failure to restrict files, folders, and URL access)
	"""

def main():
	logging.basicConfig(format="%(asctime)s - %(levelname)s %(message)s", level = logging.INFO)

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
	parser.add_argument(
	   "-f", '--file',
	   help='Specific textfiles to use for attacking. Otherwise will use defaults.',
		metavar='',
	   required=False
	)
	args = parser.parse_args()

	url = args.url
	vul = args.vulnerability

	request = Requests()
	request = request.request

	fuzz = Fuzzer(request)
	fuzz.discover(url)

	classification = Classification()
	if vul is None or url is None:
		choicesDescriptions()
		sys.exit(0)

	for i in args.vulnerability.split(","):
		i = i.strip()
		if i == "DIR-TRA":
			start = timer()
			dft = DirectoriesFilesTraversal(url, request)
			directoriesLst, filesLst = dft.startScanningDirectoriesFiles()
			end = timer()
			print("\nDirectories & Files Traversal\n=========")

			if(len(directoriesLst) > 0 or len(filesLst) > 0):
				if(len(directoriesLst) > 0):
					print("Directories\n--------")
					for link in directoriesLst:
						print("--- " + link)
				if(len(filesLst) > 0):
					print("Files\n--------")
					for link in filesLst:
						print("--- " + link)
				classification.vulnerability(i)
			else:
				print("Nothing found!")

			print("--- Completed in %.3f ms" % (end - start))

		elif i == "BRUTE":
			start = timer()
			logging.info("Brute forcing " + url + "...")
			b = BruteForce(url, request)
			flag, username, password, new_url = b.startBruteForce()
			end = timer()

			print("\nBrute Force Stats\n==================")
			print("Cracked? " + str(flag))

			if flag:
				print("Before URL: " + url)
				print("After Login URL: " + new_url)
				print("Username: " + username)
				print("Password: " + password)
				classification.vulnerability(i)

			print("--- Completed in %.3f ms" % (end - start))

		elif i == "A-SQL":
			print("NOT IMPLEMENTED YET!")
		elif i == "P-SQL":
			print("NOT IMPLEMENTED YET!")
		elif i == "XSS":
			x = XSS(request)

			xRf = x.attackReflect(fuzz.get_fuzz_links())
			xStr = x.attackStored(fuzz.get_fuzz_links())

			print("\nXSS STATS\n=========")

			print("URL: " + args.url)
			print("After XSS Injection URL: " + url)
			if(xRf == 1 or xStr == 1):
				classification.vulnerability(i)
			#else:
				#print("No issues detected")
		elif i == "CSRF":
			print("NOT IMPLEMENTED YET!")




main()
