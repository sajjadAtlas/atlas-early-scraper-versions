import selenium
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



def PipelineCompiler():
	options = Options()
	options.headless = True
	options.add_argument('--no-sandbox')
	driver = webdriver.Chrome('/Users/sajjad/Documents/chromedriver', options=options)
	print("Logging in, please wait")
	driver.get('https://www.biopharmcatalyst.com/account/login')
	driver.find_element_by_id('loginName').send_keys('Shakeel.school@gmail.com')
	driver.find_element_by_id('password').send_keys('Profit6969')
	driver.find_element_by_xpath('//*[@id="main"]/div/section/form/p/input').click()
	driver.get('https://www.biopharmcatalyst.com/calendars/historical-catalyst-calendar')
	historical = driver.find_element_by_xpath('//*[@id="main"]/div[2]/div[2]')
	time.sleep(2)
	print("Scraping...")
	pd.set_option('display.max_columns', None)
	pd.set_option('display.max_rows', None)
	catalyst_html = historical.get_attribute('innerHTML')
	df1 = read_html(catalyst_html)[0]
	df1.index = df1.index + 1  # shifting index
	df1.sort_index(inplace=True)
	file = pd.read_csv(r'/Users/sajjad/Documents/calendar.csv')
	df2 = pd.DataFrame(file)
	frames = [df1, df2]
	df3 = pd.concat(frames)
	
	del df3['last updated']
	df3.index = df3.index + 1  # shifting index
	df3.sort_index(inplace=True)
	
	driver.quit()
	
	print("Scrape Complete")
	
	PipeLineComp = df3.to_csv(r'/Users/sajjad/Documents/PipelineFile.csv', index = False)
	
	print("Saved to file")
	
	
	gc = gspread.service_account('/Users/sajjad/Documents/client_secret.json')
	
	sheet3 = gc.open("PIPELINE")
	file = '/Users/sajjad/Documents/PipelineFile.csv'
	df = pd.read_csv(file, encoding='ISO-8859-1')
	df.to_csv(file, encoding='utf-8', index=False)
	x = open(file, 'r').read()

	gc.import_csv('1euFw5CaWdq5mhzoNdaAVswu2wp5ZcOaurC312cR1rRM', x)
	
	
	print("gSheet Updated...Task Completed")
	print("Commencing again in 24h")
	
	

	
	
	
PipelineCompiler()

schedule.every(24).hours.do(PipelineCompiler)

while True:
	schedule.run_pending()

