from dir_func import get_home_dir, create_dir
import driver_func as drv
import requests
import json
import concurrent.futures
import shutil # to save it locally
import sys
import time

home = get_home_dir() 

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

def get_manga_name(driver):
	try:
		name_xpath = '/html/body/div[1]/div[2]/div[1]/div[2]/table/tbody/tr[1]/td[2]/h2'
		name = driver.find_element_by_xpath(name_xpath).text
		return name
	except:
		print('Error getting manga name')
		return ''

def get_chapters(root_url, init, end):
	try:
		driver = drv.create_driver()
		driver.get(root_url)
	except:
		print('Error to acess manga page')
		sys.exit(1)

	manga_name = get_manga_name(driver)
	chapters = []

	with concurrent.futures.ThreadPoolExecutor() as executor:
		for i in range(init, end+1):
			future = executor.submit(get_chapter, driver, root_url, i, manga_name)
			chapter = future.result()
			chapters.append(chapter)

	drv.close_driver(driver)


	# create_download_list({'manga_name' : manga_name, 'chapters' : chapters})

def get_chapter(driver, root_url, chapter_num, manga_name):
	chapter_url = f'{root_url}/{chapter_num}'
	
	path = f'{home}/Downloads/Manga/{manga_name}/Chapter_{chapter_num}/'
	create_dir(path)

	# get all pages
	page_num = 1
	img_srcs = []
	print(f'getting chapter {chapter_num}...')
	
	with concurrent.futures.ThreadPoolExecutor() as executor:
		while True:
			future = executor.submit(
					get_page, driver, chapter_url, page_num,
					chapter_num, manga_name, path)
			result = future.result()

			if result == '404':
				break
			elif result == 'unknow_error':
				continue
			else:
				img_srcs.append(result)
				page_num += 1

	print(f'chapter {chapter_num} successfully getted!')
	# return {f'Chapter_{chapter_num}' : img_srcs}

def get_page(driver, chapter_url, num, chapter_num, manga_name, path):
	page_url = f'{chapter_url}/{num}'

	if page_exist(page_url):
		print(f'\tgetting page {num} of chapter {chapter_num}...')
		try:
			drv.open_tab(driver)
			driver.get(page_url)

			img = driver.find_element_by_xpath('//*[@id="img"]')
			src = img.get_attribute('src')

			drv.close_tab(driver)

			download_img(src, path, num)
			return 'OK'

		except:
			print(f'\tA Error getting page {num} of chapter {chapter_num}')
			print('\tTrying again....')
			return 'unknow_error'

	else:
		return '404'

def download_img(img, path, num):
	r = requests.get(img, stream=True)

	if r.status_code == 200:
		# Set decode_content value to True, otherwise the downloaded image file's size will be zero.
		r.raw.decode_content = True

		filename = f'page_{num}.jpg'

		with open(path+filename,'wb') as f:
			shutil.copyfileobj(r.raw, f)

		print(f'\tPage {num} Downloaded')
	else:
		print(f'\tPage {num} Couldn\'t be retreived')


#
#

# beta functions: 

#
#

# write a json file with the links of files to
def create_download_list(manga_data):
	with open('download_list.json', 'w', encoding='utf-8') as file:
		js = json.dumps(manga_data, indent=4)
		file.write(js)

# read json file and download files
def download_manga_from_list():
	with open('download_list.json', 'r') as file:
		manga_data = json.load(file)

	manga_name = manga_data['manga_name']
	chapters = manga_data['chapters']

	home = get_home_dir()

	for chapter in chapters:
		chapter_id = list(chapter.keys())[0]
		chapter_imgs = list(chapter.values())[0]

		path = f'{home}/Downloads/Manga/{manga_name}/{chapter_id}/'
		create_dir(path)

		num = 1
		chapter_number = chapter_id.split('_')[1]
		print(f'Downloading chapter {chapter_number}...')

		with concurrent.futures.ThreadPoolExecutor() as executor:
			for img in chapter_imgs:
				executor.submit(download_img, img, path, num)
				num += 1

		print(f'Chapter {chapter_number} Downloaded!\n')