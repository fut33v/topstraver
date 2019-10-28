import time
from selenium import webdriver
from PIL import ImageOps
from PIL import Image


def get_screenshot(_email, _password, _club_id, _screenshot_file_name):
	options = webdriver.ChromeOptions()
	options.add_argument('--ignore-certificate-errors')
	options.add_argument("--test-type")
	options.add_argument("--headless")
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

	if len(i) != 4:
		exit(-1)

	email = i[0]
	password = i[1]
	club_id = i[2]
	screenshot_file_name = "scr.png"

	get_screenshot(email, password, club_id, screenshot_file_name)
	area = (340, 1153, 1180, 1903)
	crop_image(screenshot_file_name,"scr.png", area)

