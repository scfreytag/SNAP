import socket
import threading
import json
import base64
import io
import PIL
from PIL import Image

TCP_IP = '127.0.0.1'
TCP_PORT = 12000
BUFFER_SIZE = 400024
MESSAGE_HELLO = '{"Start": "true"}'
MESSAGE_ENABLEIMAGE = '{"SendImage": "true"}'
MESSAGE_DISABLEIMAGE = '{"SendImage": "false"}'
MESSAGE_ENABLELOGIMAGE = '{"LogImage": "true"}'
MESSAGE_ENABLELOGIMAGE_PATH = '{{"LogImage": "true", "SetLogImagePath": "{0}"}}'
MESSAGE_DISABLELOGIMAGE = '{"LogImage": "false"}'
gazeCallbacks = []
imageCallbacks = []
positionCallbacks = []
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
thread_running = 0

def _gazeReceived(x,y,timestamp):
	for c in gazeCallbacks:
		c(x,y,timestamp)
		
def _imageReceived(imgdata):
	if imageCallbacks:
		bytes = base64.b64decode(imgdata)
		image = Image.open(io.BytesIO(bytes))
		for c in imageCallbacks:
			c(image)
		
def _positionReceived(lx,ly,lz,rx,ry,rz,timestamp):
	for c in positionCallbacks:
		c(lx,ly,lz,rx,ry,rz,timestamp)

def _readerThread():
	global thread_running
	thread_running = 1
	previous_data = ''
	try:
		while thread_running:
			data = previous_data + s.recv(BUFFER_SIZE).decode('utf-8')
			previous_data = ""
			if data:
				data_invalid_index = data.rfind("\n")
				data_valid = data[:data_invalid_index]
				previous_data = data[data_invalid_index:]
				datas = data_valid.split("\n")
				for da in datas:
					if not da:
						continue
					d = json.loads(da)
					if 'Acknowledge' in d:
                                          # took the print message out to avoid vl confusion
                                          pass
						#print ('Acknowledge: ', d['Acknowledge'])
					if 'Gaze' in d:
						_gazeReceived(d['Gaze']['x'],d['Gaze']['y'],d['Gaze']['timestamp'])
					if 'Image' in d:
						_imageReceived(d['Image'])
					if 'Position' in d:
						_positionReceived(d['Position']['left']['x'],d['Position']['left']['y'],d['Position']['left']['z'],d['Position']['right']['x'],d['Position']['right']['y'],d['Position']['right']['z'],d['Position']['timestamp'])
					
	finally:
		s.close()
		print ("connection closed.")

def send(msg):
	#s.send(bytes(msg,'utf-8'))
    s.send(bytes(msg))

def connect():
	s.connect((TCP_IP, TCP_PORT))
	send(MESSAGE_HELLO)
	t = threading.Thread(target=_readerThread)
	t.start()
	

def addGazeCallback(callback):
	gazeCallbacks.append(callback)
	
def addImageCallback(callback):
	imageCallbacks.append(callback)
	
def addPositionCallback(callback):
	positionCallbacks.append(callback)
	
def disconnect():
	global thread_running
	thread_running = 0
def enableSendImage():
	send(MESSAGE_ENABLEIMAGE)
	
def disableSendImage():
	send(MESSAGE_DISABLEIMAGE)
	
def enableLogImage():
	send(MESSAGE_ENABLELOGIMAGE)
	
def enableLogImage(path):
	send(MESSAGE_ENABLELOGIMAGE_PATH.format(path))
	
def disableLogImage():
	send(MESSAGE_DISABLELOGIMAGE)
