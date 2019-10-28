## topstraver
take a screenshot of strava club leaderbord with selenium chrome webdriver and post it to vk wall

dependencies: python3, java, python selenium, webdriver, chromium, Pillow, vk api python

pip3 install Pillow selenium vk

webdriver download: https://chromedriver.chromium.org/downloads
(put it on $PATH)

## usage: 
* fill file with name 'input' like this: "email:password:club\_id:vk\_token:vk\_club\_id"
* python3 screenshot.py

## VK
* add new Standalone app, authorize in it and get VK Token with scope=offline,photos,wall
