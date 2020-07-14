import os
import requests
import shutil # to save it locally
import json
import concurrent.futures

# old way to do threads:

'''
# import threading

threads = list()
for img in chapter_imgs:
	aux = threading.Thread(target=download_img, args=(img, path, num))
	threads.append(aux)
	aux.start()
	num += 1

for index, thread in enumerate(threads):
	thread.join()
'''


def create_dir(dir_name):
	if not os.path.isdir(dir_name):
		# makedirs beacuse parents dir are created
		os.makedirs(dir_name)

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

		num = 1
		chapter_number = chapter_id.split('_')[1]
		print(f'Downloading chapter {chapter_number}...')

		with concurrent.futures.ThreadPoolExecutor() as executor:
			for img in chapter_imgs:
				executor.submit(download_img, img, path, num)
				num += 1

		print(f'Chapter {chapter_number} Downloaded!\n')

# download_manga_from_list()