import numpy as np
import scipy.spatial as sp
import vox_color

#spheres for making ... spheres
class sphere():
    pixlist = []
    #take center position of sphere, color in rgb 0-1 or a color object,
    #size, mode (fill or fade), and alpha (0-1 as a scaler or rgb list)
    def __init__(self,spos, color, points, size = 1, mode = 'fade', alpha = 1):
        self.pos = np.transpose(spos)
        self.size = size
        self.points = points
        #handling veriable in the way color may be passed
        if type(color) == vox_color.color: #if color is of color object we are good
            print "that is a god damn color"
            self.color = color
        elif type(color) == list:#if color is a list make a color object out of it
            self.color = vox_color.color(color)
        else:#else make it just black, you should not have fucked up if you wanted color
            self.color = vox_color.color('black')
        #handling ways that alpha can be passed
        if type(alpha) == int:
            self.alpha = [alpha,alpha,alpha]
        else:
            self.alpha = alpha

    def calcdist(self, pos):
        #calculates the distance from center for each pixel.  clips so
        #we don't have any values out of the range 0-1
        return np.clip(self.size-sp.distance.cdist(self.points,pos),0,1)


    def update(self):
        self.pixlist = (self.alpha*self.calcdist(self.pos))*self.color.c
        print self.pixlist[3421]
        #print self.points[3421]
        #print self.pos
        print sp.distance.cdist([self.points[3421]],self.pos)
        
    #def flipandinvert(n):
        #return (n-1)*-255
