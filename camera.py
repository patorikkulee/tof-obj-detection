from picamera import PiCamera
from time import sleep
from datetime import datetime
from PIL import Image
import zbarlight


camera = PiCamera()

def take_pic(filename:str):
	# camera.start_preview()
	camera.capture(f"pictures/{filename}.jpg")
	# camera.stop_preview()

def qrdect():
	file_path = './qrtest.jpg'
	with open(file_path, 'rb') as img:
		image = Image.open(img)
		image.load()
	sleep(0.5)
	code = zbarlight.scan_codes(['qrcode'],image)
	print('QR code: %s' % code)

if __name__=='__main__':
	take_pic("123")
	# qrdect()
    