#move missile function, does not draw missile
#also a startmissile function
from math import *
from pygame import *
placeholder = Surface((10,10))
placeholder.fill((255,0,0))
X = 0
Y = 1
ang = 2
vx = 3
vy = 4
def startmissile(ange,power,px,py):
    ange = radians(ange)
    sx,sy = 7*power*cos(ange),7*power*sin(ange)*-1
    return [px,py,ange,sx,sy]
    

#miss = [x,y,ang,vx,vy]
missile = [0,0,0,0,0]
gravity = 0.05
def movemissile(miss):
    miss[vy] += gravity
    angle = atan2(miss[vx],miss[vy])
    miss[ang] = angle
    miss[X] += miss[vx]
    miss[Y] += miss[vy]
    #when you get the ground
    #then put an if statement
    #here to make the missile
    #[0,0,0,0,0]

def drawmissile(miss,img):
    if missile != [0,0,0,0,0]:
        realang = degrees(miss[ang])
        img = transform.rotate(img,realang)
        screen.blit(img,(miss[X],miss[Y]))
        time.wait(10)

screen = display.set_mode((800,600))
grav = 0.05
missilelist = []
running =True
tank = [
while running:
    for evt in event.get():
        click = False
        if evt.type == QUIT:
            running = False
        if evt.type == MOUSEBUTTONDOWN:
            click = True
    screen.fill(0)
    mx,my = mouse.get_pos()
    if click:
        tempang = atan2(

    
    display.flip()
quit()
