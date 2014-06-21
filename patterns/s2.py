import cb
import vox_points
import vox_color
import opc
import time
import numpy as np

usfullshit = {'pixelcount': 6400}
##****************************************##
IP_PORT = '127.0.0.1:7890'
#IP_PORT = '192.168.1.100:7890'
IP_PORT = '10.0.0.10:7890'

client = opc.Client(IP_PORT)
if client.can_connect():
    print '    connected to %s' % IP_PORT
else:
    # can't connect, but keep running in case the server appears later
    print '    WARNING: could not connect to %s' % IP_PORT
##****************************************##


comp = cb.comp()
co = vox_color.color([0,0,0])
co.vfadeinit([1,0.0,0.0],[0.0,0.0,1.0])
c = [vox_points.dualsurface(co,0,-3,.75)]
#c.append(vox_points.surface(xy,[1,0,1],3.2,.3,1,**usfullshit))
c[0].addxywave(target = c[0].moda)
#c[0].addxywave(target = c[0].modb, xzoffset=1)
###mdd = c[0].mod[-1]
#c[1].addxywave()
###print c[0].mod
while 1:
    for x in c:
        x.update()
    pixels = comp.complayers(c)
    client.put_pixels(pixels, channel=0)
#    f = open('out','w')
#    for x in c[0].pixlist:
#        f.write(str(x)+'\n')
##    f.write(c[0].pixlist)
#    exit()
