import numpy as np
import scipy.spatial as sp

class sphere():
    
    def __init__(self, bpos, alpha, size = 1):
        self.pos = bpos
        self.alpha = alpha
        self.size = size

    #def calcdist(self, pos):
        #return sp.distance.cdist(points,ballpos)
    def calcdist(self, pos):
        global points
        print np.clip(self.size-sp.distance.cdist(points,self.pos))

    #def moveball(ball):
        #global ballspeed
        #if (ballpos[0,1] < -2.286) or (ballpos[0,1] > 2.286):
            #ballspeed = ballspeed * -1
        #b= float(ballpos[0,1]+ballspeed)
        #ballpos[0,1]= b

    #def flipandinvert(n):
        #return (n-1)*-255
