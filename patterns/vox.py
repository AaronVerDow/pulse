import griddata as gd
import numpy as np

#compile final image
class comp():
    def __init__(self):
        self.particle=False
        self.fade = False
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
                rcomp = rcomp*(1-layers[x].alphamask)+layers[x].pixlist
        if self.particle:
            rcomp = self.blendparticle(rcomp)
        elif self.fade:
            rcomp = self.blendfade(rcomp)
        return rcomp*255

    def blendparticle(self,current):
        self.partimg = ((self.partimg*self.pmaps[np.random.randint(0,10)])+current).clip(0,1)
        #self.partimg = self.partimg+current
        #self.partimg.clip(0,1)
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
