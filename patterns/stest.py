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
f = open('grid.txt','r')
xyz = []
for i in f:
    x= float(i.split(',')[0].strip())
    y= float(i.split(',')[1].strip())
    z= float(i.split(',')[2].strip())
    xyz.append([x,y,z])
points = np.asarray(xyz)
print points
#c = cb.background("2dgrid.txt",2.4384,72)
c = shapes.sphere([[0],[0],[0]],[0,1,0],points)
comp = cb.compositor()
pixels = []
start_time = time.time()

while 1:
    pixels = []
    current_time = start_time - time.time()
    #rainbow(current_time)
    #p = c.pixlist()#works as an update right now
    #print comp.flatten([c])
    #client.put_pixels(comp.flatten([c]).tolist(), channel=0)
    c.update()