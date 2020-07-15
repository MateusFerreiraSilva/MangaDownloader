import os

def get_home_dir():
	return os.path.expanduser('~')

def create_dir(dir_name):
	if not os.path.isdir(dir_name):
		# makedirs beacuse parents dir are created
		os.makedirs(dir_name)