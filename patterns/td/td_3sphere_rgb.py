# me is this DAT.
# 
# frame is the current frame.
# state is true if the timeline is paused.
# 
# Make sure the corresponding toggle is enabled in the Execute DAT.

import vox
import vox_shapes
import vox_color
import fastopc as opc
import time
import numpy as np
import math
IP_PORT = '10.0.0.10:7890'

client = opc.Client(IP_PORT)

n_pixels = 6400

##****************************************##

dis1 = 1.5
dis2 = 1.5

c=[]
comp = vox.comp()
comp.addfade(.97)
c.append(vox_shapes.sphere([[0],[0],[0]],0,size = 1))
c.append(vox_shapes.sphere([[0],[0],[0]],120,size = 1))
c.append(vox_shapes.sphere([[0],[0],[0]],240,size = 1))
stime = time.time()

def start():
	return

def create():
	return

def exit():
	return

def frameStart(frame):
    global tshift,dshift,tcolor,bcolor,c,comp,stime,dis1,dis2
    tc = time.time()-stime
    c[0].pos = np.array([[np.sin(tc+2)*dis1,np.sin(tc)*dis2,np.sin(tc)/2]])
    c[1].pos = np.array([[np.sin(tc+4)*dis2,np.sin(tc+2)*dis1,np.sin(tc+.4)/2]])
    c[2].pos = np.array([[np.sin(tc)*dis1,np.sin(tc+2)*dis1,np.sin(tc+.2)/2]])
    for x in c:
        x.update()
    pixels = comp.complayers(c)
    client.put_pixels(pixels, channel=0)
    return

def frameEnd(frame):
	return

def playState(state):
	return
	
