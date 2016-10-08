from direct.showbase.DirectObject import DirectObject
from panda3d.core import *
from direct.gui.DirectGui import *
from Tkinter import *
import time
import random

class World:


    def __init__(self):
        self.root = Tk()
        self.screenWidth = self.root.winfo_screenwidth()

        #control

        self._updateRate = 10

        self.shouldRun = False

        #tkinter variables
        self.screenWidth = self.root.winfo_screenwidth()
        self.screenHeight = self.root.winfo_screenheight()
        
        self.halfWidth = int(self.screenWidth/2)
        self.halfHeight = int(self.screenHeight/2)

        self.thirdHeight = int(self.screenHeight/3)
        self.thirdWidth = int(self.screenWidth/3)
        
        self.fifthInnerWidt = int(self.thirdWidth/5)
        #change here if width changes
        self.coord_start = int(self.thirdWidth+ self.fifthInnerWidt)

        self._canvasColor = "black"
        self._gridColor = "grey50"
        self._innerGridColor = "grey20"

        self._upperOffset = 50

        # game
        self.coords_line1 = (self.coord_start, 0, self.coord_start, self.screenHeight)


        self.dict_of_lines = {0,0,0,0,0}

        # -> make blocks as objects
        
        

        #panda 3D stuff
        self.title = OnscreenText(text="A Panda world w/o SNAP",style=1, fg=(1,1,1,1), pos=(0.8,-0.95), scale = .07)
        self.lslValues = OnscreenText(text="0",style=1, fg=(1,1,1,1), pos=(0.3,0), scale = .03)
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

    def test(self):
        print("Test!")

    def processGaze(self, x, y,ts):
        self.lslValues.setText(str(x) + ' ' + str(y) + ' ' + str(ts))
    
    def Update(self, task):
       pass

    ## end panda3D stuff

    def createScreen(self):
        self.canvas = Canvas(self.root, width = self.screenWidth, height = self.screenHeight, highlightthickness = 0, bg = self._canvasColor)
        self.canvas.pack()
        self.root.attributes("-fullscreen", True)
        
    def updateLSLText(self):
       pass
   
    def createGrid(self):
        for i in range(0,4):
            offset = i* self.fifthInnerWidt
            self.canvas.create_line(self.coords_line1[0]+offset, 
                                    self.coords_line1[1],
                                    self.coords_line1[2]+offset,
                                    self.coords_line1[3],
                                    fill = self._innerGridColor, tag= "grid")
            i +=1
        self.canvas.update()

    def createBorder(self):
        self.canvas.create_line(self.thirdWidth, 0, self.thirdWidth, self.screenHeight, fill = self._gridColor, tag= "border")
        self.canvas.create_line(self.thirdWidth*2, 0, self.thirdWidth*2, self.screenHeight, fill = self._gridColor, tag = "border")
        self.canvas.update()

    def createBrick(self):
        b = Brick()
        b.draw_size()
        # draw random position slot or draw from middle
        self.canvas.create_rectangle(self.halfWidth - (b._width*self.fifthInnerWidt), 
                                     0+ self._upperOffset, 
                                     self.halfWidth + (b._width*self.fifthInnerWidt), 
                                     0+self._upperOffset+ b._height*self.fifthInnerWidt,
                                     color = b._color, tag = "brick")
        print(b)
        self.canvas.update()

    def moveBrick(self):
        pass

   # TODO: calculate delta Time
    def updateAndRender(self):
       self.root.after(self._updateRate, self.updateAndRender)

        
    def startRendering(self):
        self.createScreen()
        self.createBorder()
        self.createGrid()
        #dummy to test

        self.createBrick()


        self.lastUpdateTime = time.time()
        self.root.after(self._updateRate, self.updateAndRender)
        self.shouldRun = True
        while self.shouldRun: # a manual mainloop
            self.root.focus_set()
                  
            self.root.update() # if a key press is done the app could be already ended
            if self.shouldRun:
                self.root.update_idletasks()


class Brick(object):
    def __init__(self):
        self._width = None
        self._height = None
        self._color = None

        self.isSettled = False

    def draw_size(self):
        self._width = random.randint(1,2)
        self._height = random.randint(2,3)

    def draw_color(self):
        # to do: randomize from list
        self._color = "green"


