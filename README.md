# Automated Detection of Vulnerabilities on Websites

### Dates Due

- [x] Phrase 1 - Feb 9th, 2018
- [ ] Phrase 2 - March 9th, 2018
- [ ] Phrase 3 - April 2nd, 2018
- [ ] Phrase 4 - April 13th, 2018
- [ ] Phrase 5 - April 23rd, 2018

### Project & Environment setup
1. Download Xampp and install https://www.apachefriends.org/index.html
2. Start Apache & SQL server from XAMPP launcher
3. Download the Damn Vulnerable Web Application (DVWA) from http://www.dvwa.co.uk/
4. Move DVWA code to the htdocs folder in xampp so that the new path is now as xampp/htdocs/dvwa
4. For start, we will set DVWA to the lowest settings to ensure our codes work. Follow the README inside the downloaded DVWA folder
5. Happy coding


### To-Do

Creating scripts that can discover the following vulnerabilities
- [ ] SQL Injections
- [ ] Cross Site Scripting (XSS)
- [ ] Broken Authentication
- [ ] Failure to restrict files, folders, and URL access
- [ ] Cross-Site Request Forgery (CSRF)

Create a command line style program 
- [ ] Ability to take URL
- [ ] Display score for each violations
- [ ] Classify which violated
- [ ] Display a fix for it (prevent it)


### Languages
Python 3

### Dependencies
Requests, BeautifulSoup4, Argparse, RoboBrowser

pip3 install requests

pip3 install beautifulsoup4

pip3 install argparse

pip3 install robobrowser



### Credits (+URL)

filenames.txt/directories.txt
-- https://blog.thireus.com/web-common-directories-and-filenames-word-lists-collection/