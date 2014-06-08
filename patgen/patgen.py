#!/usr/bin/env python
xy = []
points = []

L = 4.572
W = 4.572
Pheight = 2.4384

step = L/10

xoff = (L/2)-(step/2)
yoff = (W/2)-(step/2)
zoff = Pheight/2


pstep = Pheight/64


for x in range(10):
    for y in range(10):
        xy.append([step*x-xoff,step*y-yoff])
        for z in range(64):
            t =[step*x-xoff,step*y-yoff,Pheight-(pstep*z)-zoff]
            points.append(t)

print len(points)

f = open('grid.json','w')
f.write('[\n')
for x in range(len(points)):
    if x!=len(points)-1:
        f.write('  {"point": [%.2f, %.2f, %.2f]},\n' % (points[x][0], points[x][1], points[x][2]))
    else:
        f.write('  {"point": [%.2f, %.2f, %.2f]}\n' % (points[x][0], points[x][1], points[x][2]))
f.write(']')
f.close()

f = open('grid.txt','w')
for x in points:
    f.write('%.2f,%.2f,%.2f\n' % (x[0], x[1], x[2]))
f.close()

f = open('2dgrid.txt','w')
for i in xy:
    f.write('%.2f,%.2f\n' % (i[0], i[1]))
