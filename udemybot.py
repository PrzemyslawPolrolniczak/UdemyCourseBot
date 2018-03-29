from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from sys import exit
import datetime

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
addedCourses = []
notFreeCourses = []
alreadyOwnedCourses = []
unknowErrors = []

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
			addedCourses.append(hrefList[y].split('/')[3])
			time.sleep(2)
			driver.quit()
			time.sleep(2)
			driver = webdriver.Firefox()
			initAndLogin(yourLogin, yourPassword)
			driver.get(back)			
		elif 'cart/subscribe/course' in currentURL: ## co ciekawe przy darmowych kursach bez kuponow nie ma tego problemu
			print hrefList[y].split('/')[3] + '  --- Course enrolled!'
			addedCourses.append(hrefList[y].split('/')[3])
			time.sleep(2)
			driver.get(back)
		elif 'cart/checkout/express' in currentURL:
			print hrefList[y].split('/')[3] + '  --- ERROR! This course is not free anymore!'
			notFreeCourses.append(hrefList[y].split('/')[3])
			time.sleep(2)
			driver.get(back) 
		else:
			print hrefList[y].split('/')[3] + '  --- ERROR! You already own this course!'
			alreadyOwnedCourses.append(hrefList[y].split('/')[3])
			time.sleep(2)
			driver.get(back)	
	except:
		print "!!!!!!!!!!UNKNOWN ERROR!!!!!!!!!!"
		unknowErrors.append(hrefList[y].split('/')[3])
		driver.get(back)
currentTime = datetime.datetime.now()

def printCourseList(inputVal):
		tempCourseList = ""
	 	for course in inputVal:
			 tempCourseList += course + "\n"
		return tempCourseList

writeLog = open("log " + currentTime.strftime("%Y-%m-%d") + ".txt", "w")
writeLog.write('Date: ' + currentTime.strftime("%Y-%m-%d %H:%M") + "\n" + 'Courses added: ' + str(len(addedCourses)) + "\n" + 'Courses not free anymore: ' + str(len(notFreeCourses)) + "\n" + 'Courses already owned: ' + str(len(alreadyOwnedCourses)) + "\n" + 'Unknown errors: ' + str(len(unknowErrors)) + "\n\n" + "List of added Courses: \n" + str(printCourseList(addedCourses)) + "\n\n" + 'List of already owned courses: \n' + str(printCourseList(alreadyOwnedCourses)) + "\n\n" + "List of paid courses: \n" + str(printCourseList(notFreeCourses)) + "\n*****************************************************\n\n")
writeLog.close()
print "#################################"
print "############ D O N E ############"
print "#################################"
print "Courses added: " + str(len(addedCourses))
print "Courses not free anymore: " + str(len(notFreeCourses))
print "Courses already owned: " + str(len(alreadyOwnedCourses))
print "Unknown errors: " + str(len(unknowErrors))
print "\a"
time.sleep(0.2)
print "\a"
time.sleep(0.2)
print "\a"
overview = True;
def overviewLogic():
	
	def typeChar():
		additionalInfo = raw_input("Type 's' for list of successfully added courses, type 'o' for list of already owned courses, type 'p' for list of courses that are paid now, type 'x' to exit: ")
		allowed = "sopxh"
		while len(additionalInfo) != 1 or additionalInfo not in allowed:
			additionalInfo = raw_input("Unknown command, type 'h' for list of commands: ")
			if additionalInfo == 'h':
				print '\n'
		return additionalInfo	
	print "\n"
	character = typeChar()

	def f(case):
		return {
			's':'Successfully added courses: \n' + str(printCourseList(addedCourses)),
			'o':'Owned courses: \n' + str(printCourseList(alreadyOwnedCourses)),
			'p':'Paid courses: \n' + str(printCourseList(notFreeCourses)),
			'h':'',
			'x':'Bye!'	
		}.get(case, 'Unknown command')
	print f(character)
	print "\n"
	if character == 'x':
		return False
	else:
		return True

while overview == True:
	overview = overviewLogic()

exit()
### TO DO ###
# Otwieranie wszystkich linkow w nowych kartach a potem tylko zmiana karty i klik enroll (moze sypac blad z timeoutem)
# Uruchamianie sie samoczynnie w nocy i gaszenie kompa -- to juz raczej kazdy we wlasnym OS
# Okienka z firefoxa musza byc otwierane w tle
# Wysylka maila/sms-a z iloscia kursow dodanych i ich nazwami
# Przyspieszyc skrypt
# opcja zapamietania loginu i hasla z zapisem do zmiennej
# jakos moze da sie przypiac uruchomienie bota do stworzenia nowego tematu z kursami udemy?
