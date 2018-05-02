# Automated Detection of Vulnerabilities on Websites

### Dates Due

- [x] Phrase 1 - Feb 9th, 2018
- [x] Phrase 2 - March 9th, 2018
- [x] Phrase 3 - April 2nd, 2018
- [x] Phrase 4 - April 13th, 2018
- [x] Phrase 5 - May 2nd, 2018

### To-Do

Creating scripts that can discover the following vulnerabilities
- [x] SQL Injections
- [x] Cross Site Scripting (XSS)
- [x] Sensitive
- [x] Failure to restrict files, folders, and URL access
- [x] Brute Force
- [x] Cross-Site Request Forgery (CSRF)

Create a command line style program 
- [x] Ability to take URL
- [x] Display a score
- [x] Display a fix for it (prevent it)

Misc
- [x] Document the codes and how to use it
- [x] Follow Object Oriented Programming (OOP) standard

### Requirements
#### Languages
Python 3

#### Dependencies
Requests, BeautifulSoup4, Argparse, url-normalize

`pip3 install requests beautifulsoup4 argparse url-normalize`

### Project & Environment setup
1. Download Xampp and install https://www.apachefriends.org/index.html
2. Start Apache & SQL server from XAMPP launcher
3. Download the Damn Vulnerable Web Application (DVWA) from http://www.dvwa.co.uk/
4. Move DVWA code to the `c:\\xamp\htdocs` folder in xampp so that the new path is now as `c:\\xampp\htdocs\dvwa`
4. For start, set DVWA to the lowest settings to ensure our codes work. Follow the README inside the downloaded DVWA folder to setup the database.
5. Happy coding
6. After setuping up the website and database. Set DVWA security to 'low'. Open `config.inc.php` under ` ..\htdocs\dvwa\config\` and change `$_DVWA[ 'default_security_level' ] = 'impossible';` to `$_DVWA[ 'default_security_level' ] = 'low';`

### Usage
`$ python3 Test.py`
This will run at test of active and passive sql injections as well as bruteforce logins

`$ python3 main.py -h`
This will print out the usage of python and how to use it. See below...

```
usage: main.py [-h] -v  -u  [-f FILE] [-d]

optional arguments:
  -h, --help            show this help message and exit
  -v , --vulnerability
                        Vulnerabilities Choices. See below...
  -u , --url            Website you want to attack
  -d, --debug           Enabled Debugging, otherwise Info

Vulnerability supports the following (multiple vulnerabilities? seperate by comma):
	BRUTE		- Brute Force Every Possible Inputs (LOGIN)
	A-SQL		- Active SQL Injection
	P-SQL		- Passive SQL Injection
	XSS			- Cross Site Scripting
	CSRF		- Cross Site Forgery
	DIR-TRA		- Directories/Files Traversal (Failure to restrict files, folders, and URL access)
	SENSITIVE	- Check for any sensitive data such as web configuration 

```

`$ python3 Main.py -v <Vulnerability Type> -u <URL> -d <OPTIONAL DEBUG>`

`$ python3 Main.py -v BRUTE -u http://localhost/dvwa/`
It will brute force the login, and prints out the username/password

`$ python3 Main.py  -v DIR-TRA -u http://localhost/dvwa`
It will check for unathorized folder/file access

`$ python3 Main.py -v XSS -u http://localhost/dvwa`
It will check for possible XSS weaknesses (Stored and Reflected) 

`$ python3 Main.py -v A-SQL -u http://localhost/dvwa`
Go through the list of links and their input and attempt multiple active SQL injections vectors. Active SQL Injection perform read and write.

`$ python3 Main.py -v P-SQL -u http://localhost/dvwa`
Go through the list of links and their input and attempt multiple passive SQL injections vectors. Passive SQL Injection perform read, not write.

`$ python3 Main.py -v SENSITIVE -u http://localhost/dvwa`
Check to see if there are any leak of sensitive information such as configuration files; for example phpinfo, config.ini or backup logs etc using predefined sensitive keywords

`$ python3 Main.py -v CSRF -u http://localhost/dvwa`
Takes link object and read the link object such as the content, inputs, and url to see if the CSRF token is in the link object.

`$ python3 Main.py -v BRUTE,XSS -u http://localhost/dvwa`
It will brute force the login and check for possible XSS weaknesses (Stored and Reflected). Supports multiple vulnerabilities, seperate them by comma

`$ python3 Main.py -v BRUTE -u http://localhost/dvwa -d`
It will brute force the login, and prints out the username/password. At the same time, it will enable debugging. 

`$ python3 Main.py -v BRUTE,A-SQL,P-SQL,XSS,CSRF,DIR-TRA,SENSITIVE -u https://localhost/dvwa/index.php`
It will execute every single vulnerabilities.

### Credits (+URL)

filenames.txt/directories.txt
-- https://blog.thireus.com/web-common-directories-and-filenames-word-lists-collection/
