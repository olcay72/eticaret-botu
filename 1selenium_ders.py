import time
from selenium import webdriver

driver = webdriver.Chrome()

driver.get("https://www.google.com")

print(driver.title)

time.sleep(5)   ## açılan sayfanın hemen kapanmaması için süre ayarladık burda 5 saniye

