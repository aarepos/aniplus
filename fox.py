import re
import uuid
import pickle
import hashlib
from time import sleep
from selenium import webdriver
from urllib.parse import unquote
from tinydb import TinyDB, Query
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options


WEBSITE_URL = "https://aniplus.top/"
FIRST_SERIAL_PAGE = "https://aniplus.top/anime/type/serial?page=1"
COUNT_PAGE = 36

class Fox:

	anime_list_links = []

	def __init__(self):

		# run driver
		options = Options()
		options.add_argument('--headless')
		self.driver = webdriver.Firefox(options=options)
		self.driver.implicitly_wait(10)
		self.driver.get(WEBSITE_URL)

		# set cookie
		try:
			cookies = pickle.load(open("cookies.pkl", "rb"))
			for cookie in cookies:
				self.driver.add_cookie(cookie)
		except:
			pass


	def check_point(self):
		try:
			boxes = self.driver.find_elements_by_css_selector("div.uk-alert > p")
			for box in boxes:
				box = box.get_attribute("innerHTML")
				x   = "لینک دانلودی برای این بخش آپلود نشده است"
				if box == x:
					return False

			return True
		except:
			return True


	def get_other_titles(self):
		
		all_titles = []
		
		try:
			other_titles = self.driver.find_element_by_css_selector("div.other-titles > div")
			other_titles = other_titles.find_elements_by_class_name("value")

			
			for title in other_titles:
				title = title.get_attribute("innerHTML")

				if len(title) > 30:
					continue

				all_titles.append(title)
		except:
			pass

		return all_titles



	def extract_anime_list(self, page_number):
		
		page_url = FIRST_SERIAL_PAGE.split("=")[0] + str(page_number)

		# go to page_url, open tab
		self.driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
		self.driver.get("https://aniplus.top/anime/type/serial?page=3")

		sleep(1)

		
		anime_list_elements = self.driver.find_elements_by_css_selector(".post-anime > a")

		for anime in anime_list_elements:
			self.anime_list_links.append(anime.get_attribute("href"))


	def extract_anime_info(self):

		for anime in self.anime_list_links:

			anime_id = str(uuid.uuid4())

			sleep(1)
			# go to anime url, open tab
			self.driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
			self.driver.get(anime)

			try:
				# anime name
				self.anime_name = self.driver.find_element_by_tag_name("h1").get_attribute("innerHTML")
			except:
				continue

			if self.check_point() == False: continue

			# anime other names
			self.other_titles = self.get_other_titles()

			# anime cover
			get_cover = self.driver.find_element_by_css_selector("div.box-img > img")
			self.cover = get_cover.get_attribute("src")

			show_btn = self.driver.find_element_by_class_name("js-show-download-link")
			show_btn.click()

			sleep(1)

			elems = self.driver.find_elements_by_xpath("//a[@href]")
			links = {}
			m = hashlib.sha256()

			q = Query()
			db = TinyDB("database/db.json")
			for elem in elems:
				hreff = elem.get_attribute("href")
				href  = unquote(hreff)

				if href[-3:] != "mkv":
					continue

				try:
					m.update(href.encode())
					pre_title = href.split("/")[-1].replace("%20", " ")
					link_title = re.match(r"\[.*\](.*)\[.*\]\.mkv", pre_title).group(1).strip()
					links[link_title] = hreff
				except:
					print("ERROR:", href)
					continue

			try:
				while True:
					elem = self.driver.find_element_by_xpath("//*[text()[contains(., '›')]]")
					elem = elem.get_attribute("href")
					self.driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
					self.driver.get(elem)
					elems = self.driver.find_elements_by_xpath("//a[@href]")
					for elem in elems:
						hreff = elem.get_attribute("href")
						href  = unquote(hreff)

						if href[-3:] != "mkv":
							continue

						try:
							m.update(href.encode())
							pre_title = href.split("/")[-1].replace("%20", " ")
							link_title = re.match(r"\[.*\](.*)\[.*\]\.mkv", pre_title).group(1).strip()
							links[link_title] = hreff
						except:
							print("ERROR:", href)
							continue

			except:
				pass

			get_hash = m.hexdigest()

			search_for_anime = TinyDB("database/db.json").search(q.sha256 == get_hash)
			if len(search_for_anime) != 0:
				print(f"SKIP: {self.anime_name}")
				continue


			db.insert({
				"uuid": anime_id,
				"sha256": get_hash,
				"title": self.anime_name,
				"other_titles": self.other_titles,
				"cover": self.cover,
				"links": links
			})

			
			leng = len(TinyDB("database/db.json").all())
			print(f"{leng}: {self.anime_name} added.")
		# print(elem.get_attribute("innerHTML"))

			# with open(f"links/{self.anime_name}.txt", "a") as f:
			# 	for elem in elems:
			# 		href = elem.get_attribute("href")

			# 		if href[-3:] != "mkv":
			# 			continue

			# 		f.write(href + "\n")


			





	def show(self):
		print(self.anime_list_links)


# 1 2
fox = Fox()
fox.extract_anime_list(2)
fox.extract_anime_info()