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

    def calcdist(self, location):
        #calculates the distance from center for each pixel.  clips so
        #we don't have any values out of the range 0-1
        return np.clip(self.size-sp.distance.cdist(self.points,pos),0,1)

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
    def addsinwave(self, axis ='x', amp = 1, freq = 1, axisoffset = 0, zoffset = 0):
        """ Adds a sine wave for the x OR y axis
        axis is x or y
        amp is the amplitud modifer
        freq is the frequancy modifer
        axisoffset shift along what ever axis is selected. (moved left or right)
        zoffset shifts along the z axiz (moved up or down)
        """
        self.mod.append({'modname':self.sinwave, 'arg':{'axis': axis, 'amp':amp,'freq':freq,'axisoffset':axisoffset,'zoffset':zoffset}})

    def sinwave(self,axis,amp,freq,axisoffset,zoffset,**k):
        """sine wave calculations for each point
        """
        for p in self.points:
            p['z']=amp*sin(freq*p[axis]+(time.time()-self.stime)+axisoffset)+zoffset
    
    ##Add a 2d sin wave using the x and y axis    
    def addxywave(self, xamp = .5, xfreq = 1, xoffset = 0, xzoffset = 0, yamp = .5, yfreq = 1, yoffset = 0, yzoffset = 0):
        """ Adds a 2d sine wave for x and y axis
        xamp/yamp aplitud on respective axis.  set to .5 by default because you add 2 wave
        xfreq/yfreq frquancy on the respective axis
        xoffset/yoffset offset along the axis (left/right/forward/back)
        xzoffset/yzoffset offset along the z axiz (up/down)
        """
        self.mod.append({'modname':self.xywave, 'arg':{'xamp':xamp, 'xfreq':xfreq, 'xoffset':xoffset, 'xzoffset':xzoffset, 'yamp':yamp, 'yfreq':yfreq, 'yoffset':yoffset, 'yzoffset':yzoffset}})

    def xywave(self, xamp, xfreq, xoffset, xzoffset, yamp, yfreq, yoffset, yzoffset,**k):
        """sine wave calculations for each point
        """
        for p in self.points:
            p['z']=(xamp*sin(xfreq*p['x']+(time.time()-self.stime)+xoffset)+xzoffset)+(yamp*sin(yfreq*p['y']+(time.time()-self.stime)+yoffset)+yzoffset)
    
    def addrwave(self, location =[0,0,0] , amp = 1, freq = 1, axisoffset = 0, zoffset = 0):
        """adds a radiating sine wave from 'location'
        """
        self.mod.append({'modname':self.rwave, 'arg':{'location': location,'amp':amp,'freq':freq,'axisoffset':axisoffset,'zoffset':zoffset}})       
    
    def addrwave(self, location, amp, freq, axisoffset, zoffset):
        pass
    
    #add a field that pushed points away
    def addpushfield(self,size = 1,location = [0,0,0]):
        self.mod.append({'modname':self.pushfield,'arg':{'size':size,'location':location}})
        
    def pushfield(self, size, location):
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
            #if we have variable added to the mod
            if 'arg' in m:
                #call the mod and pass the variable in the dic
                m['modname'](**m['arg'])
            else:
                print 'no args listed'
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

class dualsurface(pointholder,layer):
    def __init__(self,color,za,zb,alpha):
        initshit()
        for l in range(gd.stripcount):
            self.pointsa(**{'sid':l, 'x': gd.grid2d[sid][0], 'y': gd.grid2d[sid][1],'z':za,'size':size})
            self.pointsb(**{'sid':l, 'x': gd.grid2d[sid][0], 'y': gd.grid2d[sid][1],'z':zb,'size':size})
        #pass color to colorhandle in layer class to set it up.
        self.color = self.colorhandle(color)
        #pass alpha to alpha handle in layer class to set it up.
        self.alpha = self.alphahandle(alpha)
        self.stime = time.time()        
        
    def initshit(self):
        self.moda = []
        self.modb = []
        self.pixlist = []
        self.alphamask = []
        self.pointsa = []
        self.pointsb

        
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

#    def cull(self):
#        t = time.time()
#        for p in self.points:
#            pass
    
    def fillout(self):
        while len(self.points) < self.pcount:
            sid = random.randint(0,len(gd.grid2d)-1)
            z = random.uniform(gd.zmin,gd.zmax)
            self.add(**{'sid': sid, 'x': gd.grid2d[sid][0],  'y': gd.grid2d[sid][1], 'stime': time.time(), 'size': self.size, 'tspan': self.tspan, 'z':z})

#    def fillout(self):
#        while len(self.points) < self.pcount:
            

    def ramp(self):
        pass

    def update(self):
        self.cull()
        self.fillout()
        self.updatepix()
