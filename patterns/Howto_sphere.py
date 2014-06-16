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
#make a red color layer
cl_red = vox_color.color([1.0,0.0,0.0])
#make an array to track layers
layer = []
#add 3 spheres to the list

#the first one will be at location x=0,y=0,z=0
#we will use the remade color layer cl_red
layer.append(vox_shapes.sphere([[0.0],[0.0],[0.0]],cl_red))

#this green sphere can be added by passing location and rgb colors 0-1.
#default size is 1 so we change it to .5.  default mode is fade chaning
#it to fill so it will not fade out around the outside
layer.append(vox_shapes.sphere([[0.0],[1.0],[0.0]],[0.0,1.0,0.0],size = .5, mode = 'fill'))

#blue layer with lowered alpha.  lower the max speed to .07 meter per frame
#the ratio that it will try to move per frame to it's target is redused
#to a fifth and it will be a bubble (faded in the middle full outside)
layer.append(vox_shapes.sphere([[0.0],[-1.0],[0.0]],[0.0,0.0,1.0], alpha = .8, maxspeed = .07, ratio = .2, mode = 'bubble'))

starttime = time.time()
while 1:
    #see how long we have been running
    changedtime = time.time()-starttime
    
    #setting location of sphere
    layer[0].pos = np.array([[0.0,0.0,np.sin(changedtime)]])
    
    #setting target location,  the sphere will move to that location
    #limeted by the max speed and the ratio of distance it tries to cover
    #in relation to distance from target
    layer[1].target = np.array([[0.0,1.0,np.sin(changedtime)]])
    layer[2].target = np.array([[0.0,-1.0,np.sin(changedtime)]])
    for x in layer:
        #update each layer
        x.update()
    #pixels will hold the final array after the compositor if finished
    pixels = comp.complayers(layer)
    #send them to the server
    client.put_pixels(pixels, channel=0)
    #sleep (note I hate this)
    time.sleep(1/30.)
