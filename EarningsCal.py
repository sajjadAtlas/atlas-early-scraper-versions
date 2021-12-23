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



def earnings_calendar():
	options = Options()
	options.headless = True
	driver = webdriver.Chrome('/Users/sajjad/Documents/chromedriver', options=option)
	
	print('Logging in, please wait')
	driver.get('https://www.biopharmcatalyst.com/account/login')
	driver.find_element_by_id('loginName').send_keys('Shakeel.school@gmail.com')
	driver.find_element_by_id('password').send_keys('Profit6969')
	driver.find_element_by_xpath('//*[@id="main"]/div/section/form/p/input').click()
	print("Scraping...")
	driver.get('https://www.biopharmcatalyst.com/calendars/biotech-earnings-calendar')
	pd.set_option('display.max_columns', None)
	pd.set_option('display.max_rows', None)
	earningscal = driver.find_element_by_xpath('//*[@id="main"]/div[2]/div[2]')
	earningscalHTML = earningscal.get_attribute('innerHTML')
	
	df = pd.read_html(earningscalHTML)[0]
	df.loc[-1] = ['stringFilter', 'DateFilter', 'NumberRangeFilter', 'NumberRangeFilter', 'NumberRangeFilter', 'NumberRangeFilter']  # adding a row
	df.index = df.index + 1  # shifting index
	df.sort_index(inplace=True)
	
	driver.quit()
	
	print("Scrape Complete")
	
	EarningsFile = df.to_csv(r'/Users/Sajjad/Documents/EarningsCal.csv', index = False)
	
	print("Saved to file")
	
	gc = gspread.service_account('/Users/sajjad/Documents/client_secret.json')


	sheet5 = gc.open("EARNINGSCAL")
	file = '/Users/sajjad/Documents/EarningsCal.csv'
	df = pd.read_csv(file, encoding='ISO-8859-1')
	df.to_csv(file, encoding='utf-8', index=False)
	x = open(file, 'r').read()

	gc.import_csv('1uTvW-kW4Z1anwUk0qqGVq6nn-obGE5yIEG6PTbRWKmU', x)
	
	print("gSheet Updated...Task Completed")
	print("Commencing again in 24h")
	
earnings_calendar()

schedule.every(24).hours.do(earnings_calendar)

while True:
	schedule.run_pending()
	
	