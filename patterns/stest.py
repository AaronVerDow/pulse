import cb
import vox_shapes
import vox_color
#import opc
import fastopc as opc
import time
import numpy as np
import math

IP_PORT = '127.0.0.1:7890'

client = opc.Client(IP_PORT)
if client.can_connect():
    print '    connected to %s' % IP_PORT
else:
    # can't connect, but keep running in case the server appears later
    print '    WARNING: could not connect to %s' % IP_PORT

n_pixels = 6400



co = vox_color.color([1.0,0.0,0.0])
c = vox_shapes.sphere([[0],[0],[0]],co)
comp = cb.comp()
pixels = []
start_time = time.time()

layers = [c]
s=1.
d=1
c = vox_shapes.sphere([[0],[0],[0]],[1,0,0])
layers.append(c)
start_time = time.time()
loops = 0
while 1:
    pixels = []
    current_time = start_time - time.time()
    for l in layers:
        l.update()
    pixels = comp.complayers(layers)
    client.put_pixels(pixels, channel=0)
    if d==1:
        s=s+0.1
        if s>=2:
            d=0
    else:
        s=s-0.1
        if s<=0.1:
            d=1
            j= vox_color.color([np.random.random_sample(),np.random.random_sample(),np.random.random_sample()])
            layers[0].color = j
    layers[0].size=s
    layers[1].size=2-s
    time.sleep(1 / 32.)
