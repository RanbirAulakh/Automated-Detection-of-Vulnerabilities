import sys
import argparse

from Attacks.BruteForce import BruteForce
from Attacks.DirectoriesFilesTraversal import DirectoriesFilesTraversal
from Attacks.PassiveSQLInjection import PassiveSQLInjection
from Attacks.ActiveSQLInjection import ActiveSQLInjection
from Utilities.Requests import Requests
from Utilities.Classification import Classification

from timeit import default_timer as timer

def choicesDescriptions():
	# ALL		- Execute All Vulnerabilities

	return """
Vulnerability supports the following:
	BRUTE		- Brute Force Every Possible Inputs (LOGIN)
	A-SQL		- Active SQL Injection
	P-SQL		- Passive SQL Injection
	XSS		- Cross Site Scripting
	CSRF		- Cross Site Forgery
	DIR-TRA		- Directories/Files Traversal (Failure to restrict files, folders, and URL access)
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

	classification = Classification()
	if vul is None or url is None:
		choicesDescriptions()

	elif args.vulnerability == "DIR-TRA":
		start = timer()
		dft = DirectoriesFilesTraversal(url, request)
		directoriesLst, filesLst = dft.startScanningDirectoriesFiles()
		end = timer()

		print("\nDirectories & Files Traversal\n=========")
		if(len(directoriesLst) > 0):
			print("Directories\n--------")
			for i in directoriesLst:
				print("--- " + i)
		if(len(filesLst) > 0):
			print("Files\n--------")
			for i in filesLst:
				print("--- " + i)

		print("Score: <Work-In-Progress>")
		print("Security Principles Violation: <Work-In-Progress>")
		print("--- Completed in %.3f ms" % (end - start))


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

		if flag:
			classification.vulnerability(vul)
		# print("Score: <Work-In-Progress>")
		# print("Security Principles Violation: <Work-In-Progress>")
		print("--- Completed in %.3f ms" % (end - start))

	elif args.vulnerability == "A-SQL":
		print("NOT IMPLEMENTED YET!")
	elif args.vulnerability == "P-SQL":
		print("NOT IMPLEMENTED YET!")
	elif args.vulnerability == "XSS":
		print("NOT IMPLEMENTED YET!")
	elif args.vulnerability == "CSRF":
		print("NOT IMPLEMENTED YET!")



main()