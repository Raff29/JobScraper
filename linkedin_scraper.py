import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from proxy_validator import read_proxies, validate_proxy_format
import time
import random


def scrape(url, header, proxies=None, wait_time=5):
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--chromedirver-path = ./chromedriver.exe')

    user_agent = UserAgent().random
    options.add_argument(f'user-agent={user_agent}')
    
    proxies = read_proxies("http_proxies.txt")
    valid_proxies = []
    for proxy in proxies:
      if validate_proxy_format(proxy):
        valid_proxies.append(proxy)
        
    if valid_proxies:
      proxy = random.choice(valid_proxies)
      options.add_argument(f'--proxy-server={proxy}')

    driver = webdriver.Chrome(options=options)

    time.sleep(random.uniform(wait_time - 1, wait_time + 1))

    try:
      driver.get(url)

      last_height = driver.execute_script('return document.body.scrollHeight')
      while True:
          driver.execute_script(
              'window.scrollTo(0, document.body.scrollHeight);')
          time.sleep(random.uniform(0.5, 1))
          new_height = driver.execute_script('return document.body.scrollHeight')
          if new_height == last_height:
              break
          last_height = new_height

        html = driver.page.source
    except Exception as e:
      print(f"Error scrappin URL: {e}")
      html = ""

    driver.close()
    
    if html:
        soup = BeautifulSoup(html, 'html.parser')
    else:
      soup = None

    return soup


def extract_data(soup, target_element, title_selector, company_selector, location_selector, url_selector):

    data = []
    if soup:
        elements = soup.find_all(target_element)

        for element in elements:
            job_data = {}
            
            job_data["title"] = element.select_one(title_selector).text
            job_data["company"] = element.select_one(company_selector).text
            job_data["location"] = element.select_one(location_selector).text
            job_data["url"] = element.select_one(url_selector).get("href")
            
            data.append(job_data)

    return data

