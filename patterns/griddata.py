import numpy as np

x_steps = 10
y_steps = 10
z_steps = 64

##*************read grid******************##
f = open('grid.txt','r')
xyz = []
exploded = np.zeros((x_steps,y_steps,z_steps,4))
##c = count
xc = 0
yc = 0
zc = 0
for i in f:
    x= float(i.split(',')[0].strip())
    y= float(i.split(',')[1].strip())
    z= float(i.split(',')[2].strip())
    xyz.append([x,y,z])

    if zc == z_steps:
        zc = 0
        yc = yc + 1
    if yc == y_steps:
        yc = 0
        xc = xc + 1
    exploded[xc][yc][zc] = [x,y,z,0]
    zc = zc + 1
    
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
