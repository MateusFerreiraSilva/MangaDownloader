import requests

def get_chapters(driver, init, end):
	# download_list(img_srcs)
	pass

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
	download_list(img_srcs)

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

def download_list(img_srcs):
	with open('download_list.txt', 'w') as f:
		for img in img_srcs:
			f.write(f'{img}\n')