# simple Doodle Jump clone - use arrow keys to move
# Changes made to the demo project as a part of one of the Coursera's online courses
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random

# helper functions
def camera(pos):
   """ convert from world coordinates to screen coordinates """
   return [pos[0]-offset[0],pos[1]-offset[1]]

def height(y):
    """ account for inversion of vertical coordinates """
    global h
    return h-y
 

class doodle:
    rebound = 7
    def __init__(self,pos):
        """ initialize doodle """
        self.pos = pos
        self.vel = [0,0]
    
    def nudge(self, x):
        """ method to push doodle to left or right """
        self.vel[0] += x
                
    def update(self):
        """ update doodle in draw handler, all physics done here """
        self.pos[0] = (self.pos[0] + self.vel[0]) % w
        
        # compute platforms oldy and newy before and after current step, respectively
        oldy = min(height(self.pos[1])//100, num_plat - 1)
        newy = min(height(self.pos[1]+self.vel[1])//100,num_plat - 1)
        
        # bounce if you cross platform height, are going down and hit the actual platform
        if oldy != newy and self.vel[1] > 0 and pl[oldy].exists and pl[oldy].left < self.pos[0] < pl[oldy].right:
            sound.play()
            self.vel[1] = min(-self.vel[1],-doodle.rebound)
            if random.random()> .7: 	#make the platform disappear occasionally
                pl[oldy].exists = False
        else:
            self.pos[1] += self.vel[1]
            
        # accelerate due to gravity
        self.vel[1] += .1
        
        # if doodle get near top of frame, update offset[1] to move camera up
        clearance = 300
        if self.pos[1]-offset[1] < clearance:
            offset[1] = self.pos[1] - clearance
        
        # restart if fall below screen
        if self.pos[1]-offset[1] > h+50:
            offset[0],offset[1] = 0,0
            dd.pos[0],dd.pos[1] = w//2,h-200
            dd.vel[1] = 0
            for i in range(0,num_plat):
                pl[i].exists = True

class platform:
    
    def __init__(self):
        """ create a platform with left and right boundaries and existence flag """
        global w
        width = random.randrange(100,160)
        self.left = random.randrange(25,w-(25+width))
        self.right = self.left + width
        self.exists = True

# define callbacks for event handlers
        
def keydown(key):
    """ velocity model for left/right motion of doodle """
    if key == simplegui.KEY_MAP["left"]:
        dd.nudge(-2.5)
    elif key == simplegui.KEY_MAP["right"]:
        dd.nudge(2.5)
        
def keyup(key):
    """ velocity model for left/right motion of doodle """
    if key == simplegui.KEY_MAP["left"]:
        dd.nudge(2.5)
    elif key == simplegui.KEY_MAP["right"]:
        dd.nudge(-2.5)

   
def draw(canvas):
    """ update doodle position, draw doodle, draw platforms that are visible and their heights """
    dd.update()
    canvas.draw_circle(camera(dd.pos),5,2,"White")
    
    # enumerate all multiples of 100 in range of offset[1] to offset[1] + height
    for steps in range(100*int(offset[1]//100),int(h+offset[1]),100):
        
        # convert steps to index for platforms
        ind = height(steps)//100
        if ind < num_plat and pl[ind].exists:
            canvas.draw_line(camera([pl[ind].left,steps]),camera([pl[ind].right,steps]),4,"Yellow")
        canvas.draw_text(str(height(steps)),camera([w-50,steps]),12,"White")
        # canvas.draw_line(camera([0,steps]),camera([w,steps]),1,"White")
        
# initialize stuff
w = 800
h = 600
frame = simplegui.create_frame("Doodle Jump", w, h)
sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/jump.ogg") #hamster republic

# set handlers
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_draw_handler(draw)

# create 1000 random platforms
num_plat = 1000
pl = [platform() for i in range(0,num_plat)]

# make first platform cover the whole bottom of the window so you don't die immediately
pl[0].left = 0
pl[0].right = w

# global offset store current camera information
offset = [0,0]

# create the doodle jumper
dd = doodle(camera([w//2,h-200]))


# get things rolling
frame.start()
