from picamera import PiCamera
from time import sleep
from datetime import datetime
from PIL import Image
import zbarlight

def shoot_video(filename:str):
	camera = PiCamera()
	#camera.start_preview()
	camera.start_recording(f"videos/{filename}.mp4")
	sleep(3)
	camera.stop_recording()
	#camera.stop_preview()
	camera.close()

def take_pic(filename:str):
	camera = PiCamera()
	# camera.start_preview()
	camera.capture(f"pictures/{filename}.jpg")
	camera.close()
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
	#take_pic("123")
	# qrdect()
	shoot_video("123")
    
