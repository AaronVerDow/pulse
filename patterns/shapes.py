import numpy as np
import scipy.spatial as sp

class sphere():
    
    def __init__(self, bpos, alpha, points, size = 1):
        self.pos = np.transpose(bpos)
        self.alpha = alpha
        self.points = points
        self.size = size

    #def calcdist(self, pos):
        #return sp.distance.cdist(points,ballpos)
    def calcdist(self, pos):
        print np.shape(np.clip(self.size-sp.distance.cdist(self.points,pos),0,1))

    #def moveball(ball):
        #global ballspeed
        #if (ballpos[0,1] < -2.286) or (ballpos[0,1] > 2.286):
            #ballspeed = ballspeed * -1
        #b= float(ballpos[0,1]+ballspeed)
        #ballpos[0,1]= b

    def update(self):
        print self.calcdist(self.pos)
    #def flipandinvert(n):
        #return (n-1)*-255
