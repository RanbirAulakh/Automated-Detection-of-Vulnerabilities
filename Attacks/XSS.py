class XSS(object):
  
  
  from bs4 import BeautifulSoup
  import re
  import urllib.request as urlreq
  from robobrowser import RoboBrowser

  """
    Perform XSS attack
  """


  def checkDVWAPage(URL):
      page = urlreq.urlopen(URL)
      soup = BeautifulSoup(page.read())

      forms = soup.find_all('form')
      for form in forms:
          #print("Parsing form...")
          localInputs = form.find_all('input')
          localTextAreas = form.find_all('textarea')

      browser = RoboBrowser()
      browser.open(URL)
      print("Starting URL: " + browser.url)
      form = browser.get_form(method='post')
      #Due to dvwa, need to login to get to target page
      form['username'].value = 'admin'
      form['password'].value = 'password'
      form.serialize()
      browser.submit_form(form)

      #Should be on a new page now?
      #Figure out what my current URL is
      print(browser.url)
      #Change URL
      browser.open(URL)
      print(browser.url)
      XSSPageForms = browser.get_form(method='post')
      print(XSSPageForms.fields)
      #NOTE: name and message have character caps (Because bad website is bad)
      XSSPageForms["txtName"].value = "PyScript"
      XSSPageForms["mtxMessage"].text = 'Python Says Hello' #Magic injection
      browser.submit_form(form, submit='btnClear')
      #We are triggering the button, but we're still missing some proccess;
      #Whatever we're saving isn't being stored- might be related to auth?



  def testForms(formList):
      #Somehow extract the forms using robobrowser and feed in samples from
      #websites on how to test for XSS in forms (Not in links)
      return

  checkDVWAPage("http://127.0.0.1/dvwa/vulnerabilities/xss_s/")
