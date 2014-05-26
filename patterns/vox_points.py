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
        return sp.distance.cdist(self.points,pos)
    
    def calc2ddist(self,location):
        return sp.distance.cdist(gd.grid2d,location)
        

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
    def addsinwave(self, target = 'default' , axis ='x', amp = 1, freq = 1, axisoffset = 0, zoffset = 0):
        """ Adds a sine wave for the x OR y axis
        axis is x or y
        amp is the amplitud modifer
        freq is the frequancy modifer
        axisoffset shift along what ever axis is selected. (moved left or right)
        zoffset shifts along the z axiz (moved up or down)
        """
        if target == 'default': target = self.mod
        target.append({'modname':self.sinwave, 'arg':{'axis': axis, 'amp':amp,'freq':freq,'axisoffset':axisoffset,'zoffset':zoffset}})

    def sinwave(self,axis,amp,freq,axisoffset,zoffset,target,**k):
        """sine wave calculations for each point
        """
        for p in target:
            p['z']=amp*sin(freq*p[axis]+(time.time()-self.stime)+axisoffset)+zoffset
    
    ##Add a 2d sin wave using the x and y axis    
    def addxywave(self, target = 'default', xamp = .5, xfreq = 1, xoffset = 0, xzoffset = 0, yamp = .5, yfreq = 1, yoffset = 0, yzoffset = 0):
        """ Adds a 2d sine wave for x and y axis
        xamp/yamp aplitud on respective axis.  set to .5 by default because you add 2 wave
        xfreq/yfreq frquancy on the respective axis
        xoffset/yoffset offset along the axis (left/right/forward/back)
        xzoffset/yzoffset offset along the z axiz (up/down)
        """
        if target == 'default': target = self.mod
        target.append({'modname':self.xywave, 'arg':{'xamp':xamp, 'xfreq':xfreq, 'xoffset':xoffset, 'xzoffset':xzoffset, 'yamp':yamp, 'yfreq':yfreq, 'yoffset':yoffset, 'yzoffset':yzoffset}})

    def xywave(self, xamp, xfreq, xoffset, xzoffset, yamp, yfreq, yoffset, yzoffset, target,**k):
        """sine wave calculations for each point
        """
        for p in target:
            p['z']=(xamp*sin(xfreq*p['x']+(time.time()-self.stime)+xoffset)+xzoffset)+(yamp*sin(yfreq*p['y']+(time.time()-self.stime)+yoffset)+yzoffset)
    
    def addrwave(self, target = 'default', location =[0,0] , amp = 1, freq = 1, axisoffset = 0, zoffset = 0):
        """adds a radiating sine wave from 'location'
        """
        if target == 'default': target = self.mod
        target.append({'modname':self.rwave, 'arg':{'location': np.array(location).reshape(1,2),'amp':amp,'freq':freq,'axisoffset':axisoffset,'zoffset':zoffset}})       
    
    def rwave(self, location, amp, freq, axisoffset, zoffset, target):
        dist = self.calc2ddist(location)
        for p in target:
            p['z']=amp*sin(freq*dist[p['sid']]+(time.time()-self.stime)+axisoffset)+zoffset
    
    #add a field that pushed points away
    def addpushfield(self,size = 1,location = [0,0,0]):
        self.mod.append({'modname':self.pushfield,'arg':{'size':size,'location':np.array(location).reshape(1,3)}})
        
    def pushfield(self, size, location):
        #dist = sp.distance.cdist(self.points,location)
        for p in self.points:
            x = np.power(sp.distance.cdist(np.array([[p['x']],[p['y']],[p['zstart']]]).reshape(1,3),location),-3)
#            if p['z']>=location[1][3]:
#                p['z']=p['z']+x
            p['z'] = p['zstart']+x

    """start update code
    """
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
        if self.color:
            self.pixlist = self.alphamask*self.color.c
        else:
            self.pixlist = 0
            self.alphamask = 1-self.alphamask

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
                m['modname'](target = self.points,**m['arg'])
            else:
                print 'no args listed'
                m['modname']()
        self.updatepix()
    """end update code
    """

#surface of points
class surface(pointholder,layer):
    def __init__(self,xy,color,size,z,alpha):
        #####################not sure why I have to do this will fix later
        self.initshit()
        #######################
        for l in range(len(gd.xy)):
            #self.add(l,xy[l][0],xy[l][1],z,size)
            self.add(**{'sid':l,'x': gd.xy[l][0],'y': gd.xy[l][1],'z':z,'zstart':z,'size':size})
        #pass color to colorhandle in layer class to set it up.
        if color:
            self.color = self.colorhandle(color)
        else:
            self.color = color
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
        self.initshit()
        for l in range(gd.stripcount):
            self.pointsa.append({'sid':l, 'x': gd.grid2d[l][0], 'y': gd.grid2d[l][1],'z':za,'size':1})
            self.pointsb.append({'sid':l, 'x': gd.grid2d[l][0], 'y': gd.grid2d[l][1],'z':zb,'size':1})
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
        self.pointsb = []
    
    def add(self):
        pass
    def remove(self):
        pass
    
    """start update code
    """

    def updatepix(self,ap,bp):
        if len(ap)==len(bp):
            px=np.zeros((gd.pixelcount,1))
            for strp in range(len(ap)):
                aclose = self.findclosest(ap[strp]['z'])
                bclose = self.findclosest(bp[strp]['z'])
                if aclose<bclose:
                    p1,p2 = aclose, bclose
                else:
                    p2,p1 = aclose, bclose
                for i in range(p1,p2):
                    px[i+(ap[strp]['sid']*gd.zcount)] = 1
        else:
            print "not the same length"
        self.alphamask = px*self.alpha
        if self.color:
            self.pixlist = self.alphamask*self.color.c
        else:
            self.pixlist = 0
            self.alphamask = 1-self.alphamask
    #point a, point b, stripid, alpha
    def renderstrip(self,pa,pb, strip, a):
        a = self.findcloses(pa)
        b = self.findcloses(pb)
        

    def findclosest(self,p):
        scale = (1/gd.zsteps)
        return np.clip(np.int(33+p*scale),0,63)

    #update pixlist
    def update(self):
        #for each mod we have in the list
        for m in self.moda:
            #if we have variable added to the mod
            if 'arg' in m:
                #call the mod and pass the variable in the dic
                m['modname'](target = self.pointsa,**m['arg'])
            else:
                print 'no args listed'
                m['modname']()
        for m in self.modb:
            #if we have variable added to the mod
            if 'arg' in m:
                #call the mod and pass the variable in the dic
                m['modname'](target = self.pointsb,**m['arg'])
            else:
                print 'no args listed'
                m['modname']()
        self.updatepix(self.pointsa,self.pointsb)
    """end update code
    """


class pointgroup(pointholder,layer):
    
#        for c in range(pcount):
#            t = random.randint(0,tspan)
#            sid = random.randint(0,len(gd.grid2d)-1)
#            z = random.uniform(gd.zmin,gd.zmax)
#            self.add(**{'sid': sid, 'x': gd.grid2d[sid][0], 'y': gd.grid2d[sid][1], 'stime': time.time(), 'size': size, 'tspan': t, 'z':z})

    def __init__(self, color = [0.0,0.0,0.0] , alpha = 1, size = 0, pcount = 0, minspawnz= gd.zmin, maxspawnz = gd.zmax, ttl = None):
        #pass color to colorhandle in layer class to set it up.
        self.color = self.colorhandle(color)
        #pass alpha to alpha handle in layer class to set it up.
        self.alpha = self.alphahandle(alpha)
        #init some shit
        self.initshit()
        
        self.size = size
        self.pcount = pcount
        self.minspawnz = minspawnz
        self.maxspawnz = maxspawnz
        self.ttl = ttl
        self.killperam = []
        
    """point modification functions
    this section hold the 'mods' for point groups
    they are interchangable with surface mods for the
    most part and may be moved into the general
    pointholder class later
    """
    def addzshift(self, shift = 0, pertime = 1):
        """add z shifting
        shift is the unit of space to move the point
        time is the 'per time' unit in sec
        will move each point 'shift' every 'time' seconds
        """
        store = storage()
        store.shift = shift
        store.time = pertime
        store.lasttime = time.time()
        self.mod.append({'modname':self.zshift, 'arg':{'store': store}})
        return store
    
    def zshift(self, target, store):
        scale = store.time*(time.time()-store.lasttime)
#        if time.time()-store.lasttime>store.time:
        for p in target:
            p['z'] = p['z']+(store.shift*scale)
        store.lasttime=time.time()
            
    def addfadein(self, ftime = 5):
        self.mod.append({'modname':self.fadein, 'arg':{'ftime':ftime}})
        
    def fadein(self, ftime):
        for p in self.points:
            if time.time()-p['stime']<ftime:
                p['alpha']=(time.time-p['stime'])*(1/ftime)
            
    
    """end mod section
    """
        
    """logic for removing points
    This section is to add peramiters that determan if a point
    should be popped from the stack.
    """    
    def addkillperam(self,peram,compare,arg):
        self.killperam.append({'peram':peram,'comp':compare,'arg':arg})
    
    
    def cull(self):
        for k in self.killperam:
            poplist = []
            if k['comp']== 'greater':
                for p in range(len(self.points)):
                    if self.points[p][k['peram']] >= k['arg']:
                        self.points.pop(p)
            elif k['comp']== 'less':
                for p in range(len(self.points)):
                    if self.points[p][k['peram']] <= k['arg']:
                        poplist.append(p)
            for idx in range(len(poplist)):
                self.points.pop(poplist[idx]-idx)
    """end point removal
    """
    
    
    def fillout(self):
        while len(self.points) < self.pcount:
            sid = random.randint(0,len(gd.grid2d)-1)
            z = random.uniform(self.minspawnz,self.maxspawnz)
            self.add(**{'sid': sid, 'x': gd.grid2d[sid][0],  'y': gd.grid2d[sid][1], 'stime': time.time(), 'size': self.size, 'ttl': self.ttl, 'z':z, 'alpha':self.alpha})
            

    def ramp(self):
        pass

    def update(self):
        self.cull()
        self.fillout()
        for m in self.mod:
            #if we have variable added to the mod
            if 'arg' in m:
                #call the mod and pass the variable in the dic
                m['modname'](target = self.points,**m['arg'])
            else:
                print 'no args listed'
                m['modname']()
        self.updatepix()

class storage():
    def __init__(self):
        self.stime = time.time()
