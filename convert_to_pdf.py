import os
import img2pdf
from dir_func import get_home_dir

def chapter_to_pdf(path, chapter, manga_name):
	dirname = path+chapter
	os.chdir(dirname)
	# convert all files ending in .jpg inside a directory
	with open(f"{manga_name}_{chapter}.pdf","wb") as file:
		imgs = []
		for fname in os.listdir(dirname):
			if not fname.endswith(".jpg"):
				continue
			img = os.path.join(dirname, fname)
			if os.path.isdir(img):
				continue
			imgs.append(img)
		file.write(img2pdf.convert(imgs))

def all_chapter_to_pdf(path, manga_name):
	os.chdir(path)
	chapters = os.listdir()

	for chapter in chapters:
		chapter_to_pdf(path, chapter, manga_name)

manga_name = 'Berserk'
path_to_chapters = get_home_dir() + f'/Downloads/Manga/{manga_name}/'

all_chapter_to_pdf(path_to_chapters, manga_name)