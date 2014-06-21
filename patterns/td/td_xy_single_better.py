# me is this DAT.
# 
# frame is the current frame.
# state is true if the timeline is paused.
# 
# Make sure the corresponding toggle is enabled in the Execute DAT.

import vox
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

shift = 0
step = 2


comp = vox.comp()
comp.addfade(.8)
co = vox_color.color([0,0,0])
co.vrainbow(shift,step)
c = [vox_points.surface(co,3,.3,1.)]
c[0].addxywave(xfreq = 1.9, yfreq = 1.9)

def start():
	return

def create():
	return

def exit():
	return

def frameStart(frame):
    global shift,step,c,co,comp
    for x in c:
        x.update()
    shift += 1
    co.vrainbow(shift,step)
    pixels = comp.complayers(c)
    client.put_pixels(pixels, channel=0)
    return

def frameEnd(frame):
	return

def playState(state):
	return
	
