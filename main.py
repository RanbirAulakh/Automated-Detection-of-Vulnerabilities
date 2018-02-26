import sys




def error():
	'''
	Print error usages
	'''
	print("Usage: python3 main.py <args>")
	print("-h\tHelp - Show Usage")
	print("-v <TYPES> \tExecute Vulnerable; Below are types")
	print("\t\tALL - Execute All Types of Vulnerables")
	print("\t\tSQL - SQL Injection")
	print("\t\tCSRF - Exploit CSRF")
	sys.exit(0)


def main():
	error()




main()