#!/usr/bin/env python
import vox
import vox_points
import vox_color
import fastopc as opc
#import opc
import time
import numpy as np

usfullshit = {'pixelcount': 6400}

##*************read grid******************##
f = open('grid.txt','r')
xyz = []
for i in f:
    x= float(i.split(',')[0].strip())
    y= float(i.split(',')[1].strip())
    z= float(i.split(',')[2].strip())
    xyz.append([x,y,z])
f.close()
points = np.asarray(xyz)
usfullshit['3dgrid'] = points
print len(points)
##****************************************##
##************read 2dgrid*****************##
f = open('2dgrid.txt','r')
xy = []
for i in f:
    x= float(i.split(',')[0].strip())
    y= float(i.split(',')[1].strip())
    xy.append([x,y])
usfullshit['2dgrid'] = np.array(xy)
f.close()
##****************************************##
##************read Z axis*****************##
f = open('zgrid.txt','r')
z = []
for i in f:
    p= float(i.strip())
    z.append([p])
f.close()
usfullshit['1dgrid'] = np.array(z)
usfullshit['zcount'] = len(z)
##****************************************##

usfullshit['length'] = 4.572
usfullshit['width'] = 4.572
usfullshit['height'] = 2.4384
usfullshit['stripcount'] = 100
usfullshit['zsteps'] = usfullshit['height']/usfullshit['zcount']
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


comp = vox.comp()
#comp.addparticlemap()
comp.addfade(.8)
co = vox_color.color([0,0,0])
co.vfadeinit([1.0,0.0,0.0],[0.0,0.0,1.0])
print np.shape(co.c)
c = [vox_points.surface(co,3,.3,1.)]
#c.append(vox_points.surface(xy,[0,0,1],6,.3,1))
c[0].addrwave(amp = 1, freq = -1)
#c[0].addxywave()
#c[1].addsinwave()
print c[0].mod
while 1:
    for x in c:
        x.update()
    pixels = comp.complayers(c)
    client.put_pixels(pixels, channel=0)
    time.sleep(1/30.)
