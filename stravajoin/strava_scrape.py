
from bs4 import BeautifulSoup
import requests
import re
import os
import operator
import datetime
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urljoin
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

class MyActivity:
    def __init__(self,type,date,title,time,dist,elev,gpx_url):
        self.activity_type=type
        self.date=date
        self.title=title
        self.time=time
        self.dist=dist
        self.elev=elev
        self.gpx_url=gpx_url


class ScrapeMyActivity:
    def __init__(self,email,password,driver):
        self.email=email
        self.password=password
        self.driver=driver
        self.datalist=[]

    @classmethod
    def get_instance(cls,email,password):

        options = Options()
        #options.add_argument('--headless')
        options.add_experimental_option('detach', True)

        driver=webdriver.Chrome(ChromeDriverManager().install(),options=options)
        driver.implicitly_wait(30)

        return cls(email,password,driver)


    def run(self):
        """
        Seleniumを使ってstravaにログインする。
        stravaにログインできた場合は、__scrapeメソッドを実行する。
        stravaにログインできない場合は、最大で3回リトライする。
        3回リトライしても成功しなかった場合は例外Exceptionを発生させる。
        また、リトライごとにSeleinumの待機時間を+10していく。
        """
        max_retries=3
        retries=0
        max_wait=50

        while True:
            try:
                self.driver.get('https://www.strava.com/athlete/training')
                WebDriverWait(self.driver,timeout=max_wait).until(EC.presence_of_all_elements_located)

                if self.driver.current_url == 'https://www.strava.com/login':
                    input_email=self.driver.find_element(By.CSS_SELECTOR,'input[id="email"]')
                    input_email.send_keys(self.email)
                    input_password=self.driver.find_element(By.CSS_SELECTOR,'input[id="password"]')
                    input_password.send_keys(self.password)
                    button_login=self.driver.find_element(By.CSS_SELECTOR,'button[id="login-button"]')
                    button_login.click()

                if self.driver.current_url == 'https://www.strava.com/athlete/training':
                    print('stravaにログイン成功!')
                    self.__scrape()
                    self.driver.quit()
                    break

            except:
                self.driver.quit()
                raise Exception('You accessed an unintended page')
                
            if retries>=max_retries:
                self.driver.quit()
                raise Exception('Too many retries')

            retries+=1
            wait=2**(retries-1)
            max_wait+=10*retries
            print(f'Waiting{wait}secconds...')
            sleep(wait)


    def __scrape(self):
        tr_list=self.driver.find_elements(By.CSS_SELECTOR,'tr[class="training-activity-row"]') 
                
        for tr in tr_list:
            training_td_dict={} #{'type':'activityのスポーツ名','date':'日付','title':'タイトル','time':'タイム','dist':'距離','elev':'獲得標高','gpx_url':'gpxファイルのurl'}
            for name in ['type','date','title','time','dist','elev']:
                td=tr.find_element(By.CSS_SELECTOR,f'td[class="view-col col-{name}"]')
                training_td_dict[name]=td.text
                if name == 'title':
                    url=td.find_element(By.CSS_SELECTOR,'a').get_attribute('href')
                    training_td_dict['gpx_url']=url+'/export_gpx'

            ma=MyActivity(**training_td_dict)
            self.datalist.append(ma)










