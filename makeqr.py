# Importing library
import qrcode
import requests
import sys

def getUrl(ip, port, endpoint):
	fullPath = 'http://' + ip + ':' + port + endpoint
	response = requests.get(fullPath).json()
	url = response['tunnels'][0]['public_url']
	print(url)
	return url


def genQRcode(url, filepath):
	# Creating an instance of QRCode class
	qr = qrcode.QRCode(version = 1,
				box_size = 10,
				border = 5)
	# Adding data to the instance 'qr'
	qr.add_data(url)
	qr.make(fit = True)
	img = qr.make_image(fill_color = 'black',
					back_color = 'white')
	img.save(filepath)
	return filepath


ngrokEndpoint = '/api/tunnels'
ngrokIP = '127.0.0.1'
ngrokPort = '4040'

if __name__ == '__main__':
	if len(sys.argv) < 2:
		raise ValueError('Missing QR Code Filepath. \n usage: python makeqr.py <output>')
	filepath = sys.argv[1]
	if len(sys.argv) == 3:
		url = sys.argv[2]
	else:
		url = getUrl(ngrokIP, ngrokPort, ngrokEndpoint)
	genQRcode(url, filepath)
	print(filepath)
