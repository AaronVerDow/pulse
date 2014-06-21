import numpy as np
import scipy.spatial as sp
import vox_color3 as vox_color
from vox3 import layer
import griddata as gd
import time

class box(layer):
    pixlist = []
    alphamask = []
    #take center position of sphere, color in rgb 0-1 or a color object,
    #size, mode (fill or fade), and alpha (0-1 as a scaler or rgb list)
    def __init__(
        self,
        spos,
        color,
        x = 1,
        y = 1,
        z = 1,
        alpha = 1,
        ratio = 1.0):

        self.pos = np.transpose(spos)
        self.x = x
        self.y = y
        self.z = z
        #there has got to be a better way to do this
        self.points = gd.grid3d
        self.target = self.pos
        self.lastrun = time.time()
        #pass color to colorhandle in layer class to set it up.
        self.color = self.colorhandle(color)
        #pass alpha to alpha handle in layer class to set it up.
        self.alpha = self.alphahandle(alpha)

    def update(self):
 
        points = gd.exploded

        x_min = 0
        x_max = 9
        y_min = 0
        y_max = 9
        z_min = 0
        z_max = 63
        listed_points = []

        while points[0][0][z_min][2] > self.pos[0][2] + self.z/2 and z_min < z_max:
            z_min = z_min + 1
        while points[0][0][z_max][2] < self.pos[0][2] - self.z/2 and z_min < z_max:
            z_max = z_max - 1
        while points[x_min][0][0][0] < self.pos[0][0] - self.x/2 and x_min < x_max:
            x_min = x_min + 1
        while points[x_max][0][0][0] > self.pos[0][0] + self.x/2 and x_min < x_max:
            x_max = x_max - 1
        while points[0][y_min][0][1] < self.pos[0][1] - self.y/2 and y_min < y_max:
            y_min = y_min + 1
        while points[0][y_max][0][1] > self.pos[0][1] + self.y/2 and y_min < y_max:
            y_max = y_max - 1

        for x in range(0,len(points)):
            for y in range(0,len(points[0])):
                for z in range(0,len(points[0][0])):
                    if x_min <= x <= x_max and y_min <= y <= y_max and z_min <= z <= z_max:
                        pixel = 1.0
                    else:
                        pixel = 0.0

                    listed_points.append([pixel])

        self.alphamask = (self.alpha*listed_points)
        self.pixlist = listed_points*self.color.c
        #self.pixlist = listed_points*self.alpha*self.color.c


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
