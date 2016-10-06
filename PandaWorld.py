from direct.showbase.DirectObject import DirectObject
from panda3d.core import *
from direct.gui.DirectGui import *

class World:


	def __init__(self):
			self.title = OnscreenText(text="A Panda world w/o SNAP",
			  style=1, fg=(1,1,1,1), pos=(0.8,-0.95), scale = .07)
			self.lslValues = OnscreenText(text="0",
			  style=1, fg=(1,1,1,1), pos=(0.3,0), scale = .03)
			#Make the background color black (R=0, G=0, B=0)
			#instead of the default grey
			base.setBackgroundColor(0, 0, 0)
	
			#By default, the mouse controls the camera.	 Often, we disable that so that
			#the camera can be placed manually (if we don't do this, our placement
			#commands will be overridden by the mouse control)
			base.disableMouse()
	
			#Set the camera position (x, y, z)
			camera.setPos(0, 0, 45)
	
			#Set the camera orientation (heading, pitch, roll) in degrees
			camera.setHpr(0, -90, 0)

	def processLSLSamples(self, aSampleSet):
		text = '\n'.join(str(x) for x in aSampleSet) 
		self.lslValues.setText(text)

	def processGaze(self, x, y,ts):
		self.lslValues.setText(str(x) + ' ' + str(y) + ' ' + str(ts)) 
		
	def Update(self, task):
		pass