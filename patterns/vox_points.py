import numpy as np
import scipy.spatial as sp
import vox_color
from vox_shapes import layer
import time
from math import *
import random
import griddata as gd

#base class for holding array of points
class pointholder():

    def initshit(self):
        self.mod = []
        self.pixlist = []
        self.alphamask = []
        self.points = []
        self.pointsindex = []
    
    #add a point
    def add(self,**newpoint):
        self.points.append(newpoint)
    
    #remove points by its position in the list
    def remove(self,num):
        self.points.pop(num)

    #this add a new mod to the stack.  no checks on what you put in
    #if you do it wrong you will just crash everything so check you 
    #target ie.
    #'modname':wavex.....
    def addmod(self,**func):
        self.mod.append(func)
 
    """
    This section is for adding and running def that modify the points in
    some way.
    """
    ##Add a sin wave over the X axis
    def addxwave(self):
        self.mod.append({'modname':self.xwave})
    
    ##Add a sin wave over the y axis    
    def addywave(self):
        self.mod.append({'modname':self.ywave})
    
    ##Add a 2d sin wave using the x and y axis    
    def addxywave(self):
         self.mod.append({'modname':self.xywave})
 
    def xwave(self):
        for p in self.points:
            p['z']=sin(p['x']+(time.time()-self.stime))
            
    def ywave(self):
        for p in self.points:
            p['z']=sin(p['y']+(time.time()-self.stime))
            
    def xywave(self):
        for p in self.points:
            p['z']=(sin(p['y']+(time.time()-self.stime))+sin(p['x']+(time.time()-self.stime)))/2
    
    #add a field that pushed points away
    def addpushfield(self,size,location):
        self.mod.append({'modname':self.pushfield,'var':{'size':size,'location':location}})
        
    def pushfield(self, **karg):
        pass


    #def update pixlist
    def updatepix(self):
        #make a new array the size of the final pixel list
        px=np.zeros((gd.pixelcount,1))
        #for each point
        for p in self.points:
            rendstrip = self.pointrender(p['z'],p['size'])
            for rp in range(len(rendstrip)):
                if rendstrip[rp] != 0:
                    pixnumber = p['sid']*gd.zcount+rp
                    px[pixnumber]=rendstrip[rp]
        self.alphamask = px*self.alpha
        self.pixlist = self.alphamask*self.color.c

    #calculate distance on a 1d plain
    def calcdist(self, location):
        return np.abs(location-gd.grid1d)

    def pointrender(self, location, size):
        n = 1/gd.zsteps
        nsize = size*gd.zsteps
        return np.clip((nsize-self.calcdist(location))*n,0,1)
    
    #update pixlist
    def update(self):
        #for each mod we have in the list
        for m in self.mod:
#            #if we have variable added to the mod
#            if m['var']:
#                #call the mod and pass the variable in the dic
#                m['modname'](**m['var'])
#            else:
            m['modname']()
        self.updatepix()
        

#surface of points
class surface(pointholder,layer):
    def __init__(self,xy,color,size,z,alpha):
        #####################not sure why I have to do this will fix later
        self.initshit()
        #######################
        for l in range(len(xy)):
            #self.add(l,xy[l][0],xy[l][1],z,size)
            self.add(**{'sid':l,'x': xy[l][0],'y': xy[l][1],'z':z,'size':size})
        #pass color to colorhandle in layer class to set it up.
        self.color = self.colorhandle(color)
        #pass alpha to alpha handle in layer class to set it up.
        self.alpha = self.alphahandle(alpha)
#        self.gridinfo = griddata
        self.stime = time.time()

    #changing the starting z val of all points in the surface
    def changez(self,z):
        for l in self.points:
            l['z']=z
    
    #changing the size of all points in the surface
    def changesize(self,size):
        for l in self.points:
            l['size'] = size
        
class pointgroup(pointholder,layer):
    
    def __init__(self,color,size,alpha,tspan,pcount):
        #pass color to colorhandle in layer class to set it up.
        self.color = self.colorhandle(color)
        #pass alpha to alpha handle in layer class to set it up.
        self.alpha = self.alphahandle(alpha)
        #grid data stored in a dictionary
#        self.gridinfo = griddata
        
        self.initshit()
        
        self.size=size ########want to add in range option
        self.tspan = tspan
        self.pcount = pcount
        
        for c in range(pcount):
            t = random.randint(0,tspan)
            sid = random.randint(0,len(gd.grid2d)-1)
            z = random.uniform(gd.zmin,gd.zmax)
            self.add(**{'sid': sid, 'x': gd.grid2d[sid][0], 'y': gd.grid2d[sid][1], 'stime': time.time(), 'size': size, 'tspan': t, 'z':z})
    
    #clear out the old points        
    def cull(self):
        t = time.time()
        for p in self.points:
            if t - p['stime'] > p['tspan']:
                self.points.remove(p)
    
    def fillout(self):
        while len(self.points) < self.pcount:
            sid = random.randint(0,len(gd.grid2d)-1)
            z = random.uniform(gd.zmin,gd.zmax)
            self.add(**{'sid': sid, 'x': gd.grid2d[sid][0],  'y': gd.grid2d[sid][1], 'stime': time.time(), 'size': self.size, 'tspan': self.tspan, 'z':z})

    def update(self):
        self.cull()
        self.fillout()
        self.updatepix()
