import pickle
import selenium.webdriver

driver = selenium.webdriver.Firefox()

driver.get("https://aniplus.top/")

cookies = pickle.load(open("cookies.pkl", "rb"))
for cookie in cookies:
    driver.add_cookie(cookie)

driver.get("https://aniplus.top/")