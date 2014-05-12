import griddata as gd
import numpy as np

class color(object):
    #default colors for the lazy
    clist =[['black',[0.,0.,0.]],
            ['white',[1.,1.,1.]],
            ['red',[1.,0.,0.]],
            ['green',[0.,1.,0.]],
            ['blue',[0.,0.,1.]],
            ['yellow',[1.,1.,0.]],
            ['purple',[1.,0.,1.]],
            ['cyan',[0.,1.,1.]]]
    def __init__(self, color):
        global n_pixels #using global for pixel number
        #check what type of color layer: flat default, passed rgb, or 
        #Procedural generation
        if type(color) is list:
            if len(color) == 3:
                print 'rgb vals was sent'
                self.c = np.array(color).reshape(1,3)
            else:
                print 'a list was sent but it was the wrong size'
                print 'setting to black'
                self.c = np.array([0.,0.,0.]).reshape(1,3)
                pass #did not pass rgb list,  kill it with fire
        elif any(color.lower() == i[0] for i in self.clist):##this may  need fixed##
            print 'def color was passed'
            pass #build flat color
 #       elif:
 #           print "else"
        else:
            print "passed color was not rgb, default color, or known pattern"
            print 'setting to black'
            self.c = np.array([0.,0.,0.]).reshape(1,3)

    #vertical fade from toprgb down to bottomrgb
    def vfadeinit(self, toprgb, bottomrgb):
        strip= []
        rstep = (toprgb[0]-bottomrgb[0])/64 ##remve hard numbers
        gstep = (toprgb[1]-bottomrgb[1])/64
        bstep = (toprgb[2]-bottomrgb[2])/64
        for x in range(100): ##remove hard numbers
            for i in range(64): #remove hard numbers
                strip.append([toprgb[0]-i*rstep,toprgb[1]-i*gstep,toprgb[2]-i*bstep])
        self.c = strip
