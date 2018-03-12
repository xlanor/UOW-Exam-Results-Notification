
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import *
import os, time
import telegram
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler,Job, MessageHandler, Filters, RegexHandler, ConversationHandler

class openSite():
	def __init__(self):
		self.__driver = None
		# Chromedriver uses the installed chrome.
		self.__chrome_driver = "./chromedriver"

	def loadDriver(self):
		driver = webdriver.Chrome(chrome_options=self.__chrome_options(), executable_path=self.__chrome_driver)
		driver.get('https://solss.uow.edu.au/sid/sols_login_auth.do_login')
		#driver.get_screenshot_as_file("capture.png")
		return driver

	def __chrome_options(self):
		# instantiate a chrome options object so you can set the size and headless preference
		chrome_options = Options()
		chrome_options.add_argument("--headless")
		chrome_options.add_argument("--window-size=1920x1080")
		return chrome_options

#Class login inherits class opensite.
class Login(openSite):
	def __init__(self,username,password):
		openSite.__init__(self)
		self.__driver = openSite.loadDriver(self)
		self.__username = username
		self.__password = password

	def scrape_results(self):
		if self.__login_Attempt():
			print('Logged in')
			tbody = self.__navigate_Results()
			if tbody:
				print('Navigated to Result Page')
				result_dict = self.__scrape_Results(tbody)
				self.__close_driver()
				if not result_dict:
					return False
				else:
					return result_dict
			else:
				self.__close_driver()
				return False
		else:
			self.__close_driver()
			print('An error has occured.')
			return False

	def __close_driver(self):
		self.__driver.close()

	def __login_Attempt(self):
		user = self.__driver.find_element_by_name('p_username')
		pw = self.__driver.find_element_by_name('p_password')
		loginbtn = self.__driver.find_element_by_xpath("//input[@value='Login']")
		user.send_keys(self.__username)
		pw.send_keys(self.__password)
		loginbtn.click()
		time.sleep(10)

		#self.__driver.close()
		try:
			self.__driver.find_element_by_xpath("//input[@value='Login']")
		except NoSuchElementException:
			return True
		else:
			return False

	def __navigate_Results(self):
		resultbtn = self.__driver.find_element_by_xpath("//a[@data-id='21']")
		resultbtn.click()
		time.sleep(10)

		#table = self.__driver.find_element_by_class_name('table-striped')
		tbody = self.__driver.find_element_by_xpath("//tbody")

		self.__driver.get_screenshot_as_file("capture.png")

		if tbody:
			return tbody
		else:
			return False

	def __scrape_Results(self,tbody):
		rows = tbody.find_elements_by_xpath("//tr")
		result_dict = {}
		if rows:
			for index,row in enumerate(rows):
				if index != 0:
					cell = row.find_elements_by_tag_name("td")
					result = cell[7].get_attribute('innerHTML')
					if result.find('&nbsp') != -1:
						result_dict[cell[3].text] = "-"
					else:
						result_dict[cell[3].text] = result
			return result_dict
		else:
			return False

	def write_element_log(self,object_to_write):
		result = object_to_write.get_attribute('innerHTML')
		with open("logging_obj.txt","w") as log:
			log.write(formatted_result)

	def write_log(self):
		formatted_result = self.__driver.page_source
		with open("logging.txt","w") as log:
			log.write(formatted_result)

class checkResult():
	def __init__(self):
		self.details = {'username':'SOLSUsername','password':'SOLSPassword'} #enter your SOLS USN/PW Here
		self.send_list = ['myuserid'] #Enter your tg user ID here (ie 10034673)
		self.notificaion_list = ['Secondary user id'] #Enter your secondary user_ID here, ie: I want to send my results to myself, but I want to send a general notification to my group of friends.

	def check_Results(self,bot,update):
		result = Login(self.details['username'],self.details['password']).scrape_results()
		message = ""
		if result:
			if self.parse_Results(result,message):
				bot.sendMessage(chat_id=self.send_list[0],text=message,parse_mode='HTML')
				notificationstring = ""
				notificationstring += "Results have been released! Please check SOLS\n"
				notificationstring += "{} {} {} {} {}".format('@user1','@user2','@user3','@user4','@user5') #I have 5 friends in my group chat
				bot.sendMessage(chat_id=self.notificaion_list[0],text=notificationstring,parse_mode='HTML')
			else:
				#debugging stuff, ideally you should not fire a notification
				bot.sendMessage(chat_id=self.send_list[0],text=str(result),parse_mode='HTML')


	def parse_Results(self,result_dict,message):
		for key,value in result_dict.items():
			if value == "-":
				return False
			else:
				message += "{} : {} \n".format(key,value)

		return True
    
	# Debug stuff. nomnom
	def get_raw_data(self,bot,update):
		print (update)

def load_bot():
	print("Result_Checking online")
	updater = Updater(token="yourbottoken",request_kwargs={'read_timeout': 6, 'connect_timeout': 7}) #replace your bot token here.
	dispatcher = updater.dispatcher	
	raw_data_handler = CommandHandler('rawdata', checkResult().get_raw_data)
	dispatcher.add_handler(raw_data_handler)
	j = updater.job_queue
	job_minute = j.run_repeating(checkResult().check_Results,600,0)
	updater.start_polling()
	updater.idle



if __name__ == "__main__":
	load_bot()
