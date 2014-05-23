import cb

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

n_pixels = 6400



c = cb.background("2dgrid.txt",2.4384,72)
comp = cb.compositor()
pixels = []
start_time = time.time()
while 0:
    pixels = []
    current_time = start_time - time.time()
    c.surfacewave(current_time)
    #c.radwave(current_time)
    p = c.pixlist()
    for pi in p:
        pixels.append([pi[0]*256,pi[1]*256,pi[2]*256])
    client.put_pixels(pixels, channel=0)

while 1:
    pixels = []
    current_time = start_time - time.time()
    c.rainbow(current_time)
    p = c.pixlist()#works as an update right now
    print comp.flatten([c])
    client.put_pixels(comp.flatten([c]).tolist(), channel=0)
