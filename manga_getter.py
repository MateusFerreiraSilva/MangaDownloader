from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from manga_downloader import download_img, get_home_dir, create_dir
import requests
import json
import concurrent.futures
import time

home = get_home_dir()

def create_driver():
	options = Options()
	options.add_argument('--private')
	options.headless = True

	driver = webdriver.Firefox(options=options)

	return driver

def close_driver(driver):
	driver.quit()

def open_tab(driver):
	driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')

def close_tab(driver):
	driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'w') 

def page_exist(site):
	while True:
		try:
			r = requests.get(site)
			break
		except:
			print(f'fail to access: {site}')
	
	if r.status_code == 200:
		return True
	return False

def get_manga_name():
	pass

def get_chapters(root_url, init, end):
	driver = create_driver()

	manga_name = 'Berserk'
	chapters = []

	with concurrent.futures.ThreadPoolExecutor() as executor:
		for i in range(init, end+1):
			future = executor.submit(get_chapter, driver, root_url, i, manga_name)
			chapter = future.result()
			chapters.append(chapter)

	close_driver(driver)

	# create_download_list({'manga_name' : manga_name, 'chapters' : chapters})

def get_chapter(driver, root_url, chapter_num, manga_name):
	chapter_url = f'{root_url}/{chapter_num}'
	
	path = f'{home}/Downloads/Manga/{manga_name}/{chapter_num}/'
	create_dir(path)

	# get all pages
	page_num = 1
	img_srcs = []
	print(f'getting chapter {chapter_num}...')
	
	with concurrent.futures.ThreadPoolExecutor() as executor:
		while True:
			future = executor.submit(
					get_page_src, driver, chapter_url, page_num,
					chapter_num, manga_name, path)
			result = future.result()

			if result == '404':
				break

			elif result == 'unknow_error':
				# try again
				page_num -= 1

			img_srcs.append(result)
			page_num += 1

	print(f'chapter {chapter_num} successfully getted!')
	# return {f'Chapter_{chapter_num}' : img_srcs}

def get_page_src(driver, chapter_url, num, chapter_num, manga_name, path):
	page_url = f'{chapter_url}/{num}'

	if page_exist(page_url):
		print(f'\tgetting page {num} of chapter {chapter_num}...')
		try:
			open_tab(driver)
			driver.get(page_url)

			img = driver.find_element_by_xpath('//*[@id="img"]')
			src = img.get_attribute('src')

			close_tab(driver)

			download_img(src, path, num)
			return 'OK'

		except:
			print(f'\tA Error getting page {num} of chapter {chapter_num}')
			print('\tTrying again....')
			return 'unknow_error'

	else:
		return '404'

def create_download_list(manga_data):
	with open('download_list.json', 'w', encoding='utf-8') as file:
		js = json.dumps(manga_data, indent=4)
		file.write(js)