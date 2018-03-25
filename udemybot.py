from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

## Dla wygody mozna ustawic haslo z reki, wtedy wystarczy do zmiennej yourLogin przypisac stringa z loginem i analogicznie z haslem (np: yourlogin = 'mail@gmail.com') 
yourLogin = raw_input('Enter your login: ')
yourPassword = raw_input('Enter your password: ')
print 'Your login details are:'
print 'Login: ' + yourLogin
print 'Password: ' + yourPassword

driver = webdriver.Firefox()

def initAndLogin(login, password):
	driver.get('https://www.udemy.com/')
	driver.execute_script("$('a.btn-quaternary').click()")
	time.sleep(2)
	driver.execute_script('document.getElementById("id_email").value="' + login + '"')
	driver.execute_script('document.getElementById("id_password").value="' + password + '"')
	driver.execute_script("$('#submit-id-submit').click()")
	time.sleep(5)

initAndLogin(yourLogin, yourPassword)
driver.get("https://www.wykop.pl/tag/kursyudemy/")
elem = driver.find_element_by_css_selector("a[href*='https://www.wykop.pl/wpis/']")
elem.click()
back = driver.current_url
links = driver.find_elements_by_css_selector("a[href*='udemy.com']")
hrefList = []

for x in range(0, len(links)):
	hrefList.append(links[x].get_attribute("href"))

for y in range(0, len(links)):
	driver.get(hrefList[y])
	time.sleep(2)
	try:
		driver.execute_script("$('button.course-cta').click()")
		time.sleep(3)
		currentURL = driver.current_url
		if 'cart/success' in currentURL: ## po kliknieciu enroll wymagany jest restart przegladarki, inaczej po wejsciu na strone udemy bedzie ciagle timeout error
			print hrefList[y].split('/')[3] + '  --- Course enrolled!'
			time.sleep(2)
			driver.quit()
			time.sleep(2)
			driver = webdriver.Firefox()
			initAndLogin(yourLogin, yourPassword)
			driver.get(back)			
		elif 'cart/subscribe/course' in currentURL: ## co ciekawe przy darmowych kursach bez kuponow nie ma tego problemu
			print hrefList[y].split('/')[3] + '  --- Course enrolled!'
			time.sleep(2)
			driver.get(back)
		elif 'cart/checkout/express' in currentURL:
			print hrefList[y].split('/')[3] + '  --- ERROR! This course is not free anymore!'
			time.sleep(2)
			driver.get(back) 
		else:
			print hrefList[y].split('/')[3] + '  --- ERROR! You already own this course!'
			time.sleep(2)
			driver.get(back)	
	except:
		print "!!!!!!!!!!UNKNOWN ERROR!!!!!!!!!!"
		driver.get(back)
print "#################################"
print "############ D O N E ############"
print "#################################"
## Make a finish sound
print "\a"
time.sleep(0.2)
print "\a"
time.sleep(0.2)
print "\a"

