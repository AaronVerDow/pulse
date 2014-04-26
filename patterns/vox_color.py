class color():
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
        if any(color.lower() == i[0] for i in self.clist):##this may  need fixed##
            print 'def color was passed'
            pass #build flat color
        elif type(color) is list:
            if len(color) == 3:
                print 'rgb vals was sent'
                self.c = color
            else:
                print 'a list was sent but it was the wrong size'
                print 'setting to black'
                self.c = [0.,0.,0.]
                pass #did not pass rgb list,  kill it with fire
 #       elif:
 #           print "else"
        else:
            print "passed color was not rgb, default color, or known pattern"
            print 'setting to black'
            self.c = [0.,0.,0.]
