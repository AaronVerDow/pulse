import vox
import vox_shapes
import vox_color
import fastopc as opc
import time
import numpy as np
import math
import random

usfullshit = {'pixelcount': 6400}
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

#spawn a compositer
comp = vox.comp()
#make a color layer
co = vox_color.color([1.0,1.0,1.0])
#over ride the color layer with a fade
co.vfadeinit([1.0,0.0,0.0],[0.0,0.0,1.0])
#make an array to track layers and drop a fill screen layer in
layer = [vox.fillscreen(co)]
#add a sphere on top of that.  alpha = 'invert' will block anything
#not behind the sphere.  This makes all layers beblow it into a color 
#layer in a way.
layer.append(vox_shapes.sphere([[0],[0],[0]],[1.0,1.0,1.0],alpha = 'invert',mode = 'fill'))
while 1:
    for x in layer:
        #update each layer
        x.update()
    #pixels will hold the final array after the compositor if finished
    pixels = comp.complayers(layer)
    #send them to the server
    client.put_pixels(pixels, channel=0)
    #sleep (note I hate this)
    time.sleep(1/30.)
