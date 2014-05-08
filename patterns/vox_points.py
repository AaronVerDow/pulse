import numpy as np
import scipy.spatial as sp
import vox_color
from vox_shapes import layer

#base class for holding array of points
class pointholder():
    
    #list of points around the cube
    points = []
    pointsindex = []
    
    #values of pixels for full cube to be used by compiler
    pixlist = []
    alphamask = []

    #add a new poiint to the point list
    def add(self,line,x,y,z,size):
        self.points.append([line, x, y, z, size])
        self.pointsindex.append(line)
        
    #remove points by its position in the list
    def remove(self,num):
        points.pop(num)
        pointsindex.pop(num)

    #def update pixlist
    def updatepix(self):
        #make a new array the size of the final pixel list
        px=np.zeros((self.gridinfo['pixelcount'],1))
        #for each point
        for  p in self.points:
            rendstrip = self.pointrender(p[3],p[4])
            for rp in range(len(rendstrip)):
                if rendstrip[rp] != 0:
                    pixnumber = p[0]*self.gridinfo['zcount']+rp
                    px[pixnumber]=rendstrip[rp]
        print np.shape(px)
        #self.alphamask = px*np.array(self.alpha).reshape(3,1)
        self.alphamask = px*self.alpha
        print np.shape(self.alphamask)
        self.pixlist = self.alphamask*self.color.c

    #calculate distance on a 1d plain
    def calcdist(self, location):
        return np.abs(location-self.gridinfo['1dgrid'])

    def pointrender(self, location, size):
        t =self.gridinfo['zsteps']
        n = 1/self.gridinfo['zsteps']
        nsize = size*(t)
        return np.clip((nsize-self.calcdist(location))*n,0,1)
    
    #update pixlist
    def update(self):
        self.updatepix()
        
        

#surface of points
class surface(pointholder,layer):
    def __init__(self,xy,color,size,z,alpha,**griddata):
        print 'z '+str(z)
        for l in range(len(xy)):
            self.add(l,xy[l][0],xy[l][1],z,size)
        #pass color to colorhandle in layer class to set it up.
        self.color = self.colorhandle(color)
        #pass alpha to alpha handle in layer class to set it up.
        self.alpha = self.alphahandle(alpha)
        self.gridinfo = griddata

    #changing the starting z val of all points in the surface
    def changez(self,z):
        for l in points:
            l[3]=z
    
    #changing the size of all points in the surface
    def changesize(self,size):
        for l in points:
            l[4]=size
