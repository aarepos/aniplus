import pickle
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


WEBSITE_URL = "https://aniplus.top/"
FIRST_SERIAL_PAGE = "https://aniplus.top/anime/type/serial?page=1"
COUNT_PAGE = 36







def its_exists(driver):

	try:

		download_btn = driver.find_element_by_class_name("js-show-download-link")
		download_btn.click()

		sleep(2)

		download_box = driver.find_element_by_css_selector(".uk-alert > p")
		x = "لینک دانلودی برای این بخش آپلود نشده است"
		if download_box.get_attribute("innerHTML") == x:
			return False

		return True
	except:
		return True






def get_anime_info(driver, path):
	

	# open path, new tab
	driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
	driver.get(path)
	sleep(3)

	if not its_exists(driver):
		pritn("not exists:", path)
		return

	print("path:", path)
	sleep(2)
	return
	# get anime info




def get_anime_list(driver, count_of_page):
	
	page_url = FIRST_SERIAL_PAGE.split("=")[0] + count_of_page

	# go to page_url, open tab
	driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')
	driver.get(page_url)
	sleep(3)

	anime_list = driver.find_elements_by_css_selector(".post-anime > a")
	
	# print(anime_list)

	for i in anime_list:
		get_anime_info(driver, i.get_attribute("href"))
		# print(i.get_attribute("href"))
	


def main():

	# run driver
	driver = webdriver.Firefox()
	driver.implicitly_wait(10)
	driver.get(WEBSITE_URL)

	# set cookie
	try:
		cookies = pickle.load(open("cookies.pkl", "rb"))
		for cookie in cookies:
		    driver.add_cookie(cookie)
	except:
		pass

	# go to target page
	driver.get(FIRST_SERIAL_PAGE)

	# start crawling
	for page in range(1, COUNT_PAGE + 1):
		get_anime_list(driver, str(page))
		break

	# close driver
	driver.close()







if __name__ == "__main__":
	main()