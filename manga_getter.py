from selenium.webdriver.common.keys import Keys
import requests
import json
import concurrent.futures
import time

def open_tab(driver):
	driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 't')

def close_tab(driver):
	driver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'w') 

def page_exist(site):
	try:
		r = requests.get(site)
		if r.status_code == 200:
			return True
	except:
		return False

def get_manga_name():
	pass

def get_chapters(driver, root_url, init, end):
	manga_name = 'Berserk'
	chapters = []

	# with concurrent.futures.ThreadPoolExecutor() as executor:
	# 	for i in range(init, end+1):
	# 		future = executor.submit(get_chapter, driver, root_url, i)
	# 		chapter = future.result
	# 		chapters.append(chapter)

	for i in range(init, end+1):
		chapter = get_chapter(driver, root_url, i)
		chapters.append(chapter)

	create_download_list({'manga_name' : manga_name, 'chapters' : chapters})

def get_chapter(driver, root_url, chapter_num):
	chapter_url = f'{root_url}/{chapter_num}'

	# get all pages
	page_num = 1
	img_srcs = []
	print(f'getting chapter {chapter_num}...')
	
	with concurrent.futures.ThreadPoolExecutor() as executor:
		while True:
			future = executor.submit(get_page_src, driver, chapter_url, page_num, chapter_num)
			result = future.result()

			if result == '404':
				break

			img_srcs.append(result)
			page_num += 1

	print(f'chapter {chapter_num} successfully getted!')
	return {f'Chapter_{chapter_num}' : img_srcs}

def get_page_src(driver, chapter_url, num, chapter_num):
	page_url = f'{chapter_url}/{num}'

	if page_exist(page_url):
		print(f'\tgetting page {num} of chapter {chapter_num}...')
		
		open_tab(driver)
		driver.get(page_url)
		# time.sleep(0.5)

		img = driver.find_element_by_xpath('//*[@id="img"]')
		close_tab(driver)

		src = img.get_attribute('src')
		return src

	else:
		return '404'

def create_download_list(manga_data):
	with open('download_list.json', 'w', encoding='utf-8') as file:
		js = json.dumps(manga_data, indent=4)
		file.write(js)