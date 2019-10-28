import time
from selenium import webdriver
from PIL import ImageOps
from PIL import Image

import vk

import sys
import urllib.request
import urllib.parse
import base64
import requests
import json


def get_screenshot(_email, _password, _club_id, _screenshot_file_name):
	options = webdriver.ChromeOptions()
	options.add_argument('--ignore-certificate-errors')
	options.add_argument("--test-type")
	options.add_argument("--headless")
	options.add_argument("--lang=ru")
	options.binary_location = "/usr/bin/chromium-browser"
	driver = webdriver.Chrome(chrome_options=options)

	driver.set_window_position(0, 0)
	driver.set_window_size(1920, 2048)

	driver.get('https://strava.com/login')

	email = driver.find_element_by_id("email")
	email.send_keys(_email)

	password = driver.find_element_by_id("password")
	password.send_keys(_password)

	driver.find_element_by_id("login-button").click()

	print("sleep for 5 seconds...")
	time.sleep(5)


	driver.get("https://www.strava.com/clubs/{}/leaderboard".format(_club_id))

	driver.find_element_by_class_name("last-week").click()

	print("sleep for 2 seconds...")
	time.sleep(5)

	driver.save_screenshot(_screenshot_file_name)

	driver.close()


def crop_image(_input_file, _output_file, _area):
	img = Image.open(_input_file)
	cropped_img = img.crop(_area)
	cropped_img.save(_output_file, "PNG")


if __name__ == "__main__":

	f = open("input", 'r')
	i = f.readline()
	i = i.split(':')

	print (i)

	if len(i) < 6:
		exit(-1)

	email = i[0]
	password = i[1]
	club_id = i[2]

	vk_token = i[3]
	vk_club_id = int(i[4])

	if (len(i) > 6):
		area = tuple( map(int, i[5].split(','))  )
	else:
		area = (340, 1153, 1180, 1903)

	print("will be cropping to:", area)

	scr_fname = "scr.png"

	get_screenshot(email, password, club_id, scr_fname)
	crop_image(scr_fname, scr_fname, area)

	session = vk.Session(access_token=vk_token)
	vkapi = vk.API(session, v="5.35")
	time.sleep(0.5)

	data = vkapi.photos.getWallUploadServer(group_id=-vk_club_id)
	DATA_UPLOAD_URL = data['upload_url']

	r = requests.post(DATA_UPLOAD_URL, files={'photo': open(scr_fname,"rb")})
	if r.status_code != requests.codes.ok:
		print ("failed to POST photo!")
		exit(-1)
	params = {'server': r.json()['server'], 'photo': r.json()['photo'], 'hash': r.json()['hash'], 'group_id': -int(vk_club_id)}

	wallphoto = vkapi.photos.saveWallPhoto(**params)
	print(wallphoto)

	photo_id = wallphoto[0]['id']
	photo_owner = wallphoto[0]['owner_id']

	params = {'attachments': 'photo' + str(photo_owner) + '_' + str(photo_id), 'message': '#накатали@53cycling'}
	params['owner_id'] = vk_club_id
	print(params)

	vkapi.wall.post(**params)

