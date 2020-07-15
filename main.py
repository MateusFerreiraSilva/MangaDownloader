import manga_downloader as md

def main():
	root_url = 'http://www.mangareader.net/berserk'
	md.get_chapters(root_url, 315, 316)
main()