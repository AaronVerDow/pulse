import numpy as np

##*************read grid******************##
f = open('grid.txt','r')
xyz = []
for i in f:
    x= float(i.split(',')[0].strip())
    y= float(i.split(',')[1].strip())
    z= float(i.split(',')[2].strip())
    xyz.append([x,y,z])
grid3d = np.array(xyz)
f.close()
##****************************************##
##************read 2dgrid*****************##
f = open('2dgrid.txt','r')
xy = []
for i in f:
    x= float(i.split(',')[0].strip())
    y= float(i.split(',')[1].strip())
    xy.append([x,y])
grid2d = np.array(xy)
f.close()
##****************************************##
##************read Z axis*****************##
f = open('zgrid.txt','r')
z = []
for i in f:
    p= float(i.strip())
    z.append([p])
f.close()
grid1d = np.array(z)
zcount = len(z)
##****************************************##

length = 4.572
width = 4.572
height = 2.4384
stripcount = 100
zsteps = height/zcount
zmax = 1.2192
zmin = -1.2192
xmax = width/2
xmin = (width/2)*-1
ymax = length/2
ymin = (length/2)*-1
pixelcount = 6400
