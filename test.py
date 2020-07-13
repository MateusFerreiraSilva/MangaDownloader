import json

with open('download_list.json', 'r') as file:
	manga_data = json.load(file)

	manga_name = manga_data['manga_name']
	chapters = manga_data['chapters']

	for chapter in chapters:
		chapter_id = list(chapter.keys())[0]
		chapter_imgs = list(chapter.values())[0]

		print(chapter_id)