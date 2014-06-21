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

locationbounds = 3

c=[]
comp = vox.comp()
c.append(vox_shapes.sphere([[0],[0],[0]],ranbowlist[-1],size = .1))
flipflop = 0


def start():
	return

def create():
	return

def exit():
	return

def frameStart(frame):	
    spoint = [[random.uniform(-locationbounds,locationbounds)],[random.uniform(-locationbounds,locationbounds)],[random.uniform(-locationbounds,locationbounds)]]
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
    
    minsize = (1-energy)*.7+.4
    growspeed = energy*.17+.03
	return

def frameEnd(frame):
	return

def playState(state):
	return
	
