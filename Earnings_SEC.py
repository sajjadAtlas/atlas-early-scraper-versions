
from selenium import webdriver

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import schedule
import re
from fuzzywuzzy import fuzz

import mysql.connector
mydb = mysql.connector.connect(
  host="database-1.c5tk1b6m5b4o.us-east-1.rds.amazonaws.com",
  user="admin",
  password="Atlas1979"

)
url = 'https://www.sec.gov/cgi-bin/browse-edgar?company=&CIK=&type=10-Q&owner=include&count=40&action=getcurrent'
pastData = []
currentData = []
CompanyList = ['CAVCO INDUSTRIES INC.']

def Earnings_SEC():
    options = Options()
    options.headless = True
    driver = webdriver.Chrome('/Users/sajjad/Downloads/chromedriver', options=options)

    driver.get(url)


    time.sleep(5)
    text = driver.find_element_by_xpath('/html/body/div/table[2]/tbody/tr[2]/td[3]').text

    result = ''.join(i for i in text if not i.isdigit() and not i == '(' and not i == ')')

    splits = result.split()
    for word in splits:
        if word == 'Reporting' or word == 'Issuer' or word == 'Filer':

            splits.remove(word)

            splits = ' '.join(splits)




    for name in CompanyList:
        fuzzRatio = fuzz.partial_ratio(name, splits)
        if fuzzRatio >= 90:
            time.sleep(1)
            driver.find_element_by_xpath('/html/body/div/table[2]/tbody/tr[3]/td[2]/a[1]').click()
            time.sleep(2)
            form = driver.find_element_by_partial_link_text('htm')

            time.sleep(1)
            form.click()
            time.sleep(2)
            shelf_text = driver.find_elements_by_tag_name('body')
            link = driver.current_url
            currentData.append(link)

            time.sleep(5)

        else:
            driver.quit()
            Earnings_SEC()


def comparison(new_data):
    if new_data in pastData:
        return False
    else:
        return True



def run():
    link = Earnings_SEC()
    del currentData[:]
    Earnings_SEC()
    print(currentData)
    if currentData is not None:
        for item in currentData:
            cmp_res = comparison(item)
            if cmp_res:
                pastData.append(item)
                print(pastData)
            else:
                print("Entry already present!")
    else:
        print("No Entries Found Yet")


schedule.every(5).seconds.do(run)

while True:
    schedule.run_pending()