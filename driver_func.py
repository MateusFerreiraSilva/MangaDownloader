from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys

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