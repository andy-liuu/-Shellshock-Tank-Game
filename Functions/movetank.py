from pygame import *
from math import *
from copy import *
from random import *
init()
#tank is [x,y,ang,direc,frame counter,switch counter]
#missile is [x,y,and,vx,vy,type]

def movetank(tank,ground):
    X = 0
    Y = 1
    ang = 2
    direc = 3
    count = 4
    swit = 5
    keys = key.get_pressed()


    #find y position
    
    ypos = 0
    for k in range(600):
        if ground.get_at((round(tank[X]),k)) == (0,0,255,255):
            ypos = (k-1)

            break

    tank[Y] = ypos

    
    #find angle
    if tank[direc] == "right":
        findh = 0

        for q in range(600):
            if ground.get_at((round(tank[X])+15,q)) == (0,0,255,255):
                findh = (q-1)
                break

                
        

        angle = -1*atan2((findh-tank[Y]),15)
        tank[ang] = angle
        diff = -1*(findh-ypos)
      
        
    elif tank[direc] == "left":
        findh = 0

        for q in range(600):
            if ground.get_at((round(tank[X])-15,q)) == (0,0,255,255):
                findh = (q-1)
                break


        angle = -1*atan2((findh-tank[Y]),15)
        tank[ang] = angle
        diff = -1*(findh-ypos)
    
     
       
    


    

    

    #find x position and find directions
    w,h = ground.get_size()
    switches = ["rswitch","lswitch"]
    if tank[direc] not in switches:
        
        #move left
        if keys[K_a] and tank[X] > 50:
            if tank[direc] == "right":
                tank[direc] = "rswitch"
            else:
                if diff < 30:
                    tank[X] -= cos(angle)
                    

        #move right
        elif keys[K_d] and tank[X] < w-50:
            if tank[direc] == "left":
                tank[direc] = "lswitch"
            else:
                if diff < 30:
                    tank[X] += cos(angle)
                    
              
    #fall down slopes fast
    if 50<tank[X]<w-50:
        if tank[ang] < -pi/3:
            if tank[direc] == "left":
                tank[X] -= 1
            elif tank[direc] == "right":
                tank[X] += 1

    #cases based on which direction tank is going, frame counter
    if tank[direc] == "lswitch" or tank[direc] == "rswitch":
        tank[count] = 0
        tank[swit] += 1

        if tank[swit] >= 24 and tank[direc] == "rswitch":
            tank[direc] = "left"
            tank[swit] = 0
        if tank[swit] >= 24 and tank[direc] == "lswitch":
            tank[direc] = "right"
            tank[swit] = 0
    elif tank[direc] == "left" or tank[direc] == "right":
        if keys[K_d] or keys[K_a]:
            tank[count] += 1


    
    

def drawtank(tank,limgset,movelist,screen):
    X = 0
    Y = 1
    ang = 2
    direc = 3
    count = 4
    swit = 5
    

    drawang = degrees(tank[ang])

    #every 5 frames change pictures
    if tank[direc] == "left" or tank[direc] == "right":
        fnum = tank[count]//5 % 4
        chosen = movelist[fnum]

    elif tank[direc] == "lswitch" or tank[direc] == "rswitch":
        fnum = tank[swit]//5
        chosen = limgset[fnum]



    picy = chosen.get_height()
    
    chosen = transform.rotate(chosen,drawang)
    rx,ry = chosen.get_size()
    if tank[direc] == "left" or tank[direc] == "lswitch":
        chosen = transform.flip(chosen,True,False)
    screen.blit(chosen,(tank[X]-(rx//2),tank[Y]-(ry)//2-picy//2))

    
    


def startmissile(tank,x,y,power,typ):
    X = 0
    Y = 1

    #calculate angle
    ange = atan2(-1*(y-tank[Y]),x-tank[X])
    

    #calculate power
    sx,sy = 10*power*cos(ange)/100,10*power*sin(ange)*-1/100
    return [tank[X],tank[Y]-20,ange,sx,sy,typ,0]
    

#miss = [x,y,ang,vx,vy,typ,count]
def movemissile(miss,ground,):
    X = 0
    Y = 1
    ang = 2
    vx = 3
    vy = 4
    typ = 5
    count = 6

    w,h = ground.get_size()
    miss[vy] += gravity
    angle = -1*atan2(miss[vy],miss[vx])
    miss[ang] = angle
    miss[X] += miss[vx]
    miss[Y] += miss[vy]
    miss[count] += 1

    
    if (not 0<=miss[X]<=w) or (not miss[Y]<=h):     
        miss[X] = 0
        miss[Y] = 0
        miss[ang] = 0
        miss[vx] = 0
        miss[vy] = 0
        miss[typ] = 0
        miss[count] = 0

    try:
        if (ground.get_at((round(miss[X]),round(miss[Y]))) != (0,0,0,255)):
            hitlist.append((miss[X],miss[Y],miss[typ]))
            miss[X] = 0
            miss[Y] = 0
            miss[ang] = 0
            miss[vx] = 0
            miss[vy] = 0
            miss[typ] = 0
            miss[count] = 0
    except:
        pass

    

def drawmissile(miss,basicset,superset,surf):
    X = 0
    Y = 1
    ang = 2
    vx = 3
    vy = 4
    typ = 5
    count = 6
    if miss[typ] == 0:
        img = superset[(miss[count]//20 )% 2]
    else:
        img = basicset[(miss[count]//20) % 2]
    if miss != [0,0,0,0,0,0]:
        realang = degrees(miss[ang])
        imgw,imgh = img.get_size()


        img = transform.rotate(img,realang)
        surf.blit(img,(miss[X]-imgw//2,miss[Y]-imgh//2))
def randomground(ground):
    points = []
    w,h = ground.get_size()
    
    points.append((0,h-200))
    for i in range(100,w,100):
        pbx,pby = points[-1]
        newy = pby + randint(-50,50)
        if newy >= h-100:
            newy = h-100
        elif newy < 250:
            newy = 250
        points.append((i,newy))
        points.append((i+50,newy))
    points += [(w,newy),(w,h),(0,h)]
    return points
    
def correctground(ground):
    w,h = ground.get_size()
    draw.rect(ground,(0,0,255),(0,h-15,w,15))
    
def destroy(hx,hy,ground):
    draw.circle(ground,(0,0,0,255),(hx,hy),7)
    draw.polygon(ground,(0,0,0,255),((hx-10,0),(hx+10,0),(hx+7,hy),(hx-7,hy)))
    
def create(hx,hy,ground):
    w,h = ground.get_size()
    ypos = 0
    for k in range(h):
        if ground.get_at((hx,k)) == (0,0,255,255):
            ypos = (k-1)

            break
    draw.circle(ground,(0,0,255),(hx,ypos),7)
    draw.polygon(ground,(0,0,255),((hx-10,h),(hx+10,h),(hx+7,ypos),(hx-7,ypos)))

#load every single picture
#======================================================

#moving tank sprites
movelist = []
move1 = image.load("moving tank/movetank1.png")
move2 = image.load("moving tank/movetank2.png")
move3 = image.load("moving tank/movetank3.png")
move4 = image.load("moving tank/movetank4.png")
movelist += [move1,move2,move3,move4]


#turning tank sprites
rightturn = []
leftturn = []
turn1 = image.load("turning tank/turntank1.png")
turn2 = image.load("turning tank/turntank2.png")
turn3 = image.load("turning tank/turntank3.png")
turn4 = transform.flip(turn2,True,False)
turn5 = transform.flip(turn1,True,False)
leftturn += [turn1,turn2,turn3,turn4,turn5]

#exploding tank sprites
explodetank = []
explode1 = image.load("exploding tank/explode1.png")
explode2 = image.load("exploding tank/explode2.png")
explode3 = image.load("exploding tank/explode3.png")
explode4 = image.load("exploding tank/explode4.png")
explode5 = image.load("exploding tank/explode5.png")
explode6 = image.load("exploding tank/explode6.png")
explode7 = image.load("exploding tank/explode7.png")
explode8 = image.load("exploding tank/explode8.png")
explode9 = image.load("exploding tank/explode9.png")
explode10 = image.load("exploding tank/explode10.png")
explode11 = image.load("exploding tank/explode11.png")
explodetank += [explode1,explode2,explode3,explode4,explode5,
                explode6,explode7,explode8,explode9,explode10,
                explode11]

#missile sprites
basicmissile = []
supermissile = []
basic1 = image.load("missile sprites/basic1.png")
basic2 = image.load("missile sprites/basic2.png")
super1 = image.load("missile sprites/super1.png")
super2 = image.load("missile sprites/super2.png")
basicmissile += [transform.flip(basic1,True,False),transform.flip(basic2,True,False)]
supermissile += [transform.flip(super1,True,False),transform.flip(super2,True,False)]

#======================================================================
#constants
gravity = 0.1


#make screens        
screen = display.set_mode((800,600))
offscreen = screen.copy()

#offscreen ground
offscreen.fill((0,0,0,255))
draw.polygon(offscreen,(0,0,255),randomground(offscreen))



tank = [350,0,12,"right",0,0]
missilelist = []
hitlist = []
running =True
while running:
    click = False
    right = False
    left = False
    for evt in event.get():
        
        if evt.type == QUIT:
            running = False
        if evt.type == MOUSEBUTTONDOWN:
            click = True
            if evt.button == 1:
                left = True
            elif evt.button == 3:
                right = True
    correctground(offscreen)
    screen.blit(offscreen,(0,0))
    mx,my = mouse.get_pos()
    mb = mouse.get_pressed()
    power = 100

    #start missile
    if click:
        #create is 0, destroy is 1
        if right:
            missiletype = 0
        elif left:
            missiletype = 1
        missil = startmissile(tank,mx,my,power,missiletype)
        missilelist.append(missil)
    #move missile
    for _ in range(len(missilelist)):
        m = missilelist.pop(0)
        if m != [0,0,0,0,0,0,0]:
            movemissile(m,offscreen)
            drawmissile(m,basicmissile,supermissile,screen)
            missilelist.append(m)

    for j in range(len(hitlist)):
        hitx,hity,whichone = [int(h) for h in hitlist.pop(0)]
        if whichone == 1:    
            destroy(hitx,hity,offscreen)
        elif whichone == 0:
            create(hitx,hity,offscreen)
    time.wait(10)
    movetank(tank,offscreen)
    drawtank(tank,leftturn,movelist,screen)
    display.flip()
    
    

quit()
