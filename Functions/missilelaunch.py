from math import *
from pygame import *
#global variables gravity and contact
def missilelaunch(ang,power,px,py):
    ang = radians(ang)
    vx,vy = 7*power*cos(ang),7*power*sin(ang)*-1

    while True:
        vy += grav
        px += vx
        py += vy
        screen.fill(0)
        draw.rect(screen,(255,0,0),(px,py,20,20))
        time.wait(10)
        display.flip()

        #later agg contact to the stage
        if px > 800 or py > 600:
            break
screen = display.set_mode((800,600))
grav = 0.05

running =True
while running:
    for evt in event.get():
        if evt.type == QUIT:
            running = False
    missilelaunch(80,1,50,400)
    screen.fill(0)
    

quit()
