from selenium import webdriver
import time 

driver = webdriver.Chrome()
driver.get("www.google.com")
time.sleep(5)
driver.quit()