import griddata as gd
import numpy as np
import time
import vox_color

#base layer to hold common actions like dynamicly taking color layers   
class layer():
    def colorhandle(self,color):
        #handling veriable in the way color may be passed
        if type(color) == vox_color.color: #if color is of color object we are good
            print "that is a god damn color"
            return color
        elif type(color) == list:#if color is a list make a color object out of it
            return vox_color.color(color)
        else:#else make it just black, you should not have fucked up if you wanted color
            return vox_color.color('black')

    def alphahandle(self,alpha):
        self.void = False
        self.invert = False
        if alpha == 'void':
            self.void = True
            return np.array([[1.0,1.0,1.0]])
        if alpha == 'invert':
            self.invert = True
            return np.array([[1.0,1.0,1.0]])
        #handling ways that alpha can be passed
        if type(alpha) == int:
#            return [alpha,alpha,alpha]
#            return alpha
            return np.array([[alpha,alpha,alpha]])
        else:
            return alpha

    def alphamagic(self):
        if self.void == True:
            self.pixlist = 0
        if self.invert == True:
            self.pixlist = 0
            self.alphamask = 1-self.alphamask

    def setalpha(self, alpha):
        self.alpha = alphahandle(alpha)
        
    def setcolor(self, color):
        self.color = colorhandle(color)

class fillscreen(layer):
    def __init__(self,color,alpha = 1):
        self.alpha = self.alphahandle(alpha)
        self.color = self.colorhandle(color)
        self.pixels = np.ones((6400,3))
        
    def update(self):
        self.pixlist = self.color.c*self.alpha*self.pixels

#compile final image
class comp():
    def __init__(self, ablock = True):
        self.particle=False
        self.fade = False
        self.shift = False
        self.ablock = ablock


    #Take layers(an array of layer objects that have pixlist and
    # alphamask. Turns them into single image 
    def complayers(self, layers):
        rcomp = []
        for x in range(len(layers)):
            if x == 0:
                rcomp = layers[x].pixlist
            #if we have more the one layer we use the current layer
            #being added and use its alpha map to mask the rolling layer
            else:
                if self.ablock:
                    rcomp = rcomp*(1-layers[x].alphamask)+layers[x].pixlist
                else:
                    rcomp = rcomp*(1-layers[x].pixlist)+layers[x].pixlist
        if self.particle:
            rcomp = self.blendparticle(rcomp)
        elif self.fade:
            rcomp = self.blendfade(rcomp)
        if self.shift:
            rcomp = self.shiftf(rcomp)
        return rcomp*255




    def blendparticle(self,current):
        self.partimg = ((self.partimg*self.pmaps[np.random.randint(0,10)])+current).clip(0,1)
        return self.partimg
    
    def addparticlemap(self):
        self.particle=True
        self.pmaps = []
        for x in range(10):
            self.pmaps.append(np.random.rand(6400,1)*.9)
        self.partimg = np.zeros((6400,3))

    def addfade(self, fspeed = .6):
        self.fade = True
        self.fades = fspeed
        self.partimg = np.zeros((6400,3))

    def blendfade(self,current):
        self.partimg = ((self.partimg*self.fades)+current).clip(0,1)
        return self.partimg

    def addshift(self, dual = False, sps = .8, fadeper = .6):
        self.shift = True
        self.spf = sps
        self.fadeper = fadeper
        self.sframe = np.zeros((6400,3))
        self.lstime = time.time()
        self.dfade = dual
    
    def shiftf(self, current):
        ctime = time.time()-self.lstime
        snum = (ctime*self.spf)
        snuminvert = 1-(self.spf)
        fr = (self.sframe+current).clip(0,1)
        if self.dfade:
            uframe = np.append(np.delete(fr.reshape(100,64,3),0,1),np.zeros((100,1,3)),1)
            dframe = np.append(np.zeros((100,1,3)),np.delete(fr.reshape(100,64,3),63,1),1)
            frame = (dframe.reshape(6400,3)+uframe.reshape(6400,3))/2
            self.sframe = frame*self.spf
        else:
            if self.spf>0:
                frame = np.append(np.delete(fr.reshape(100,64,3),0,1),np.zeros((100,1,3)),1)
                self.sframe = frame.reshape(6400,3)*(self.spf)
            elif self.spf<0:
                frame = np.append(np.zeros((100,1,3)),np.delete(fr.reshape(100,64,3),63,1),1)
                self.sframe = frame.reshape(6400,3)*(np.abs(self.spf))            
        self.lstime = time.time()
        return (self.sframe+current).clip(0,1)    
