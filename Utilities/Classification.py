import statistics
from collections import OrderedDict

class Classification:
	"""
	In order to classify the rating for each vulnerabilities. We ended up using OWASP rating methodology.
	More information can be found here: https://www.owasp.org/index.php/OWASP_Risk_Rating_Methodology

	However, we made some changes to OWASP rating methodology. For example, technical impact factors, we
	decided to eliminate "Loss of Accountability", Business Impact Factors (ie: Finanical, Rep damage),
	and Threat Agent Factors (we can't determine their motive)/


	TL:DR; RISK = Likelihood * Impact

	Since, we are not using neural networks or machine learning to determine if the info or leaked data are
	private/sentitive. We will just give an estimate score.

	"""
	def determineRisk(self, ciaScore, vulScore):
		"""
		Determine the risk and return 3 results, not the best logic, but works flawlessly
		:param vulScore: mean of VulScore
		:param ciaScore: mean of ciaScore
		:return: risk in string
		"""

		severityRisk1 = ""
		if ciaScore >= 0 and ciaScore < 3:
			severityRisk1 = "LOW"
		elif ciaScore >= 3 and ciaScore < 6:
			severityRisk1 = "MEDIUM"
		elif ciaScore >= 6 and ciaScore < 10:
			severityRisk1 = "HIGH"

		severityRisk2 = ""
		if vulScore >= 0 and vulScore < 3:
			severityRisk2 = "LOW"
		elif vulScore >= 3 and vulScore < 6:
			severityRisk2 = "MEDIUM"
		elif vulScore >= 6 and vulScore < 10:
			severityRisk2 = "HIGH"

		if severityRisk1 == severityRisk2:
			if severityRisk1 == "HIGH" and severityRisk2 == "HIGH":
				return severityRisk1, severityRisk2, "CRITICAL"
			return severityRisk1, severityRisk2, severityRisk1
		elif severityRisk1 == "LOW":
			if severityRisk2 == "MEDIUM":
				return severityRisk1, severityRisk2, "LOW"
			if severityRisk2 == "HIGH":
				return severityRisk1, severityRisk2, "MEDIUM"
		elif severityRisk1 == "MEDIUM":
			if severityRisk2 == "LOW":
				return severityRisk1, severityRisk2, "LOW"
			if severityRisk2 == "HIGH":
				return severityRisk1, severityRisk2, "HIGH"
		elif severityRisk1 == "HIGH":
			if severityRisk2 == "LOW":
				return severityRisk1, severityRisk2, "MEDIUM"
			if severityRisk2 == "MEDIUM":
				return severityRisk1, severityRisk2, "HIGH"

	def vulnerabilityInfo(self):
		"""
		Return a dictionary that contains relevant information related to vulnerabilities
		:return: info
		"""
		dataDict = OrderedDict()

		BRUTE_DICT = {"Links":["Brute Force Attack Info: https://www.owasp.org/index.php/Brute_force_attack",
											 "Brute Force Fix: https://www.owasp.org/index.php/Blocking_Brute_Force_Attacks",
							   "Summary of Fix: Implement delay for every fail attempts or lock an account "
							   "after certain number of tries."]}
		A_SQL = {"Links":["SQL Injection Attack Info: https://www.owasp.org/index.php/SQL_Injection",
							"SQL Injection Fix (Cheat Sheet): https://www.owasp.org/index.php/PHP_Security_Cheat_Sheet",
						  "SQL Injection Prevention: https://www.owasp.org/index.php/SQL_Injection_Prevention_Cheat_Sheet"]}
		P_SQL = A_SQL

		XSS = {"Links":["Cross-site Scripting (XSS) Attack Info: https://www.owasp.org/index.php/Cross-site_Scripting_(XSS)",
						  "XSS Fix (Prevention): https://www.owasp.org/index.php/XSS_(Cross_Site_Scripting)_Prevention_Cheat_Sheet"]}

		CSRF = {"Links":["Cross-Site Request Forgery (CSRF) Attack Info: https://www.owasp.org/index.php/Cross-Site_Request_Forgery_(CSRF)",
							"CSRF Fix (Cheat Sheet): https://www.owasp.org/index.php/Cross-Site_Request_Forgery_(CSRF)_Prevention_Cheat_Sheet",
						  "CSRF Prevention: https://www.owasp.org/index.php/Talk:Cross-Site_Request_Forgery_(CSRF)_Prevention_Cheat_Sheet"]}

		DIR_TRA = {"Links":["Directory Traversal/File Attack Info: https://www.owasp.org/index.php/Path_Traversal",
							"Directory Traversal/File Fix (Prevention): https://www.owasp.org/index.php/File_System#Path_traversal"]}

		SENSITIVE = {"Links":["Sensitive Files Disclosure Info: https://www.owasp.org/index.php/Top_10-2017_A3-Sensitive_Data_Exposure",
							  "Sensitive Files Disclosure (Prevention) OWASP: https://www.owasp.org/index.php/Top_10-2017_A3-Sensitive_Data_Exposure"
							"Sensitive Files Disclosure (Prevention) - External: https://hdivsecurity.com/owasp-sensitive-data-exposure"]}

		dataDict["BRUTE"] = BRUTE_DICT
		dataDict["A-SQL"] = A_SQL
		dataDict["P-SQL"] = P_SQL
		dataDict["XSS"] = XSS
		dataDict["CSRF"] = CSRF
		dataDict["DIR-TRA"] = DIR_TRA
		dataDict["SENSITIVE"] = SENSITIVE

		return dataDict

	def vulnerability(self, name, fullName):
		"""
		Determine the score for each vulnerability

		:param name: vulnerability name
		:return: None
		"""

		"""
			Vulnerability Score according to OWASP
			
			Ease of discovery
				How easy is it for attackers to discover this vulnerability? 
					Practically impossible (1), difficult (3), easy (7), automated tools available (9)
				
			Ease of exploit
				How easy is it for attackers to actually exploit this vulnerability? 
					Theoretical (1), difficult (3), easy (5), automated tools available (9)
			
			Awareness
				How well known is this vulnerability?
					Unknown (1), hidden (4), obvious (6), public knowledge (9)
			
			Intrusion detection
				How likely is an exploit to be detected? 
					Active detection in application (1), logged and reviewed (3), Hit or Miss (5)
					logged without review (8), not logged (9)
					
			Stored as List
				[Ease Discovery, Ease Exploit, Awareness, Intrusion Detection]
							
		"""
		vulnerability_score = [0, 0, 0, 0]

		"""
			Possible CIA Score: 
				(1) Very Minimal, (3) Minimal, (5) Medium Impact, (7) Critical, (9) Very Critical (All data)
				
			Stored as List
				[Confidentiality, Integrity, Avaiability]
		"""
		cia_score = [0, 0, 0]

		if name == "BRUTE":
			cia_score = [3, 1, 5]
			vulnerability_score = [9, 9, 9, 5]

		elif name == "A-SQL" or name == "P-SQL":
			cia_score = [9, 9, 9]
			vulnerability_score = [9, 9, 9, 8]

		elif name == "XSS":
			cia_score = [3, 1, 5]
			vulnerability_score = [9, 5, 4, 5]

		elif name == "CSRF":
			cia_score = [3, 1, 5]
			vulnerability_score = [9, 5, 4, 5]

		elif name == "DIR-TRA":
			cia_score = [3, 1, 5]
			vulnerability_score = [9, 9, 9, 5]

		elif name == "SENSITIVE":
			cia_score = [1, 1, 3]
			vulnerability_score = [3, 1, 1, 5]

		# determine the risk
		meanCiaScore = statistics.mean(cia_score)
		meanVulScore = statistics.mean(vulnerability_score)
		severityRisk1, severityRisk2, totalRisk = Classification.determineRisk(self, meanCiaScore, meanVulScore)

		print("\n" + fullName + " Rating and Impact:\n===================")
		print("Likelihood: {0} - {1}".format(meanVulScore, severityRisk2))
		print("Impact: {0} - {1}".format(meanCiaScore, severityRisk1))
		print("Overall Risk: {0}".format(totalRisk))

		print("\nMore Information about " + fullName + " and how to fix it:\n==================================================")

		"""
			Dictionary that contains vulnerability information, if it's true, prints it
		"""
		dataDict = Classification.vulnerabilityInfo(self)
		for i in dataDict[name]["Links"]:
			print(i)

		print("\n\n")
