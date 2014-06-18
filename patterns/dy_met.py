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
#IP_PORT = '192.168.1.100:7890'

client = opc.Client(IP_PORT)
if client.can_connect():
    print '    connected to %s' % IP_PORT
else:
    # can't connect, but keep running in case the server appears later
    print '    WARNING: could not connect to %s' % IP_PORT
##****************************************##
#minspeed = .015
#maxspeed = .11
#speed range .095
#(energy*.095)+.015
#minpoints = 40
#maxpoints =  150
#point range 110
#(energy*110)+40
energy = .01 ###############3 set this to look at "global energy"###
comp = vox.comp()
comp.addfade(.8)
mxspd = .015
mxpnts = 40
co = vox_color.color([1.0,1.0,1.0])
c = [vox_points.pointgroup(color = co, size = 2, pcount = mxpnts, minspawnz = 1.2192, maxspawnz = 4, maxspeed = mxspd, ratio = 1.)]
c[0].addzshift(ztarget = -3)
c[0].addkillperam('z','less',-1.2192)
while 1:
    c[0].maxspeed = (energy*.095)+.015
    c[0].pcount = (energy*110)+40
    for x in c:
        x.update()
    pixels = comp.complayers(c)
    client.put_pixels(pixels, channel=0)
    time.sleep(1/30.)
