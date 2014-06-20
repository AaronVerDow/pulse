import vox
import vox_shapes
import vox_color
import fastopc as opc
import time
import numpy as np
import math
import random

usfullshit = {'pixelcount': 6400}
##****************************************##
IP_PORT = '127.0.0.1:7890'
#IP_PORT = '192.168.1.100:7890'
#IP_PORT = '10.0.0.10:7890'

client = opc.Client(IP_PORT)
if client.can_connect():
    print '    connected to %s' % IP_PORT
else:
    # can't connect, but keep running in case the server appears later
    print '    WARNING: could not connect to %s' % IP_PORT
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

for x in range(30):
    print ' '
    
print "Global energy level set to 1"

c=[]
comp = vox.comp()
c.append(vox_shapes.sphere([[0],[0],[0]],ranbowlist[-1],size = .1))
flipflop = 0
while 1:
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
    
    time.sleep(1/32.)
