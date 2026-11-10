import time
from selenium import webdriver

driver = webdriver.Chrome()

ur1 = ("https://www.github.com")

driver.get(ur1)
driver.maximize_window()            ## açılan pencereyi küçültür
#driver.set_window_size(375, 800)   ## pencereyi istediğimiz boyutlara ayarlarız 
#driver.minimize_window()

time.sleep(5)

driver.save_screenshot("github_screenshot.png")


driver.quit()