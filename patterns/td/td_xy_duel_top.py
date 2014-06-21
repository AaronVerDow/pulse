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
import random
IP_PORT = '10.0.0.10:7890'

client = opc.Client(IP_PORT)

n_pixels = 6400

##****************************************##

tshift = 0
dshift = 0
tcolor = 0
bcolor = 240


comp = vox.comp()
co = vox_color.color([0,0,0])
co.vfadeinit(tcolor,bcolor)
c = [vox_points.dualsurface(co,0,-3,.75)]
c[0].addxywave(target = c[0].moda)


def start():
	return

def create():
	return

def exit():
	return

def frameStart(frame):	
    global tshift,dshift,tcolor,bcolor,c,co
    for x in c:
        x.update()
    co.vfadeshift(tshif,bshift)
    pixels = comp.complayers(c)
    client.put_pixels(pixels, channel=0)
    return

def frameEnd(frame):
	return

def playState(state):
	return
	
