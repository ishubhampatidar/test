from PIL import Image, ImageFont, ImageDraw
import io
import pyqrcode
from base64 import b64encode
import eel
import os

eel.init("web")

img = ''
@eel.expose
def generate_qr(data):
	global img
	img = pyqrcode.create(data)
	buffers = io.BytesIO()
	img.png(buffers, scale=8)
	encoded = b64encode(buffers.getvalue()).decode("ascii")
	print("QR code generation successful.")
	return "data:image/png;base64, " + encoded

@eel.expose
def save_qr_image(file):
	
	os.makedirs('qr_image', exist_ok = True)
	img.png(f'./qr_image/{file}.png', scale=6, module_color=[0, 0, 0, 128])  #background=[0xff, 0xff, 0xcc]

	image = Image.open(f'./qr_image/{file}.png')
	width, height = image.size
	draw = ImageDraw.Draw(image)
	font = ImageFont.truetype(r'GothamBold.ttf', 24)
	text_width, text_height = draw.textsize(file, font=font)
	print(width, height)
	position = int((width / 2) - (text_width / 1.5)), int(height - 20)
	draw.text(position, file.upper(), fill ="black", font = font)
	image.save(f'./qr_image/{file}.png')
	print(f'{file}.png, saved successfully')


eel.start("index.html", size=(1000,600))