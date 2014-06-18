import numpy as np
import scipy.spatial as sp
import vox_color
from vox import layer
import griddata as gd
import time

#spheres for making ... spheres
class sphere(layer):
    pixlist = []
    alphamask = []
    #take center position of sphere, color in rgb 0-1 or a color object,
    #size, mode (fill or fade), and alpha (0-1 as a scaler or rgb list)
    def __init__(self,spos, color, size = 1, mode = 'fade', alpha = 1, maxspeed = .1, ratio = 1.0):
        self.pos = np.transpose(spos)
        self.size = size
        self.points = gd.grid3d
        self.maxspeed = maxspeed
        self.ratio = ratio
        self.target = self.pos
        self.lastrun = time.time()
        self.mode = mode
        
        #pass color to colorhandle in layer class to set it up.
        self.color = self.colorhandle(color)
        #pass alpha to alpha handle in layer class to set it up.
        self.alpha = self.alphahandle(alpha)

    def calcdist(self, pos):
        #calculates the distance from center for each pixel.  clips so
        #we don't have any values out of the range 0-1
        return np.clip((self.size-sp.distance.cdist(self.points,pos)),0,1)


    def update(self):
        self.movetowards()
        dis = self.calcdist(self.pos)
        if self.mode == 'fade':
            self.pixlist = (self.alpha*dis)*self.color.c
            self.alphamask = (self.alpha*dis)
        elif self.mode == 'fill':
            m = dis>0
            self.pixlist = (self.alpha*m)*self.color.c
            self.alphamask = (self.alpha*m)
        elif self.mode == 'bubble':
            m = dis>0
            self.pixlist = (1-dis)*m*self.alpha*self.color.c
            self.alphamask = (1-dis)*m*self.alpha
        self.alphamagic()
            
    def movetowards(self):
        ctime = time.time()-self.lastrun
        self.pos = self.pos+np.clip(((self.target-self.pos)*self.ratio*ctime),-self.maxspeed,self.maxspeed)
        self.lastrun = time.time()

class cylinder():
    """
    pl0 = first point on line
    pl1 = 2nd point on line
    planp = point on the plane
    plann = normal of the plane
    """
    def isectp(self,lp0,lp1,planp,plann):
        #make direction vector
        u = lp1-lp0
        #don't know but something to do with direction to point on surface
        w = lp0-planp
        
        dot = np.dot(plann,np.transpose(u))
        
        if abs(dot)>.0000001:
            fac = -np.dot(plann,w)/dot
            u2 = u*fac
            return lp0+u2
        else:
            return None
