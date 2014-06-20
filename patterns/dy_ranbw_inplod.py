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

minsize = 1.1
growspeed = .05
shiftspeed = .1

for x in range(30):
    print ' '
    
print "Global energy level set to 1"

c=[]
comp = vox.comp()
c.append(vox_shapes.sphere([[0],[0],[0]],ranbowlist[-1],size = 5))
flipflop = 0
stime = time.time()
stage = 0
spoint = [[0],[0],[0]]
while 1:
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
    time.sleep(1/32.)
    if time.time()-stime>15 and stage == 0:
        print "Global energy level set to 5"
        minsize = .8
        growspeed = .1
        stage = 1
    elif time.time()-stime>25 and stage == 1:
        print "Global energy level set to 7"
        minsize = .5
        growspeed = .15
        stage = 2
    elif time.time()-stime>30 and stage == 2:
        print "Global energy level set to 10"
        minsize = .4
        growspeed = .2
        stage = 3
    elif stage == 3:
        pass
#        spoint = [[spoint[0][0]+random.uniform(-shiftspeed,shiftspeed)],[spoint[1][0]+random.uniform(-shiftspeed,shiftspeed)],[spoint[2][0]+random.uniform(-shiftspeed,shiftspeed)]]
        
    print len(c)
