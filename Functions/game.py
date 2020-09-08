#main.py
"""Tanks, by Andy Liu (31500782)
Features:
- Menu with other screens
    -click sound with changing pages
    -highlight buttons on title page
- Game
    -Terrain
        - Changable ground
        - Random ground generator at start of each round
    - Tanks
        - Can drive on any terrain
        - intentional restrictions on movement
        - intentional forced movement when sliding down too steep a hill
        - driving angle calculated and shown in sprite
        - fuel counter
        - Explosion animation when dead
    - Missile
        -angle calculated and shown
        -sound effect when launched and hit
        - can destroy ground or build ground
    - game over screen
        -click to reset everything and play again
        - auto-reset when music ends
- Music
    -menu music persists between credit/instruction/title screen
    -game music for gameplay
    -new music when you gameover
"""
from math import *
from pygame import *
from copy import *
from random import *
import os

init()

#main game function is this, other game functions are defined inside
def game():


    """
    FUNCTION DEFINING
    """

    """TANK STUFF"""

    #tank format is [x,y,and,direction,count,switch count]
    def startmovement(tank,ground):#only for starting the game, update y pos and ang
        X = 0
        Y = 1
        ang = 2
        direc = 3
        count = 4
        swit = 5
        
        #find y position at top of blue ground    
        ypos = 0
        for k in range(600):
            if ground.get_at((round(tank[X]),k)) == (0,0,255,255):
                ypos = (k-1)
                break
        tank[Y] = ypos

        #find angle based on which direction the tank is facing
        if tank[direc] == "right":
            findh = 0
            for q in range(600):#look 15px in front of tank to find angle (smooth enough on bumps)
                if ground.get_at((round(tank[X])+15,q)) == (0,0,255,255):
                    findh = (q-1)
                    break
            angle = -1*atan2((findh-tank[Y]),15)
            tank[ang] = angle     
        elif tank[direc] == "left":
            findh = 0
            for q in range(600):
                if ground.get_at((round(tank[X])-15,q)) == (0,0,255,255):
                    findh = (q-1)
                    break
            angle = -1*atan2((findh-tank[Y]),15)
            tank[ang] = angle

    def movetank(tank,ground):
        X = 0
        Y = 1
        ang = 2
        direc = 3
        count = 4
        swit = 5
        keys = key.get_pressed()
        #find y position, see startmovement()    
        ypos = 0
        for k in range(600):
            if ground.get_at((round(tank[X]),k)) == (0,0,255,255):
                ypos = (k-1)
                break
        tank[Y] = ypos
        
        #find angle, see startmovement()
        if tank[direc] == "right":
            findh = 0
            for q in range(600):
                if ground.get_at((round(tank[X])+15,q)) == (0,0,255,255):
                    findh = (q-1)
                    break
            angle = -1*atan2((findh-tank[Y]),15)
            tank[ang] = angle
            diff = -1*(findh-ypos)  #later used to see if the slope is too high to drive    
        elif tank[direc] == "left":
            findh = 0
            for q in range(600):
                if ground.get_at((round(tank[X])-15,q)) == (0,0,255,255):
                    findh = (q-1)
                    break
            angle = -1*atan2((findh-tank[Y]),15)
            tank[ang] = angle
            diff = -1*(findh-ypos)

            
        #change x position and find directions
        w,h = ground.get_size()
        switches = ["rswitch","lswitch"]

        if tank[direc] not in switches:        
            #move left
            if keys[K_a] and tank[X] > 50:#boundary, do not go offscreen

                if tank[direc] == "right": #r --> l makes an rswitch
                    tank[direc] = "rswitch"
                else:
                    if diff < 30:
                        tank[X] -= cos(angle)#for consistent speed across any angle
            #move right
            elif keys[K_d] and tank[X] < w-50:

                if tank[direc] == "left":#l-->r makes a lswitch
                    tank[direc] = "lswitch"
                else:
                    if diff < 30:
                        tank[X] += cos(angle)

        #fall down slopes fast  
        if 50<tank[X]<w-50:#respect boundary
            if tank[ang] < -pi/3:#threshhold
                if tank[direc] == "left":
                    tank[X] -= 1
                elif tank[direc] == "right":
                    tank[X] += 1

        #cases based on which direction tank is going, frame counter for future animations
        if tank[direc] == "lswitch" or tank[direc] == "rswitch":
            tank[swit] += 1
            tank[count] += 1

            if tank[swit] >= 24 and tank[direc] == "rswitch":
                tank[direc] = "left"
                tank[swit] = 0
            if tank[swit] >= 24 and tank[direc] == "lswitch":
                tank[direc] = "right"
                tank[swit] = 0
        elif tank[direc] == "left" or tank[direc] == "right":
            if keys[K_d] or keys[K_a]:
                tank[count] += 1#count always goes up to keep track of fuel




    """MISSILE STUFF"""
    #miss = [x,y,ang,vx,vy,typ,count]

    #initial start on the click
    def startmissile(tank,x,y,power,typ):
        X = 0
        Y = 1
        #sound effect
        mixer.Sound.play(launchsound)
        #calculate angle
        ange = atan2(-1*(y-(tank[Y]-20)),x-tank[X])
        

        #calculate power
        sx,sy = 10*power*cos(ange)/100,10*power*sin(ange)*-1/100
        return [tank[X],tank[Y]-20,ange,sx,sy,typ,0]

    #movement in parabolas
    """GLOBAL VARIABLE HITLIST"""
    """GLOBAL VARIABLE GRAVITY"""
    def movemissile(miss,ground,):
        X = 0
        Y = 1
        ang = 2
        vx = 3
        vy = 4
        typ = 5
        count = 6

        #basic movement
        w,h = ground.get_size()
        miss[vy] += gravity
        angle = -1*atan2(miss[vy],miss[vx])#angle for sprite
        miss[ang] = angle
        miss[X] += miss[vx]#xy vectors
        miss[Y] += miss[vy]
        miss[count] += 1

        #cases to reset(later despawn) the missile
        if (not -25<=miss[X]<=w+25) or (not miss[Y]<=h+25):   #out of x bounds (plus a little leeway in case it comes back  
            miss[X] = 0
            miss[Y] = 0
            miss[ang] = 0
            miss[vx] = 0
            miss[vy] = 0
            miss[typ] = 0
            miss[count] = 0

        try:#at high speeds sometimes crashes but it will be good on the next frame
            if (ground.get_at((round(miss[X]),round(miss[Y]))) == (0,0,255)):#hit the ground
                hitlist.append((miss[X],miss[Y],miss[typ]))#record where the hit was
                miss[X] = 0
                miss[Y] = 0
                miss[ang] = 0
                miss[vx] = 0
                miss[vy] = 0
                miss[typ] = 0
                miss[count] = 0
        except:
            pass



    #sprites and rotation
    #--------------------------------------------------------------

    #removes the tank sprite, puts the background
    def collumnfix(tank,screen,tempground):
        X = 0
        Y = 1
        ang = 2
        direc = 3
        count = 4
        swit = 5
        
        #changte screen
        w,h = tempground.get_size()
        try:#in case something happens, but due to the boundaries it never does (here for comfort)
            #use entire collumn in case the tank falls down a slope fast
            cover = tempground.subsurface((tank[X]-49,0,98,h))
            screen.blit(cover,(tank[X]-49,0))

        except:#in case the tank goes somewhere it;s not supposed too(:. crash) just reset everything
            screen.blit(tempground,(0,0))

    #re-blit the tank sprite      
    def fixit(tank,movelist,limgset,surf):#movelist and limgset are the lists of images
        X = 0
        Y = 1
        ang = 2
        direc = 3
        count = 4
        swit = 5
        
        
        drawang = degrees(tank[ang])

        """first tank"""
        #every 5 frames change pictures
        if tank[direc] == "left" or tank[direc] == "right":
            fnum = tank[count]//5 % 4
            chosen = movelist[fnum]
        elif tank[direc] == "lswitch" or tank[direc] == "rswitch":
            fnum = tank[swit]//5
            chosen = limgset[fnum]

        #rotate and adjust, also bring pic up by oicy//2 to "drive on ground"    
        picy = chosen.get_height()   
        chosen = transform.rotate(chosen,drawang)
        rx,ry = chosen.get_size()
        if tank[direc] == "left" or tank[direc] == "lswitch":
            chosen = transform.flip(chosen,True,False)
        surf.blit(chosen,(tank[X]-(rx//2),tank[Y]-(ry)//2-picy//2))

    #remoe old missile sprite, place new missile sprite
    def drawmissile(miss,tank,tank2,basicset,superset,movelist,limgset,surf,tempground):
        X = 0
        Y = 1
        ang = 2
        vx = 3
        vy = 4
        typ = 5
        count = 6


        
        #cover old missile (max 50x50 box to reduce lag)
        try:#sometimes missiles do wierd things at high  speeds
            #casework for different areas of the screen to not go overboard
            if 25<=miss[X]<=1175 and 25<=miss[Y]<=600:
                cover = tempground.subsurface((miss[X]-25,miss[Y]-25,50,50))
                surf.blit(cover,(miss[X]-25,miss[Y]-25))
            elif miss[X]<=25 and miss[Y]<=25:
                cover = tempground.subsurface((0,0,50,50))
                surf.blit(cover,(0,0))
            elif 25<=miss[X]<=1175 and miss[Y]<=25:
                cover = tempground.subsurface((miss[X]-25,0,50,50))
                surf.blit(cover,(miss[X]-25,0))
            elif miss[X]<=25 and 25<=miss[Y]<=600:
                cover = tempground.subsurface((0,miss[Y]-25,50,50))
                surf.blit(cover,(0,miss[Y]-25))
            elif miss[X]>1175 and miss[Y]<=25:
                cover = tempground.subsurface((1150,0,50,50))
                surf.blit(cover,(1150,0))
            elif miss[X]>1175 and 25<=miss[Y]<=600:
                cover = tempground.subsurface((1150,miss[Y]-25,50,50))
                surf.blit(cover,(1150,miss[Y]-25))
            else:
                surf.blit(tempground,(0,0))
        except:#reset everything in case
            surf.blit(tempground,(0,0))
            

        
        #draw new missile
        if miss[typ] == 0:
            img = superset[(miss[count]//20 )% 2]
        else:
            img = basicset[(miss[count]//20) % 2]
        if miss != [0,0,0,0,0,0]:
            #rotation
            realang = degrees(miss[ang])
            imgw,imgh = img.get_size()
            img = transform.rotate(img,realang)
            surf.blit(img,(miss[X]-imgw//2,miss[Y]-imgh//2))




    """GROUND MANIP"""

    # randomish list of points for the draw.poly... at the beginning
    def randomground(ground):
        points = []
        w,h = ground.get_size()
        
        points.append((0,h-200))
        for i in range(100,w,100):#spaced out changes at 100px
            pbx,pby = points[-1]
            newy = pby + randint(-50,50)#restrict how slopy the slopes can get
            if newy >= h-100:
                newy = h-100
            elif newy < 250:
                newy = 250
            points.append((i,newy))
            points.append((i+50,newy))
        points += [(w,newy),(w,h),(0,h)]
        return points

    #iin case missiles want to dig too low or build too high
    def correctground(ground):
        w,h = ground.get_size()
        draw.rect(ground,(0,0,255),(0,h-50,w,50))#replace ground too low
        draw.rect(ground,(0,0,0),(0,0,w,50))#remove ground too high in black


    #missile affects ground
    def destroy(hx,hy,ground):#black will be colorkeyed to be transparent 
        #elipse crater plus a poly beam going up (gets rid of incaves)
        #deep and narrow to encourage building
        mixer.Sound.play(explosound)
        #do stuff
        draw.circle(ground,(0,0,0),(hx,hy),12)
        draw.polygon(ground,(0,0,0),((hx-17,0),(hx+17,0),(hx+12,hy),(hx-12,hy)))

    def create(hx,hy,ground):
        mixer.Sound.play(explosound)
        w,h = ground.get_size()
        ypos = 0
        #adjust the hit location to the top of the blueground in case the y vector is too big
        for k in range(h):
            if ground.get_at((hx,k)) == (0,0,255,255):
                ypos = (k-1) - 10 #bigger hill for balancing

                break
        #blue hill plus beam going down to make no caves
        draw.circle(ground,(0,0,255),(hx,ypos),12)
        draw.polygon(ground,(0,0,255),((hx-17,h),(hx+17,h),(hx+12,ypos),(hx-12,ypos)))
    

    """Overlay screens"""
    #these screens are done last as an overlay
    """global variable whoseturn,infofont"""
    def updateinfo(tank,misscount,infoscreen,surf):

        #reset
        infoscreen.fill((100,132,183))

        #missile words
        misswords = infofont.render("Missiles Left: %d" %(5-misscount),True,(255,255,255))
        mfx,mfy = infofont.size("Missiles Left: %d" %(5-misscount))
        infoscreen.blit(misswords,(infoscreen.get_width()-mfx,0))

        #fuel words
        fuelwords = infofont.render("Fuel Left: %d" %(150-tank[4]),True,(255,255,255))
        infoscreen.blit(fuelwords,(0,0))

        #player showcaser
        if whoseturn:
            playwords= "P1"
        else:
            playwords = "P2"
        
        playx,playy = infofont.size(playwords)
        infoscreen.blit(infofont.render(playwords,True,(255,255,255)),(infoscreen.get_width()//2 - (playx//2),0))
        surf.blit(infoscreen,(300,551))

    def transition(infoscreen,whoseturn,surf):#between turns
        
        #reset
        infoscreen.fill((100,132,183))

        if whoseturn:#player 1
            transwords = transitionfont.render("Player 2's Turn",True,(255,255,255))
            tx,ty = transitionfont.size("Player 2's Turn")
        else:#not player 1 :. player 2
            transwords = transitionfont.render("Player 1's Turn",True,(255,255,255))
            tx,ty = transitionfont.size("Player 1's Turn")
        infoscreen.blit(transwords,(infoscreen.get_width()//2 - (tx//2),0))
        surf.blit(infoscreen,(300,551))

    """global variable vstext"""
    def healthbar(health1,health2,surf):
        #player 1
        draw.rect(surf,(122,138,163),(350,25,200,25)) 
        draw.rect(surf,(249,67,114),(350,25,health1,25))

        #player 2
        draw.rect(surf,(122,138,163),(650,25,200,25)) 
        draw.rect(surf,(249,67,114),(850-health2,25,health2,25))

        screen.blit(vstext,(600-vstextx//2,37-vstexty//2))

        
        
    """
    SPRITES
    """
    #all sprites originally point right
    #===========================================================================
    #moving tank sprites
    movelist = []
    move1 = image.load("moving tank/movetank1.png")
    move2 = image.load("moving tank/movetank2.png")
    move3 = image.load("moving tank/movetank3.png")
    move4 = image.load("moving tank/movetank4.png")
    movelist += [move1,move2,move3,move4]


    #turning tank sprites
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
    basicmissile += [transform.flip(basic1,True,False),transform.flip(basic2,True,False)]#so rotate works easier
    supermissile += [transform.flip(super1,True,False),transform.flip(super2,True,False)]

    #imaged game layers
    groundimg = image.load("layer/ground.png")#doesn't get changed, used to "reset" tempground
    tempground = groundimg.copy()#gets changed
    tempground.set_colorkey((0,0,0)) #for the "black sky" on another surface
    skyimg = image.load("layer/sky_back.png")
    #=================================================================================



    """
    PRE-GAME CONSTANTS
    """
    #=====================================================
    """MUSIC FIRST"""
    mixer.music.load("music/gamesong.wav")
    mixer.music.play(-1)

    """SOUND EFFECTS WE NEED"""
    #didn't include moving because there is a slight delay between call and sound which makes a moving tank sound really bad
    explosound = mixer.Sound("sound/explo.wav")
    deadsound = mixer.Sound("sound/dead.wav")
    launchsound = mixer.Sound("sound/launch.wav")
    clicksound = mixer.Sound("sound/click.wav")

    """FONT INITING"""
    infofont = font.SysFont("arial",40)
    transitionfont = font.SysFont("arial",50)
    resetfont = font.SysFont("arial",120)


    #words I always need
    vstext = infofont.render("VS",False,(255,255,255))
    vstextx,vstexty = infofont.size("VS")

    resettext = resetfont.render("Click to Reset",True,(249,67,114))
    resetx,resety =resetfont.size("Click to Reset")

    
    #make screen
    screen = display.set_mode((1200,600))

    #game layers
    blueground = Surface((1200,600))
    blueground.fill((0,0,0))
    blueground.set_colorkey((0,0,255))#for the "blue ground" to become the tempground img
    draw.polygon(blueground,(0,0,255),randomground(blueground))

    infoscreen = Surface((600,49))

    #math constants
    gravity = 0.1

    #lists
    missilelist = []
    hitlist = []

    #starting tanks always start on the same x poses, y pos is updated based oon randomground
    player1 = [350,0,0,"right",0,0]
    player2 = [850,0,0,"left",0,0]
    startmovement(player1,blueground)
    startmovement(player2,blueground)

    #starting health
    health1 = 200
    health2 = 200


    #counters
    misscount = 0#number of missies shot
    gameovercount = 0#frames for the gameover screen
    running =True
    change = True#everytime a missile hits the ground(also to start)
    whoseturn = True#true = player1
    gameover = False#true = someone died
    firstgameoverloop = False#records the first loop you die for music purposes
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
                    
        #alternate escape option         
        if key.get_pressed()[27]:
            running = False


        #first check if the person is dead before doing the rest of the game
        if gameover:
            
            """new music"""
            if firstgameoverloop:#only do this once when you first die
                mixer.music.stop()#no more old
                mixer.music.load("music/realgameover.wav")
                mixer.music.play(0)
                mixer.Sound.play(deadsound)

            firstgameoverloop = False#after this point it is not the first death loop

            
            #finish the missile paths but they no longer destroy the ground, also no more sounds to hear the explosion sound + new music
            for _ in range(len(missilelist)):
                m = missilelist.pop(0)
                if m != [0,0,0,0,0,0,0]:
                    movemissile(m,blueground)
                    drawmissile(m,tank,player2,basicmissile,supermissile,movelist,leftturn,screen,noobjects)
                    missilelist.append(m)


            #ANIMATION OF TANK EXPLODING
            #casework finds loser
            if p1win:
                loser = player2 #variables point to same list so it still changes both like I want
                thegreatwinner = player1
            else:
                loser = player1
                thegreatwinner = player2
                
            #get rid of idle losing tank
            collumnfix(loser,screen,noobjects)

            #in case the winning tank gets clipped by collumnfix
            fixit(thegreatwinner,movelist,leftturn,screen)

            """EXPLODE Animation"""
  
    ##        X = 0
    ##        Y = 1
    ##        ang = 2
    ##        direc = 3
    ##        count = 4
    ##        swit = 5
            
            
            explodeang = degrees(loser[2])
            chosenexplode = explodetank[gameovercount//15]#15 loops per frame
            
            #similar to collumnfix but the frame spacing and list of items is different
            explodey = chosenexplode.get_height()   
            chosenexplode = transform.rotate(chosenexplode,explodeang)
            rexplodex,rexplodey = chosenexplode.get_size()
            if loser[3] == "left" or loser[3] == "lswitch":
                chosenexplode = transform.flip(chosenexplode,True,False)
            screen.blit(chosenexplode,(loser[0]-(rexplodex//2),loser[1]-(rexplodey)//2-explodey//2))

            gameovercount += 1#next frame
            gameovercount = min(gameovercount,164)#do not exeed 15*11-1 frames so list stays in bound (11 sprites to explode)

            #WORDS TO PUT IN PLACE OF INFOSCREEN
            infoscreen.fill((100,132,183))

            #for %s text
            if p1win:
                winner = "Player 1"
            else:
                winner = "Player 2"
            
            winwords = infofont.render("%s Wins!" %(winner),True,(randint(1,255),randint(1,255),randint(1,255)))#seizure colors
            winx,winy = infofont.size("%s Wins!" %(winner))
            infoscreen.blit(winwords,((infoscreen.get_width()-winx)//2,0))#centers text

            screen.blit(infoscreen,(300,551))


            #FIX HEALTHBAR INCASE COLLUMNFIX DESTROYS IT
            healthbar(health1,health2,screen)

            #click to reset text
            screen.blit(resettext,((screen.get_width()-resetx)//2,(screen.get_height()-resety)//2))

            
            display.flip()

            #CLICK TO RESET or autoreset when the music finishes
            if click or not mixer.music.get_busy():
                #reset blueground
                blueground.fill((0,0,0))
                draw.polygon(blueground,(0,0,255),randomground(blueground))
                
                #reset lists
                missilelist = []
                hitlist = []

                #tanks positions reset
                player1 = [350,0,0,"right",0,0]
                player2 = [850,0,0,"left",0,0]
                startmovement(player1,blueground)
                startmovement(player2,blueground)

                #starting health
                health1 = 200
                health2 = 200


                #reset other counter variables
                misscount = 0
                gameovercount = 0
                running =True
                change = True
                whoseturn = True
                gameover = False
                firstgameoverloop = True

                #reset music
                mixer.music.load("music/gamesong.wav")
                mixer.music.play(-1)
    


            



        else:#no loser yet
        
            #code that adjusts the ground into current state
            if change:#when ground is hit or beginning of game
                    
                #sky
                screen.blit(skyimg,(0,0))

                #ground with a bit of colorkey magic
                tempground.blit(groundimg,(0,0))#reset tempground into the blank image
                correctground(blueground)#in case of missile digging/building too high/low
                tempground.blit(blueground,(0,0))#colorkey is blue so tempground is now black sky + imaged ground
                screen.blit(tempground,(0,0))#colorkey is black so screen is now imaged sky+imaged ground
                noobjects = screen.copy()#good time to get the screen without any overlay/sprites for future sprite purposes

            #basics
            mx,my = mouse.get_pos()
            mb = mouse.get_pressed()
            power = 100


            #remove the old tank sprite positions
            collumnfix(player1,screen,noobjects)
            collumnfix(player2,screen,noobjects)






            #start sequencing, tank variable points to player1/player2 lists

            if whoseturn:
                tank = player1#vars point to same list :. change the actual player1 list like I want
                hurt = Rect((player2[0]-25,max(player2[1]-25,0),50,50)) #hurtbox rect not to go offscreen up top(stopped by collumnfix at bottom)
            else:
                tank = player2
                hurt = Rect((player1[0]-25,max(player1[1]-25,0),50,50))


            #move tank 
            if tank[4] < 150 :#fuel counted by tank[count]
                movetank(tank,blueground)

            #start missile 
            if click and misscount<5:
                #create is 0, destroy is 1
                misscount += 1
                if right:
                    missiletype = 0
                elif left:
                    missiletype = 1
                missil = startmissile(tank,mx,my,power,missiletype)
                missilelist.append(missil)

                
            #move missile also draw it in same loop
            for _ in range(len(missilelist)):
                m = missilelist.pop(0)
                if m != [0,0,0,0,0,0,0]:#only do stuff (include append back) if not reset by
                    drawmissile(m,tank,player2,basicmissile,supermissile,movelist,leftturn,screen,noobjects)#draw first to never draw a (0,0) missile accidently
                    movemissile(m,blueground)

                    #casework if hit the enemy, cannot hit self
                    if hurt.collidepoint(m[0],m[1]):
                        mixer.Sound.play(explosound)
                        if whoseturn:
                            health2 -= 10
                            health2 = max(health2,0)#no negative health
                            
                        else:
                            health1 -= 10
                            health1 = max(health1,0)

                        

                    else:
                        missilelist.append(m)

            
            #missiles hitting the ground
            change = False #all the gound manip gets done if the ground changes
            for j in range(len(hitlist)):
                hitx,hity,whichone = [int(h) for h in hitlist.pop(0)]
                if whichone == 1:    
                    destroy(hitx,hity,blueground)
                    change = True
                elif whichone == 0:
                    create(hitx,hity,blueground)
                    change = True




            #put the new tank positions in place
            fixit(player1,movelist,leftturn,screen)
            fixit(player2,movelist,leftturn,screen)

            #UPDATE INFOSCREENs
            updateinfo(tank,misscount,infoscreen,screen)
            
            #MAKE AND UPDATE HEALTH BAR
            healthbar(health1,health2,screen)            

            display.flip()
            time.wait(5)#not too fast

            
            #check if dead
            if not gameover:
                if health1 == 0:
                    gameover = True
                    firstgameoverloop = True
                    p1win = False
                elif health2 == 0:
                    gameover = True
                    firstgameoverloop = True
                    p1win = True



            
            #check if need to change turn
            if misscount>4 and  len(missilelist) == 0 and len(hitlist) == 0 and health1 != 0 and health2 != 0 :
                
                #if a missile hits the tank right before the cahnge turn you need to remove that image
                collumnfix(player1,screen,noobjects)
                collumnfix(player2,screen,noobjects)
                fixit(player1,movelist,leftturn,screen)
                fixit(player2,movelist,leftturn,screen)

                #MAKE AND UPDATE HEALTH BAR In case the collumnfix overlaps the health bar
                healthbar(health1,health2,screen)
                
                #next turn
                whoseturn = not whoseturn

                #reset tank values
                misscount = 0
                player1[4] = 0
                player2[4] = 0

                #new player animation
                transition(infoscreen,not whoseturn,screen)
                display.flip()

                #unconventional way of having to get a click for
                #the next turn without having that click make
                #a new missile while getting the next player
                nextturn = True
                while nextturn:
                    for evt in event.get():
                        if evt.type == MOUSEBUTTONDOWN:
                            nextturn = False
                            break
                        if evt.type == QUIT:
                            running = False
                            nextturn = False
                            break
                        
    mixer.music.stop()#let the menu song play later
    mixer.Sound.play(clicksound)
    return "title"#if quit()


"""OTHER SCREENS"""

def title():

    screen = display.set_mode((1200,600))

    #the entire screen is a pic
    titleimg = image.load("menu screens/title.png")
    
    playbut = Rect(434,159,329,65)
    instructbut = Rect(435,256,327,66)
    creditbut = Rect(435,346,327,65)

    buttonlist = [playbut,instructbut,creditbut]
    returnlist = ["game","instruct","credit"]

    #click button sound
    clicksound = mixer.Sound("sound/click.wav")
    
    running =True
    while running:
        click = False
        for evt in event.get():
            if evt.type == QUIT:
                running = False
            if evt.type == MOUSEBUTTONDOWN:
                click = True
        #alternate escape option         
        if key.get_pressed()[27]:
            running = False
            
        #mouse pos
        mx,my = mouse.get_pos()
        #reset screen
        screen.blit(titleimg,(0,0))

        #case work for different buttons
        color = (255,0,0)
        for but in buttonlist:
            if but.collidepoint(mx,my):
                size = 15
                startingx,startingy,wid,hei = but
                
                #taken straight from my paint project with a little modification
                #draw a rect with no weird corners
                evensize = size+size%2
                draw.rect(screen,color,but,evensize)
                draw.rect(screen,color,(startingx-(evensize)//2+1,startingy-(evensize)//2+1,evensize,evensize))     #next 4 lines fill in the corners of the rectangle
                draw.rect(screen,color,(startingx-(evensize)//2+1,(startingy+hei)-(evensize)//2,evensize,evensize))              #the various +1's eliminate pygame inconsistencies
                draw.rect(screen,color,((startingx+wid)-(evensize)//2,startingy-(evensize)//2+1,evensize,evensize))              #(found by trial)
                draw.rect(screen,color,((startingx+wid)-(evensize)//2,(startingy+hei)-(evensize)//2,evensize,evensize))

                #return another screen if you click ona button
                if click:
                    mixer.Sound.play(clicksound)
                    ind = buttonlist.index(but)
                    return returnlist[ind]
        display.flip()
    mixer.Sound.play(clicksound)
    return "exit"
def instruct():
    #just blit the image once and wait for them to click out
    screen = display.set_mode((1200,600))   
    instimg = image.load("menu screens/instruct.png")
    screen.blit(instimg,(0,0))
    display.flip()

    #sund effect
    clicksound = mixer.Sound("sound/click.wav")
    
    running =True
    while running:
        for evt in event.get():
            if evt.type == QUIT:
                running = False
        #alternate escape option         
        if key.get_pressed()[27]:
            running = False
    #when click the x button
    mixer.Sound.play(clicksound)
    return "title"
        
def credit():

    
    screen = display.set_mode((1200,600))
    credimg = image.load("menu screens/credit.png")
    screen.blit(credimg,(0,0))
    display.flip()
    running =True

    clicksound = mixer.Sound("sound/click.wav")
    while running:
        for evt in event.get():
            if evt.type == QUIT:
                running = False
        #alternate escape option         
        if key.get_pressed()[27]:
            running = False

    #sound effect when changing screens
    mixer.Sound.play(clicksound)
    return "title"

#load every song
mixer.music.load("music/menusong.wav")

#the actual program just goes through pages, also here I controll the menu song
page = "title"
while page != "exit":

    #menu song if not already playing (at opening program OR after quitting game page)
    if not mixer.music.get_busy():
        mixer.music.load("music/menusong.wav")
        mixer.music.play(-1)
    
    if page == "title":
        page = title()
    if page == "game":
        mixer.music.stop()#stop menu music
        #other game music in the game func
        page = game()    
    if page == "instruct":
        page = instruct()       
    if page == "credit":
        page = credit()    
    
quit()
