import time
import math

class line():
    pix=[] #this is to be used to store pixel location, size, color, alpha
    #x = x axis location in meters
    #y = y axis location in meters
    #l = length of line in meters
    #s = steps (number of pixels in the line)
    #scale = scale to make math easier
    def __init__(self,x,y,l,s,scale):
        self.x = x
        self.y = y
        self.length = l
        self.steps = s
        self.scale= scale #scale so that each LED on a strip is an int
        self.sSize = l/s
        self.rgb= [[0,0,0,0,0,0] for x in range(s)]
        #self.alpha = [0 for x in range(s)]
        
        self.scale1 = float(1)/s #scale to make full strip = 1 sp we can work with colors better
        print s,self.scale1
 
    def blank(self):
        self.rgb= [[0,0,0,0,0,0] for x in range(self.steps)]
    
    def renderc(self):
        rgba= [[0,0,0] for x in range(self.steps)]
    
    def rendera(self):
        rgba= [[0,0,0] for x in range(self.steps)]
        
    def sincolor(self,Xoff,time):
        for s in range(self.steps):
            self.rgb[s][0] = math.sin((s*self.scale1)*(2*math.pi)+Xoff[0]+time)*.5+.5
            self.rgb[s][1] = math.sin((s*self.scale1)*(2*math.pi)+Xoff[1]+time)*.5+.5
            self.rgb[s][2] = math.sin((s*self.scale1)*(2*math.pi)+Xoff[2]+time)*.5+.5
    
    def coswave(self, t, c1, c2):
        self.blank()
        p = math.cos(self.x*c1+t)+math.cos(self.y*c2+t)
        self.closepoint(1,p)
        return p
    
    def radwave(self, t, c1):
        self.blank()
        p = math.cos((self.x-5)*c1*math.pi+t)+math.cos((self.y-5)*c2*math.pi+t)
        self.closepoint(1,p)
        return p
    
    def closepoint(self, ps, z):
        s = float(4)/72
        p = int(math.floor((z+2)/s))
        self.rgb[p] = [1,1,1,1,1,1]
    
class cube:
    #xyf = path of xy file
    #height = height of cube in meters
    #steps = number of pixels in z axis
    def __init__(self,xyf,height,steps, alpha=False):
        self.xy = []
        self.lines = []
        f = open(xyf,"r")
        scale= 1/(height/steps)
        for i in f:
            x= float(i.split(',')[0].strip())
            y= float(i.split(',')[1].strip())
            self.xy.append([x,y])
            self.lines.append(line(x*scale,y*scale,height*scale,steps,scale))
        self.sTime = time.time()
    
    #tylers surface wave using cos
    def surfacewave(self,time):
        for s in self.lines:
            s.coswave(time,1,1)
    #not working radiating wave
    def radwave(self, time):
        for s in self.lines:
            s.radwave(time,1)
    #Rainbowing effect over the cube.
    def rainbow(self,time):
        #math.sin(x*2*math.pi).5+.5
        #math.sin(x*2*math.pi+2).5+.5
        #math.sin(x*2*math.pi+4).5+.5
        for l in self.lines:
            l.sincolor([0,2,4],time)
        pass
    
    def pixlist(self):
        p = []
        for l in self.lines:
            for r in l.rgb:
                p.append(r)
        return p
#background class for the lowest layer.  most likely going to remove
class background(cube):
    pass
#compositor will take all the layers and make them into a flat stream
#that can be send to the cube
class compositor():
    def __init__(self):
        self.mult = 256
#scene    
class scene():
    def __init__(self):
        pass

    def update(self):
        pass
        
    def add_layer(self):
        pass
