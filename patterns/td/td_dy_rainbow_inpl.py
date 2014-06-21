# me is this DAT.
# 
# frame is the current frame.
# state is true if the timeline is paused.
# 
# Make sure the corresponding toggle is enabled in the Execute DAT.

import vox
import vox_points
import vox_color
import vox_shapes
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

minsize = 1.1
growspeed = .05
shiftspeed = .1

c=[]
comp = vox.comp()
c.append(vox_shapes.sphere([[0],[0],[0]],ranbowlist[-1],size = 5))
flipflop = 0
stime = time.time()
stage = 0
spoint = [[0],[0],[0]]


def start():
	return

def create():
	return

def exit():
	return

def frameStart(frame):	
    global minsize,growspeed,shiftspeed,spoint
    if c[0].size<4.5:
        if flipflop==len(ranbowlist):
            flipflop=0
        c.insert(0,vox_shapes.sphere(spoint,ranbowlist[flipflop],size=5))
        flipflop = flipflop+1
    if len(c)>1:
        if c[-1].size<0:
            c.pop(-1)
    for s in c:
        s.size = s.size-growspeed
    for x in c:
        x.update()
    pixels = comp.complayers(c)
    client.put_pixels(pixels, channel=0)
    return

def frameEnd(frame):
	return

def playState(state):
	return
	
