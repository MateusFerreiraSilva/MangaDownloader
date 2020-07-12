from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import manga_getter as mg
import manga_downloader as md

def main():
	root_url = 'http://www.mangareader.net/berserk'

	options = Options()
	options.add_argument('--private')
	options.headless = True

	driver = webdriver.Firefox(options=options)

	mg.get_chapter(driver, root_url, 308)
	md.download_manga()

	driver.close()

main()