import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from pandas.io.html import read_html
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
import time
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import schedule
import re

url = 'https://www.globenewswire.com/Search/NewsSearch?keyword=biotech&icb=4570&subjectCode=Mergers%20and%20Acquisitions&exchange=Nasdaq%2CNYSE'
pastData = []
currentData = []

def M_A():
    options = Options()
    #options.add_extension("/Users/sajjad/Desktop/proxy.crx")
    #PROXY = "5.79.73.131:13010"
   # options.add_argument('--proxy-server=%s' % PROXY)
    options.headless = True
    options.add_argument("--incognito")
    driver = webdriver.Chrome('/Users/sajjad/Downloads/chromedriver', options=options)
    driver.get(url)

    driver.find_element_by_xpath('/html/body/div[2]/div/a[1]/i[1]').click()
    time.sleep(1)
    search_bar = driver.find_element_by_xpath('//*[@id="quicksearch-textbox"]')
    search_bar.send_keys('biotech')
    search_bar.send_keys(Keys.ENTER)

    #cookies_button = driver.find_element_by_xpath("/html/body/div[5]/div/div/a").click()
    cookies_button = WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div/div/a')))
    time.sleep(1)
    driver.execute_script("arguments[0].click();", cookies_button)

    industry_box = WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable((By.ID, 'facetfield_Icb_4570')))
    time.sleep(3)
    driver.execute_script("arguments[0].click();", industry_box)

    subject_dropdown = WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable((By.XPATH,
                                    "//a[contains(@onclick,'ShowFacetDivAll(topFacetfield_SubjectCode , allFacetfield_SubjectCode)')]")))
    time.sleep(1)
    driver.execute_script("arguments[0].click();", subject_dropdown)

    MnA_box = WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable((By.ID, 'facetfield_SubjectCode_Mergers_and_Acquisitions')))
    time.sleep(1)
    driver.execute_script("arguments[0].click();", MnA_box)

    exchange = WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable((By.XPATH, '//*[@id="content-L3"]/a[9]/div')))
    driver.execute_script("arguments[0].click();", exchange)

    exchange_menu2 = WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable(
            (By.XPATH, "//a[contains(@onclick,'ShowFacetDivAll(topFacetfield_Exchange , allFacetfield_Exchange)')]")))
    driver.execute_script("arguments[0].click();", exchange_menu2)

    nyse_box =  WebDriverWait(driver, 10).until(
        ec.element_to_be_clickable(
            (By.XPATH, '//*[@id="facetfield_Exchange_nyse"]')))
    driver.execute_script("arguments[0].click();", nyse_box)




    links = driver.find_elements_by_xpath(
        "//a[contains(., 'Acquisition') or contains(., 'Acquire') or contains(., 'Merger') "
        "or contains(., 'merger') or contains(., 'Combine') or contains(., 'Combination')]")

    # for elem in links:
    # print(elem.text)
    article = links[0]
    article_title = links[0].text
    # print(article)
    driver.implicitly_wait(10)
    article.click()

    article_textScrape = driver.find_elements_by_css_selector('#content-L2 > span')

    article_content = article_textScrape[0].text

    alert_ticker = driver.find_element_by_xpath("//p[contains(., '(NYSE:') or contains(., '(Nyse') "
                                                "or contains(., '(NYSEA:')]")


    alert_ticker = alert_ticker.text

    paranthesis_text = re.findall('\(.*?\)', alert_ticker)

    for item in paranthesis_text:
        if "NYSE" in item or "NYSEA" in item or "Nyse" in item:
            ticker_exp = item

            removable1 = "NYSE:"
            removable2 = "("
            removable3 = ")"
            removable1_1 = "NYSEA:"
            removable1_2 = "Nyse:"


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




    currentData.append(article_content)
    driver.quit()
    return article_content


def comparison(new_data):
    if new_data in pastData:
        return False
    else:
        return True

def email(article_content):

    article_content = M_A()
    msg = MIMEMultipart()
    x = 'sajjad@spartanfinance.io'
    msg['From'] = x
    msg['To'] = 'sajjad.abbas09@gmail.com'

    msg['Subject'] = 'MnA News Alert'

    message = article_content

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
    article_content = M_A()
    del currentData[:]
    M_A()
    if currentData is not None:
        for article_content in currentData:
            compare = comparison(article_content)
            if compare:
                pastData.append(article_content)
                email(article_content)
            else:
                print("Entry already present")
    else:
        print("Nothing found yet")





schedule.every(1).seconds.do(run)

while True:
    schedule.run_pending()



