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

#colorspeed = 1
#maxspeed = 30
#speed range 29
#(energy*29)+1
energy = .01 ###############3 set this to look at "global energy"###
comp = vox.comp()
comp.addshift(sps = -.99)


huecount = 0
wc1 = vox_color.color(0)

c = [vox_points.surface(color = wc1, size = 2, alpha = .4)]
c.append(vox_points.surface(color = wc1, size = 2, alpha = .4))
c[0].addrwave(zoffset = 2,freq = -1)
c[1].addrwave(zoffset = 2, freq = 1)

def start():
	return

def create():
	return

def exit():
	return

def frameStart(frame):
    global huecount,wc1,comp,c
    for x in c:
        x.update()
    pixels = comp.complayers(c)
    client.put_pixels(pixels, channel=0)
    huecount += (1+energy*29)
    wc1.changecolor(huecount)
    return

def frameEnd(frame):
	return

def playState(state):
	return
	
