
import manga_getter as mg

def main():
	root_url = 'http://www.mangareader.net/berserk'

	mg.get_chapters(root_url, 313, 314)

main()