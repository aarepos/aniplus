import pickle
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


WEBSITE_URL = "https://aniplus.top/"
FIRST_SERIAL_PAGE = "https://aniplus.top/anime/type/serial?page=1"
COUNT_PAGE = 36

class Fox:

	anime_list_links = []

	def __init__(self):

		# run driver
		self.driver = webdriver.Firefox()
		self.driver.implicitly_wait(10)
		self.driver.get(WEBSITE_URL)

		# set cookie
		try:
			cookies = pickle.load(open("cookies.pkl", "rb"))
			for cookie in cookies:
				self.driver.add_cookie(cookie)
		except:
			pass



	def extract_anime_info(self):

		addr = "https://aniplus.top/anime/159?d-tab=3&d-type=link_series&link_series-3=1"
		self.driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
		self.driver.get(addr)


		try:
			while True:
				elem = self.driver.find_element_by_xpath("//*[text()[contains(., '›')]]")
				elem = elem.get_attribute("href")
				self.driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
				self.driver.get(elem)
				print("go to next page...")
		except:
			print("The end")


		print(elem.get_attribute("innerHTML"))

			





	def show(self):
		print(self.anime_list_links)


fox = Fox()
fox.extract_anime_info()