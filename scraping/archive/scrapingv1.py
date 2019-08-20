from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import requests

#driver = webdriver.Chrome("/usr/lib/chromium-browser/chromedriver")
#driver.get("https://www.metal-archives.com/lists/A")

url = 'https://www.metal-archives.com/lists/A'
response = requests.get(url)

print(response)
soup = BeautifulSoup(response.text, "html.parser")
print(soup)
