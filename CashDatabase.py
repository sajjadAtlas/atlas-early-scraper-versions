from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from pandas.io.html import read_html
from selenium.webdriver.chrome.options import Options
import pandas as pd
import time
import schedule
import gspread



def cash_database():
	options = Options()
	options.headless = True
	driver = webdriver.Chrome('/Users/sajjad/Documents/chromedriver')
	
	print('Logging in, please wait')
	driver.get('https://www.biopharmcatalyst.com/account/login')
	driver.find_element_by_id('loginName').send_keys('Shakeel.school@gmail.com')
	driver.find_element_by_id('password').send_keys('Profit6969')
	driver.find_element_by_xpath('//*[@id="main"]/div/section/form/p/input').click()
	driver.get('https://www.biopharmcatalyst.com/company-cash-database')
	
	cashDatabase = driver.find_element_by_xpath('//*[@id="cashflow"]/div[2]')
	print("Scraping...")
	cashHTML = cashDatabase.get_attribute('innerHTML')
	df = pd.read_html(cashHTML)[0]

	df.loc[-1] = ['stringFilter', 'DateFilter', 'NumberRangeFilter', 'NumberRangeFilter', 'NumberRangeFilter', 'NumberRangeFilter', 'NumberRangeFilter'
	,'NumberRangeFilter', '']  # adding a row
	df.index = df.index + 1  # shifting index
	df.sort_index(inplace=True)
	
	print("Scrape Complete")
	
	driver.quit()
	
	CashFile = df.to_csv(r'/Users/Sajjad/Documents/CashFile.csv', index = False)
	
	print("Saved to file")
	
	gc = gspread.service_account('/Users/sajjad/Documents/client_secret.json')


	sheet6 = gc.open("CASHDB")
	file = '/Users/sajjad/Documents/CashFile.csv'
	df = pd.read_csv(file, encoding='ISO-8859-1')
	df.to_csv(file, encoding='utf-8', index=False)
	x = open(file, 'r').read()

	gc.import_csv('1webmygbpQ00j1QmavDUTdWGW8qW5KZfET3gKpCwwqEs', x)
		
	print("gSheet Updated...Task Completed")
	print("Commencing again in 24h")
	
cash_database()

	
schedule.every(24).hours.do(cash_database)

while True:
	schedule.run_pending()