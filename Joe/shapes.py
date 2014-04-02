import numpy as np
import scipy.spatial as sp

class sphere():
    
    def calcdist():
        return sp.distance.cdist(points,ballpos)

    def moveball(ball):
        global ballspeed
        if (ballpos[0,1] < -2.286) or (ballpos[0,1] > 2.286):
            ballspeed = ballspeed * -1
        b= float(ballpos[0,1]+ballspeed)
        ballpos[0,1]= b

    def flipandinvert(n):
        return (n-1)*-255
