import numpy as np
import scipy.spatial as sp
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
        #handling ways that alpha can be passed
        if type(alpha) == int:
            return [alpha,alpha,alpha]
        else:
            return alpha

#spheres for making ... spheres
class sphere(layer):
    pixlist = []
    alphamask = []
    #take center position of sphere, color in rgb 0-1 or a color object,
    #size, mode (fill or fade), and alpha (0-1 as a scaler or rgb list)
    def __init__(self,spos, color, points, size = 1, mode = 'fade', alpha = 1):
        self.pos = np.transpose(spos)
        self.size = size
        self.points = points
        
        #pass color to colorhandle in layer class to set it up.
        self.color = self.colorhandle(color)
        #pass alpha to alpha handle in layer class to set it up.
        self.alpha = self.alphahandle(alpha)

    def calcdist(self, pos):
        #calculates the distance from center for each pixel.  clips so
        #we don't have any values out of the range 0-1
        return np.clip(self.size-sp.distance.cdist(self.points,pos),0,1)


    def update(self):
        dis = self.calcdist(self.pos)
        self.pixlist = (self.alpha*dis)*self.color.c
        self.alphamask = (self.alpha*dis)
    
    def maskgen(self):
        pass
            
    #def flipandinvert(n):
        #return (n-1)*-255

#base class for holding array of points
class pointholder():
    points = []
    pixlist = []
    def add(self,line,x,y,z,size):
        self.points.append([line, x, y, z, size])
    def remove(self,num):
        points.pop(num)

    def update(self):
        pass
        

#surface of points
class surface(pointholder,layer):
    def __init__(self,xy,color,size=0,z=0):
        for l in range(len(xy)):
            self.add(l,xy[l][0],xy[l][1],z,size)
        self.color = colorhandle(color)

    #changing the starting z val of all points in the surface
    def changez(self,z):
        for l in points:
            l[3]=z
    
    #changing the size of all points in the surface
    def changesize(self,size):
        for l in points:
            l[4]=size

class rpoints(pointholder,layer):
    def __init__(self,pnumber,ttl,size):
        pass

class point():
    def __init__(self, linenum, z = 0, size = 0):
        self.z = z
        self.size = size
        self.line = linenum
