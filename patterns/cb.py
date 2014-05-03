import time
import math
import numpy as np

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
        self.rgb= np.zeros((s,3),dtype=np.float16)#creat an np.array of zeros for each point
        self.alpha = np.ones((s,3),dtype=np.float16)#creat an np.array of zeros for each point
        
        self.scale1 = float(1)/s #scale to make full strip = 1 sp we can work with colors better
        print s,self.scale1
 
    def blank(self):
        self.rgb= [[0,0,0,0,0,0] for x in range(self.steps)]
    
    def renderc(self):
        rgba= [[0,0,0] for x in range(self.steps)]
    
    def rendera(self):
        rgba= [[0,0,0] for x in range(self.steps)]
        
    def sincolor(self,Xoff,time):######Need to convert this to np some how######
        for s in range(self.steps):#####################################
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
        rgblist = []
        alphalist = []
        for l in self.lines:
            rgblist.append(l.rgb)
            alphalist.append(l.alpha)
        self.colors= [np.concatenate(rgblist),np.concatenate(alphalist)]
        return self.colors
#background class for the lowest layer.  most likely going to remove
class background(cube):
    pass
#compositor will take all the layers and make them into a flat stream
#that can be send to the cube
class compositor():
    def background(self,colors):
        return np.multiply(colors[0],colors[1])
    
    def flatten(self,layers,maxcolor = 255):
        pixels = []
        if len(layers)==1:
            pixels=self.background(layers[0].colors)
        else:
            for l in range(len(layers)):
                if 1==0:
                    pixels=self.background(layers[0])
                else:
                    pixeltemp=self.background(layers[l])
                    for c in range(len(pixels)):
                        #using the invers of the next alpha layer
                        #to tone down the current mesh
                        pixels[c][0]=(l.colors[c][0]*(1-l[1][0]))+pixeltemp[0]
                        pixels[c][1]=(pixels[c][0]*(1-l[1][1]))+pixeltemp[1]
                        pixels[c][2]=(pixels[c][0]*(1-l[1][2]))+pixeltemp[2]
        return np.asarray((pixels*maxcolor),dtype=np.int32)

#compile final image
class comp():
    #Take layers(an array of layer objects that have pixlist and
    # alphamask. Turns them into single image 
    def complayers(self, layers):
        rcomp = []
        for x in range(len(layers)):
            if x == 0:
                rcomp = layers[x].pixlist
            #if we have more the one layer we use the current layer
            #being added and use its alpha map to mask the rolling layer
            else:
                rcomp = rcomp*(1-layers[x].alphamask)+layers[x].pixlist
        return rcomp*255
#3425
#scene    
class scene():
    def __init__(self):
        pass

    def update(self):
        pass
        
    def add_layer(self):
        pass
