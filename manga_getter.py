import requests
import json

def get_manga_name():
	pass

def get_chapters(driver, root_url, init, end):
	manga_name = 'Berserk'
	chapters = []

	for i in range(init, end+1):
		chapters.append(get_chapter(driver, root_url, i))

	download_list({'manga_name' : manga_name, 'chapters' : chapters})

def get_chapter(driver, root_url, num):
	chapter_url = f'{root_url}/{num}'

	# get all pages
	i = 1
	img_srcs = []
	print(f'getting chapter {num}...')
	while True:
		aux = get_page_src(driver, chapter_url, i)
		if aux == '404':
			break

		img_srcs.append(aux)
		i += 1

	print(f'chapter {num} successfully getted!')
	return {f'Chapter_{num}' : img_srcs}

def get_page_src(driver, chapter_url, num):
	page_url = f'{chapter_url}/{num}'

	if page_exist(page_url):
		print(f'\t\tgetting page {num}...')
		driver.get(page_url)

		img = driver.find_element_by_xpath('//*[@id="img"]')
		src = img.get_attribute('src')

		return src

	else:
		return '404'

def page_exist(site):
    r = requests.get(site)
    if r.status_code == 200:
    	return True
    else:
    	return False

def download_list(manga_data):
	with open('download_list.json', 'w', encoding='utf-8') as file:
		js = json.dumps(manga_data, indent=4)
		file.write(js)
	
	# with open('download_list.txt', 'w') as f:
	# 	for img in img_srcs:
	# 		f.write(f'{img}\n')