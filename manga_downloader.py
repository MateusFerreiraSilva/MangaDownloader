import requests
import shutil # to save it locally

def download_manga():
	i = 1
	images = open('download_list.txt', 'r')
	for image in images:
		filename = f'page{i}.jpg'

		# strip removes \n
		r = requests.get(image.strip(), stream = True)
		if r.status_code == 200:
			# Set decode_content value to True, otherwise the downloaded image file's size will be zero.
			r.raw.decode_content = True

			# Open a local file with wb ( write binary ) permission.
			with open(filename,'wb') as f:
				shutil.copyfileobj(r.raw, f)

			print('Page {i} Downloaded: ', filename)
		else:
			print('Image Couldn\'t be retreived')
		i += 1

download_manga()