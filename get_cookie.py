import time
import pickle
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


driver = webdriver.Firefox()
driver.get("https://aniplus.top/login")

# button = driver.find_element_by_class_name("uk-button")
# email  = driver.find_element_by_id("email")
# passwd = driver.find_element_by_id("password")
# email.send_keys("gorgdis@gmail.com")
# passwd.send_keys("A1960622633a")

time.sleep(30)

# button.click()

# time.sleep(5)

pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))