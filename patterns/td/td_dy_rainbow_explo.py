# me is this DAT.
# 
# frame is the current frame.
# state is true if the timeline is paused.
# 
# Make sure the corresponding toggle is enabled in the Execute DAT.

import vox
import vox_shapes
import vox_points
import vox_color
import fastopc as opc
import time
import numpy as np
import math
IP_PORT = '10.0.0.10:7890'

client = opc.Client(IP_PORT)

n_pixels = 6400

##****************************************##

ranbowlist = [[1.,0.,0.],
                [1.,.5,0.],
                [1.,1.,0.],
                [.5,1.,0.],
                #[0.,1.,0.],
                [0.,1.,.5],
                [0.,1.,1.],
                [0.,.5,1.],
                [0.,0.,1.],
                [.5,0.,1.],
                [1.,0.,1.],
                [1.,0.,.5]]

energy = .01 ###############3 set this to look at "global energy"###
#minsize .4
#maxsize 1.1
#size range .7
#size (1-energy)*.7+.4
minsize = 1.1
#mingrow .03
#maxgrow .2
#growrange .17
#grow energy*.17+.03
growspeed = .03
shiftspeed = .01

c=[]
comp = vox.comp()
c.append(vox_shapes.sphere([[0],[0],[0]],ranbowlist[-1],size = .1))
flipflop = 0
spoint = [[0],[0],[0]]

def start():
	return

def create():
	return

def exit():
	return

def frameStart(frame):
    global minsize,growspeed,shiftspeed,ranbowlist,flipflop,spoint,energy,c,comp
    if c[-1].size>minsize:
        if flipflop==len(ranbowlist):
            flipflop=0
        c.append(vox_shapes.sphere(spoint,ranbowlist[flipflop],size=.1))
        flipflop = flipflop+1
    if len(c)>1:
        if c[1].size>9:
            c.pop(0)
    for s in c:
        s.size = s.size+growspeed
    for x in c:
        x.update()
    pixels = comp.complayers(c)
    client.put_pixels(pixels, channel=0)
    
    spoint = np.clip([[spoint[0][0]+random.uniform(-shiftspeed,shiftspeed)],[spoint[1][0]+random.uniform(-shiftspeed,shiftspeed)],[spoint[2][0]+random.uniform(-shiftspeed,shiftspeed)]],gd.xmin,gd.xmax)
    return

def frameEnd(frame):
	return

def playState(state):
	return
	
