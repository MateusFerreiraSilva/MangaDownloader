import os
import requests
import shutil # to save it locally
import json

def create_dir(dir_name):
	if not os.path.isdir(dir_name):
		# makedirs beacuse parents dir are created
		os.makedirs(dir_name)

# def download_manga_from_list_txt():
# 	home = os.path.expanduser('~')
# 	path = home + '/Downloads/Manga/'
# 	if not os.path.isfile(path):
# 		os.mkdir(path)

# 	i = 1
# 	images = open('download_list.txt', 'r')
# 	for image in images:		
# 		# strip removes \n
# 		link = image.strip()
# 		r = requests.get(link, stream = True)
# 		if r.status_code == 200:
# 			# Set decode_content value to True, otherwise the downloaded image file's size will be zero.
# 			r.raw.decode_content = True

# 			filename = f'page{i}.jpg'

# 			with open(path+filename,'wb') as f:
# 				shutil.copyfileobj(r.raw, f)

# 			print(f'\tPage {i} Downloaded')
# 		else:
# 			print(f'\tPage {i} Couldn\'t be retreived')
# 		i += 1

def download_manga_from_list():
	with open('download_list.json', 'r') as file:
		manga_data = json.load(file)

	manga_name = manga_data['manga_name']
	chapters = manga_data['chapters']

	home = os.path.expanduser('~')

	for chapter in chapters:
		chapter_id = list(chapter.keys())[0]
		chapter_imgs = list(chapter.values())[0]

		path = f'{home}/Downloads/Manga/{manga_name}/{chapter_id}/'
		create_dir(path)

		i = 1
		chapter_number = chapter_id.split('_')[1]
		print(f'Downloading chapter {chapter_number}...')
		for img in chapter_imgs:
			r = requests.get(img, stream=True)

			if r.status_code == 200:
				# Set decode_content value to True, otherwise the downloaded image file's size will be zero.
				r.raw.decode_content = True

				filename = f'page_{i}.jpg'

				with open(path+filename,'wb') as f:
					shutil.copyfileobj(r.raw, f)

				print(f'\tPage {i} Downloaded')
			else:
				print(f'\tPage {i} Couldn\'t be retreived')
			i += 1
		print(f'Chapter {i} Downloaded!\n')

download_manga_from_list()

# download_manga_from_list_txt()