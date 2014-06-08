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

hotlist = [[1.0,0.0,0.0],
            [.75,.15,0.0],
            [1.0,0.0,.2],
            [.8,.2,.2]]
coldlist = [[0.0,0.0,1.0],
            [0.0,1.0,0.0],
            [0.2,.7,.2],
            [.1,.1,.8]]

ranbowlist = [[1.,0.,0.],
                [1.,.5,0.],
                [1.,1.,0.],
                [.5,1.,0.],
                [0.,1.,0.],
                [0.,1.,.5],
                [0.,1.,1.],
                [0.,.5,1.],
                [0.,0.,1.],
                [.5,0.,1.],
                [1.,0.,1.],
                [1.,0.,.5]]

c=[]
comp = vox.comp()
comp.addfade(.97)
co = vox_color.color([1.0,0.0,0.0])
c.append(vox_shapes.sphere([[0],[0],[0]],ranbowlist[0],size = 1))
c.append(vox_shapes.sphere([[0],[0],[0]],ranbowlist[4],size = 1))
c.append(vox_shapes.sphere([[0],[0],[0]],ranbowlist[8],size = 1))
flipflop = 0
stime = time.time()
while 1:
    tc = time.time()-stime
    c[0].pos = np.array([[np.sin(tc+2)*1.5,np.sin(tc)*1.5,np.sin(tc)/2]])
    c[1].pos = np.array([[np.sin(tc+4)*1.5,np.sin(tc+2)*1.5,np.sin(tc+.4)/2]])
    c[2].pos = np.array([[np.sin(tc)*1.5,np.sin(tc+2)*1.5,np.sin(tc+.2)/2]])
    for x in c:
        x.update()
    pixels = comp.complayers(c)
    client.put_pixels(pixels, channel=0)
    time.sleep(1/32.)
