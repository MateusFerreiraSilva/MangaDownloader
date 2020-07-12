import json
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from collections import Counter

# driver.getPageSource().contains("404");

def get_data():
	parodies, chars, tags, artists, groups = [], [], [], [], []
	l = [parodies, chars, tags, artists, groups]
	x_path = '/html/body/div[2]/div[1]/div[2]/div/section/'
	for x in range(0, 5):
		i = 1
		while True:
			aux = f'div[{x+1}]/span/a[{i}]'
			try:
				data = driver.find_element_by_xpath(x_path+aux).text
				data_name = data.split('(')[0].strip()
				l[x].append(data_name)
			except:
				break
			
			i += 1

	return l

def to_next_page():
	try:
		aux = driver.find_element_by_xpath('//*[@id="content"]/section')
		next_button = aux.find_element_by_class_name('next')
		next_button.click()
	except:
		driver.quit()
		
url = 'https://nhentai.net/login/'

options = Options()
options.add_argument('--private')
options.headless = True
driver = webdriver.Firefox(options=options)
driver.get(url)

username = driver.find_element_by_xpath('//*[@id="id_username_or_email"]')
password = driver.find_element_by_xpath('//*[@id="id_password"]')
login_button = driver.find_element_by_xpath('//*[@id="content"]/form/button') 

username.send_keys('shall03')
password.send_keys('43456037s')
login_button.click()

fav_pag = driver.find_element_by_xpath('/html/body/nav/div/ul[2]/li[1]/a')
fav_pag.click()

parodies_c, chars_c, tags_c, artists_c, groups_c = [Counter() for i in range(0, 5)]
counters = [parodies_c, chars_c, tags_c, artists_c, groups_c]

i = 1
while True:
	try:
		pag = driver.find_element_by_xpath(f'/html/body/div[2]/div/div[{i}]')
		pag.click()
		data = get_data()
		for x in range(0, 5):
			counters[x].update(data[x])
		driver.back()
	except:
		break

	if i == 25:
		i = 1
		to_next_page()
	else:
		i += 1

driver.quit()

with open('H_Tags.json', 'w', encoding='utf-8') as file:
	js = json.dumps(counters, indent=4)
	file.write(js)