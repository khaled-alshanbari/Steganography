# Python program implementing Image Steganography

# PIL module is used to extract
# pixels of image and modify it
import os
import random
from tkinter import filedialog

from PIL import Image


def get_Desktop():
    desktop = os.path.join(os.path.join(os.path.expanduser('~')), 'Desktop')
    return desktop

# Convert encoding data into 8-bit binary
# form using ASCII value of characters
def genData(data):

		# list of binary codes
		# of given data
		newd = []

		for i in data:
			newd.append(format(ord(i), '08b'))
		return newd

# Pixels are modified according to the
# 8-bit binary data and finally returned
def modPix(pix, data):

	datalist = genData(data)
	lendata = len(datalist)
	imdata = iter(pix)

	for i in range(lendata):

		# Extracting 3 pixels at a time
		pix = [value for value in imdata.__next__()[:3] +
								imdata.__next__()[:3] +
								imdata.__next__()[:3]]

		# Pixel value should be made
		# odd for 1 and even for 0
		for j in range(0, 8):
			if (datalist[i][j] == '0' and pix[j]% 2 != 0):
				pix[j] -= 1

			elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
				if(pix[j] != 0):
					pix[j] -= 1
				else:
					pix[j] += 1
				# pix[j] -= 1

		# Eighth pixel of every set tells
		# whether to stop ot read further.
		# 0 means keep reading; 1 means thec
		# message is over.
		if (i == lendata - 1):
			if (pix[-1] % 2 == 0):
				if(pix[-1] != 0):
					pix[-1] -= 1
				else:
					pix[-1] += 1

		else:
			if (pix[-1] % 2 != 0):
				pix[-1] -= 1

		pix = tuple(pix)
		yield pix[0:3]
		yield pix[3:6]
		yield pix[6:9]

def encode_enc(newimg, data):
	w = newimg.size[0]
	(x, y) = (0, 0)

	for pixel in modPix(newimg.getdata(), data):

		# Putting modified pixels in the new image
		newimg.putpixel((x, y), pixel)
		if (x == w - 1):
			x = 0
			y += 1
		else:
			x += 1

# Encode data into image
def encode():
	img= str(filedialog.askopenfilename(initialdir=get_Desktop(), title='Select a Picture file')).strip()
	print('image path : ',img)
	temp = img.split('.')[1].upper()
	img = img.split('.')[0]+'.'+temp
	print(img)
	image = Image.open(img, 'r')

	data = input("Enter data to be encoded : ")
	if (len(data) == 0):
		raise ValueError('Data is empty')

	newimg = image.copy()
	encode_enc(newimg, data)

	new_img_name = input(f"Enter the name of new image(WITHOUT extension) : {get_Desktop()}/ ")
	new_img_name+='.png'
	try:
		newimg.save(get_Desktop()+"/"+new_img_name, str(new_img_name.split(".")[1].upper()))
	except Exception:
		newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))
	print("Text has been embeded successfully")
	newimg.show()

# Decode the data in the image
def decode():
	img = str(filedialog.askopenfilename(initialdir=get_Desktop(), title='Select a Picture file')).strip()
	image = Image.open(img, 'r')

	data = ''
	imgdata = iter(image.getdata())

	while (True):
		pixels = [value for value in imgdata.__next__()[:3] +
								imgdata.__next__()[:3] +
								imgdata.__next__()[:3]]

		# string of binary data
		binstr = ''

		for i in pixels[:8]:
			if (i % 2 == 0):
				binstr += '0'
			else:
				binstr += '1'

		data += chr(int(binstr, 2))
		if (pixels[-1] % 2 != 0):
			return data

# Main Function
def mainSteg():
	a = int(input(":: Welcome to Steganography ::\n"
						"1. Encode\n2. Decode\n --> "))
	if (a == 1):
		encode()

	elif (a == 2):
		print("Decoded Word : " + decode())
	else:
		raise Exception("Enter correct input")

def EncodeArabic():
	space = '100000'
	harakat = ['ً','ِ','ٍ','ُ','ٌ','ٌ','ْ','ّ','ّ']
	fatha = 'َ'
	msg = input("Enter the arabic word : ")
	secretmsg = input("Enter the Secret message in English : ")
	cipherTextBinary=''
	EmbedText=''
	for i in secretmsg:
		cipherTextBinary+=str(bin(ord(i))).split('0b')[1]
		cipherTextBinary+=" "
	for i in range(len(cipherTextBinary)):
		EmbedText+=msg[i]
		if cipherTextBinary[i] == '1':
			EmbedText+=fatha
		elif cipherTextBinary[i] =='0':
			EmbedText+=harakat[random.randint(0,8)]
	with open('secret.txt','w+') as file:
		file.write(EmbedText)
		print("file was saved")
	print('Result: ',EmbedText)


def DecodeArabic():
	msg = input("Enter the arabic secret word : ")
	harakat = ['ً', 'ِ', 'ٍ', 'ُ', 'ٌ', 'ٌ', 'ْ', 'ّ', 'ّ']
	fatha = 'َ'
	PlainText=''
	PlainTextD=''
	Decrypted=[]
	Converted =[]
	for i in msg:
		if i == fatha:
			PlainText+='1'
		elif i in harakat:
			PlainText+='0'
	counter=0
	for i in PlainText:
		counter += 1
		PlainTextD+=i
		if PlainTextD == '100000':
			Decrypted.append(PlainTextD)
			counter =0
			PlainTextD =''
			continue
		if counter == 7:
			counter =0
			Decrypted.append(PlainTextD)
			PlainTextD = ''


	for i in Decrypted:
		Converted.append('0b'+i)
	numbers = []
	PlainText=''
	for i in Converted:

		numbers.append(int(i,2))
	for i in numbers:
		PlainText+= chr(i)
	print('Result : ',PlainText)
def mainStegArabic():

	msg = int(input(":: Welcom to arabic Steganography :: \n 1. Encode \n 2. decode \n -->"))
	if msg == 1:
		EncodeArabic()
	elif msg == 2:
		DecodeArabic()
	else:
		print("Error, goodbye")

if __name__ == '__main__' :


	GreetingMsg="Hello, choose what type of Steganography method you would like to use\n[+] Enter 1 to hide text in a pictre\n[+] Enter 2 to hide text in Arabic words\n[+]"

	print(GreetingMsg)
	choice = int(input("->"))

	if choice == 1:
		mainSteg()
	elif choice == 2:
		mainStegArabic()
temp = '1101101 1110010 100000 1101000 1110101 1110011 1110011 1100001 1101001 1101110'
