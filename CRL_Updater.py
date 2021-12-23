import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from pandas.io.html import read_html
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


url = 'https://www.globenewswire.com/Search/NewsSearch?keyword=complete%20response%20letter&icb=4570&subjectCode=Company%20Announcement'
pastData = []
currentData = []

def CRL_Updater():
    options = Options()
    options.headless = True
    driver = webdriver.Chrome('/Users/sajjad/Downloads/chromedriver', options=options)

    driver.get(url)

    driver.find_element_by_xpath('/html/body/div[2]/div/a[1]/i[1]').click()
    time.sleep(1)
    search_bar = driver.find_element_by_xpath('//*[@id="quicksearch-textbox"]')
    search_bar.send_keys('complete response letter')
    search_bar.send_keys(Keys.ENTER)

    cookies_button = WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div/div/a')))
    time.sleep(1)
    driver.execute_script("arguments[0].click();", cookies_button)
    time.sleep(2)
    refine_search = driver.find_element_by_xpath('//*[@id="search_addkeyword"]')
    refine_search.send_keys('receives complete response letter')
    time.sleep(1)
    refine_search.send_keys(Keys.ENTER)

    exchange = WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable((By.XPATH, '//*[@id="content-L3"]/a[9]/div')))
    driver.execute_script("arguments[0].click();", exchange)

    nasdaq_box = WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable((By.XPATH, '//*[@id="facetfield_Exchange_nasdaq"]')))
    time.sleep(3)
    driver.execute_script("arguments[0].click();", nasdaq_box)

    links = driver.find_elements_by_xpath('//a[contains(translate(.,"Receives Complete Response",'
                                          '"receives complete response"),'
                                         ' "receives complete response")]')
    update = links[0]
    update_title = links[0].text

    driver.implicitly_wait(10)

    update.click()

    update_textScrape = driver.find_elements_by_css_selector("#content-L2 > span")

    update_content = update_textScrape[0].text

    if "(GLOBE NEWSWIRE)" in update_content:
        update_content = update_content.replace("(GLOBE NEWSWIRE)","")

    find_ticker = driver.find_element_by_xpath("//p[contains(., '(NASDAQ: ') or contains(., '(Nasdaq') "
                                                "or contains(., '(NasdaqCM')]")



    find_ticker = find_ticker.text

    paranthesis_text = re.findall('\(.*?\)', find_ticker)

    for item in paranthesis_text:
        if "NASDAQ" in item or "Nasdaq" in item or "NasdaqCM" in item:

            ticker_exp = item
            removable1 = "NASDAQ: "
            removable2 = "("
            removable3 = ")"
            removable1_1 = "Nasdaq: "
            removable1_2 = "NasdaqCM: "
            removable1_3 = "Nasdaq:"

            if removable1 in ticker_exp and removable2 in ticker_exp and removable3 in ticker_exp:
                ticker_exp = ticker_exp.replace(removable1, "")
                ticker_exp = ticker_exp.replace(removable2, "")
                ticker_exp = ticker_exp.replace(removable3, "")



            elif removable1_1 in ticker_exp and removable2 in ticker_exp and removable3 in ticker_exp:
                ticker_exp = ticker_exp.replace(removable1_1, "")
                ticker_exp = ticker_exp.replace(removable2, "")
                ticker_exp = ticker_exp.replace(removable3, "")


            elif removable1_2 in ticker_exp and removable2 in ticker_exp and removable3 in ticker_exp:
                ticker_exp = ticker_exp.replace(removable1_2, "")
                ticker_exp = ticker_exp.replace(removable2, "")
                ticker_exp = ticker_exp.replace(removable3, "")



            elif removable1_3 in ticker_exp and removable2 in ticker_exp and removable3 in ticker_exp:
                ticker_exp = ticker_exp.replace(removable1_3, "")
                ticker_exp = ticker_exp.replace(removable2, "")
                ticker_exp = ticker_exp.replace(removable3, "")

                #ticker is stored in ticker_exp

    currentData.append(update_content)
    return update_content

def comparison(new_data):
    if new_data in pastData:
        return False
    else:
        return True

def email(update_content):

    update_content = CRL_Updater()
    msg = MIMEMultipart()
    x = 'sajjad@spartanfinance.io'
    msg['From'] = x
    msg['To'] = 'sajjad.abbas09@gmail.com'

    msg['Subject'] = 'CRL Sent'

    message = update_content

    msg.attach(MIMEText(message, 'plain'))

    ##########################################
    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(x, "sajjad1423")  ## ENTER YOUR PASSWORD HERE

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(x, 'sajjad.abbas09@gmail.com', text)

def run():
    update_content = CRL_Updater()
    del currentData[:]
    CRL_Updater()
    if currentData is not None:
        for update_content in currentData:
            compare = comparison(update_content)
            if compare:
                pastData.append(update_content)
                email(update_content)
            else:
                print("Entry already present")
    else:
        print("Nothing found yet")



schedule.every(1).seconds.do(run)

while True:
    schedule.run_pending()