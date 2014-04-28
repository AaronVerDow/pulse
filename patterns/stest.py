import cb
import vox_shapes
import opc
import time
import numpy as np

IP_PORT = '127.0.0.1:7890'

client = opc.Client(IP_PORT)
if client.can_connect():
    print '    connected to %s' % IP_PORT
else:
    # can't connect, but keep running in case the server appears later
    print '    WARNING: could not connect to %s' % IP_PORT

n_pixels = 6400
##*************read grid******************##
f = open('grid.txt','r')
xyz = []
for i in f:
    x= float(i.split(',')[0].strip())
    y= float(i.split(',')[1].strip())
    z= float(i.split(',')[2].strip())
    xyz.append([x,y,z])
points = np.asarray(xyz)
print len(points)
##****************************************##


#c = cb.background("2dgrid.txt",2.4384,72)
c = vox_shapes.sphere([[0],[0],[0]],[0,1,0],points)
comp = cb.comp()
pixels = []
start_time = time.time()

layers = [c]
s=1.
d=1
c = vox_shapes.sphere([[0],[0],[0]],[1,0,0],points)
layers.append(c)
while 1:
    pixels = []
    current_time = start_time - time.time()
    for l in layers:
        l.update()
    pixels = comp.complayers(layers)
    client.put_pixels(pixels, channel=0)
    if d==1:
        s=s+0.1
        if s>=2:
            d=0
    else:
        s=s-0.1
        if s<=0.1:
            d=1
    layers[0].size=s
    layers[1].size=2-s
    time.sleep(1 / 60)
