import vox
import vox_points
import vox_color
import fastopc as opc
import time
import numpy as np
import math

usfullshit = {'pixelcount': 6400}
##****************************************##
IP_PORT = '127.0.0.1:7890'
IP_PORT = '10.0.0.10:7890'

client = opc.Client(IP_PORT)
if client.can_connect():
    print '    connected to %s' % IP_PORT
else:
    # can't connect, but keep running in case the server appears later
    print '    WARNING: could not connect to %s' % IP_PORT
##****************************************##
#colorspeed = 1
#maxspeed = 30
#speed range 29
#(energy*29)+1
energy = .01 ###############3 set this to look at "global energy"###
comp = vox.comp()
comp.addshift(sps = -.99)


huecount = 0
wc1 = vox_color.color(0)
c = [vox_points.surface(color = wc1, size = 2, alpha = .4)]
c.append(vox_points.surface(color = wc1, size = 2, alpha = .4))
c[0].addrwave(zoffset = 2,freq = -1)
c[1].addrwave(zoffset = 2, freq = 1)
while 1:
    for x in c:
        x.update()
    pixels = comp.complayers(c)
    client.put_pixels(pixels, channel=0)
    huecount += (1+energy*29)
    wc1.changecolor(huecount)
    time.sleep(1/30.)
