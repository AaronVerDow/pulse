import cb
import shapes
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

n_pixels = 7200
##*************read grid******************##
f = open(grid.txt,'r')
xyz = []
for i in f:
    x= float(i.split(',')[0].strip())
    y= float(i.split(',')[1].strip())
    z= float(i.split(',')[1].strip())
    self.xyz.append([x,y,z])
points = np.asarry(xyz)

#c = cb.background("2dgrid.txt",2.4384,72)
c = shapes.sphere(0,[1,1,1])
comp = cb.compositor()
pixels = []
start_time = time.time()
while 0:
    pixels = []
    current_time = start_time - time.time()
    c.surfacewave(current_time)
    #c.radwave(current_time)
    p = c.pixlist()
    for pi in p:
        pixels.append([pi[0]*256,pi[1]*256,pi[2]*256])
    client.put_pixels(pixels, channel=0)

while 1:
    pixels = []
    current_time = start_time - time.time()
    c.rainbow(current_time)
    p = c.pixlist()#works as an update right now
    print comp.flatten([c])
    client.put_pixels(comp.flatten([c]).tolist(), channel=0)
