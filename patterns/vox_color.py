import griddata as gd
import numpy as np
import math

class color(object):
    #default colors for the lazy
    clist =[['black',[0.,0.,0.]],
            ['white',[1.,1.,1.]],
            ['red',[1.,0.,0.]],
            ['green',[0.,1.,0.]],
            ['blue',[0.,0.,1.]],
            ['yellow',[1.,1.,0.]],
            ['purple',[1.,0.,1.]],
            ['cyan',[0.,1.,1.]]]
    def __init__(self, color):
        self.hue = 0
        global n_pixels #using global for pixel number
        #check what type of color layer: flat default, passed rgb, or 
        #Procedural generation
        if isinstance(color, (int, float, long, complex)):
            self.hue = color
            self.c = self.huetorgb(color)
        if type(color) is list:
            if len(color) == 1:
                np.array(color)
            if len(color) == 3:
                self.c = np.array(color).reshape(1,3)
            else:
                self.c = np.array([0.,0.,0.]).reshape(1,3)

    def changecolor(self, color):
        if isinstance(color, (int, float, long, complex)):
            self.hue = color
            self.c = self.huetorgb(color)
        if type(color) is list:
            if len(color) == 1:
                np.array(color)
            if len(color) == 3:
                self.c = np.array(color).reshape(1,3)
            else:
                self.c = np.array([0.,0.,0.]).reshape(1,3)

    def evalcolor(self, color):
        if isinstance(color, (int, float, long, complex)):
            return self.huetorgb(color)
        if type(color) is list:
            if len(color) == 1:
                return np.array(color)
            if len(color) == 3:
                return np.array(color).reshape(1,3) 
        else:
            return np.array([0.,0.,0.]).reshape(1,3)

    def shifthue(self,change):
        if self.hue:
            newhue = self.hue+change
            self.c = self.huetorgb(newhue)
            self.hue = newhue
        else:
            self.hue = change
            self.c = self.huetorgb(change)
                
    def huetorgb(self,hue):
        scale = 360/(2*math.pi)
        r = math.cos(hue/scale)+.5
        g = math.cos((hue/scale)+((4./3.)*math.pi))+.5
        b = math.cos((hue/scale)+((2./3.)*math.pi))+.5
        return np.clip(np.array([[r,g,b]]),0,1)

    #vertical fade from toprgb down to bottomrgb
    def vfadeinit(self, topcolor, bottomcolor):
        if isinstance(topcolor, (int, float, long, complex)) and isinstance(bottomcolor, (int, float, long, complex)):
            self.tophue = topcolor
            toprgb = self.huetorgb(topcolor)[0]
            self.bottomhue = bottomcolor
            bottomrgb = self.huetorgb(bottomcolor)[0]
        else:
            toprgb = topcolor
            bottomrgb = bottomcolor
        self.strip= np.zeros((6400,3))
        rstep = (toprgb[0]-bottomrgb[0])/64 ##remve hard numbers
        gstep = (toprgb[1]-bottomrgb[1])/64
        bstep = (toprgb[2]-bottomrgb[2])/64
#        for x in range(100): ##remove hard numbers
#            for i in range(64): #remove hard numbers
#                strip.append([toprgb[0]-i*rstep,toprgb[1]-i*gstep,toprgb[2]-i*bstep])
        for x in range(64):
            self.strip[x:6400+x:64] = np.array([toprgb[0]-x*rstep,toprgb[1]-x*gstep,toprgb[2]-x*bstep])
            
        self.c = self.strip
        
    def vfadeshift(self, topshift, bottomshift):
        self.tophue += topshift
        toprgb = self.huetorgb(self.tophue)[0] 
        self.bottomhue += bottomshift
        bottomrgb = self.huetorgb(self.bottomhue)[0]
        
        rstep = (toprgb[0]-bottomrgb[0])/64 ##remve hard numbers
        gstep = (toprgb[1]-bottomrgb[1])/64
        bstep = (toprgb[2]-bottomrgb[2])/64
        for x in range(64):
            self.strip[x:6400+x:64] = np.array([toprgb[0]-x*rstep,toprgb[1]-x*gstep,toprgb[2]-x*bstep])
        self.c = self.strip       

    def vrainbow(self,shift = 0, steps = 2 , flip = False):
        holder = np.zeros((100,64,3))
        if flip:
            for x in range(64):
                holder[:,63-x] = self.huetorgb(shift+x*steps)            
        else:
            for x in range(64):
                holder[:,x] = self.huetorgb(shift+x*steps)
        holder = holder.reshape(6400,3)
        self.c = holder

    def xrainbow(self,shift = 0, steps = 2, flip = False):
        holder = np.zeros((10,10,64,3))
        for x in range(10):
            holder[:,x]= self.huetorgb(shift+x*steps)
        holder = holder.reshape(6400,3)
        self.c = holder
        
    def yrainbow(self,shift = 0, steps = 2, flip = False):
        holder = np.zeros((10,10,64,3))
        for x in range(10):
            holder[x,:]= self.huetorgb(shift+x*steps)
        holder = holder.reshape(6400,3)
        self.c = holder
