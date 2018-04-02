# Automated Detection of Vulnerabilities on Websites

### Dates Due

- [x] Phrase 1 - Feb 9th, 2018
- [x] Phrase 2 - March 9th, 2018
- [ ] Phrase 3 - April 2nd, 2018
- [ ] Phrase 4 - April 13th, 2018
- [ ] Phrase 5 - April 23rd, 2018

### To-Do

Creating scripts that can discover the following vulnerabilities
- [ ] SQL Injections (50% completed)
- [x] Cross Site Scripting (XSS)
- [ ] Broken Authentication
- [x] Failure to restrict files, folders, and URL access
- [x] Brute Force
- [ ] Cross-Site Request Forgery (CSRF)

Create a command line style program 
- [x] Ability to take URL
- [ ] Display score for each violations
- [x] Classify which violated
- [x] Display a fix for it (prevent it)

Misc
- [ ] Document the codes and how to use it
- [ ] Follow Object Oriented Programming (OOP) standard

### Requirements
#### Languages
Python 3

#### Dependencies
Requests, BeautifulSoup4, Argparse

`pip3 install requests beautifulsoup4 argparse`

### Project & Environment setup
1. Download Xampp and install https://www.apachefriends.org/index.html
2. Start Apache & SQL server from XAMPP launcher
3. Download the Damn Vulnerable Web Application (DVWA) from http://www.dvwa.co.uk/
4. Move DVWA code to the `c:\\xamp\htdocs` folder in xampp so that the new path is now as `c:\\xampp\htdocs\dvwa`
4. For start, we will set DVWA to the lowest settings to ensure our codes work. Follow the README inside the downloaded DVWA folder to setup the database.
5. Happy coding

### Usage
`$ python3 Test.py`
This will run at test of active and passive sql injections as well as bruteforce logins

`$ python3 main.py -h`
This will print out the usage of python and how to use it. 

`$ python3 main.py -v <Vulnerability Type> -u <URL> -f <OPTIONAL FILE>`

`$ python3 main.py -v BRUTE -u http://localhost/dvwa/`
It will brute force the login, and prints out the username/password

`$ python3 main.py  -v DIR-TRA -u http://localhost/dvwa`
It will check for unathorized folder/file access

`$ python3 main.py -v XSS -u http://localhost/dvwa`
It will check for possible XSS weaknesses (Stored and Reflected) 

### Credits (+URL)

filenames.txt/directories.txt
-- https://blog.thireus.com/web-common-directories-and-filenames-word-lists-collection/
