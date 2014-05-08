import numpy as np
import scipy.spatial as sp
import vox_color
from vox_shapes import layer
import time
from math import *

#base class for holding array of points
class pointholder():
    
    #list of points around the cube
#    points = []
#    pointsindex = []
    
    #values of pixels for full cube to be used by compiler
#    pixlist = []
#    alphamask = []
    
    #store modifications to run over the points
#    mod = []
    
    #time
    stime = 0
    ctime = 0
    
    #add a point
    def add(self,**newpoint):
        self.points.append(newpoint)
    
    #remove points by its position in the list
    def remove(self,num):
        points.pop(num)

    #this add a new mod to the stack.  no checks on what you put in
    #if you do it wrong you will just crash everything so check you 
    #target ie.
    #'modname':wavex.....
    def addmod(self,**func):
        self.mod.append(func)
    
    def addxwave(self):
        self.mod.append({'modname':self.xwave})
        
    def addywave(self):
        self.mod.append({'modname':self.ywave})
        
    def addxywave(self):
         self.mod.append({'modname':self.xywave})
            
    #def update pixlist
    def updatepix(self):
        #make a new array the size of the final pixel list
        px=np.zeros((self.gridinfo['pixelcount'],1))
        #for each point
        for p in self.points:
            rendstrip = self.pointrender(p['z'],p['size'])
            for rp in range(len(rendstrip)):
                if rendstrip[rp] != 0:
                    pixnumber = p['sid']*self.gridinfo['zcount']+rp
                    px[pixnumber]=rendstrip[rp]
        self.alphamask = px*self.alpha
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
        for m in self.mod:
            m['modname']()
        self.updatepix()
        
        

#surface of points
class surface(pointholder,layer):
    def __init__(self,xy,color,size,z,alpha,**griddata):
        #####################not sure why I have to do this will fix later
        self.mod = []
        self.pixlist = []
        self.alphamask = []
        self.points = []
        self.pointsindex = []
        #######################
        for l in range(len(xy)):
            #self.add(l,xy[l][0],xy[l][1],z,size)
            self.add(**{'sid':l,'x': xy[l][0],'y': xy[l][1],'z':z,'size':size})
        #pass color to colorhandle in layer class to set it up.
        self.color = self.colorhandle(color)
        #pass alpha to alpha handle in layer class to set it up.
        self.alpha = self.alphahandle(alpha)
        self.gridinfo = griddata
        self.stime = time.time()

    #changing the starting z val of all points in the surface
    def changez(self,z):
        for l in self.points:
            l['z']=z
    
    #changing the size of all points in the surface
    def changesize(self,size):
        for l in self.points:
            l['size'] = size
    
    def xwave(self):
        for p in self.points:
            p['z']=sin(p['x']+(time.time()-self.stime))
            
    def ywave(self):
        for p in self.points:
            p['z']=sin(p['y']+(time.time()-self.stime))
            
    def xywave(self):
        for p in self.points:
            p['z']=(sin(p['y']+(time.time()-self.stime))+sin(p['x']+(time.time()-self.stime)))/2
        
class pointgroup(pointholder,layer):
    
    def __init__(self,color,size,alpha,ppm,**griddata):
        #pass color to colorhandle in layer class to set it up.
        self.color = self.colorhandle(color)
        #pass alpha to alpha handle in layer class to set it up.
        self.alpha = self.alphahandle(alpha)
        #grid data stored in a dictionary
        self.gridinfo = griddata
        
        self.size=size #want to add in range option
    
