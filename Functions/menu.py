#game with menu
from pygame import *

def title():

    screen = display.set_mode((1200,600))
    
    titleimg = image.load("menu screens/title.png")
    
    playbut = Rect(436,158,327,65)
    instructbut = Rect(436,257,327,65)
    creditbut = Rect(436,347,327,65)

    buttonlist = [playbut,instructbut,creditbut]
    returnlist = ["game","instruct","credit"]
    
    running =True
    while running:
        click = False
        for evt in event.get():
            if evt.type == QUIT:
                running = False
            if evt.type == MOUSEBUTTONDOWN:
                click = True

        #mouse pos
        mx,my = mouse.get_pos()
        #reset screen
        screen.blit(titleimg,(0,0))

        #case work for different buttons
        for but in buttonlist:
            if but.collidepoint(mx,my):
                draw.rect(screen,(255,0,0),but,10)

                if click:
                    ind = buttonlist.index(but)
                    return returnlist[ind]
        display.flip()

def instruct():
    screen = display.set_mode((1200,600))
    
    instimg = image.load("menu screens/instruct.png")
   
    screen.blit(instimg,(0,0))
    display.flip()

    
    running =True
    while running:
        for evt in event.get():
            if evt.type == QUIT:
                running = False
    return "title"
        
def credit():
    screen = display.set_mode((1200,600))
    
    credimg = image.load("menu screens/credit.png")
   
    screen.blit(credimg,(0,0))
    display.flip()

    
    running =True
    while running:
        for evt in event.get():
            if evt.type == QUIT:
                running = False
    return "title"
        
