#drawtank function
from pygame import *
from math import *

X = 0
Y = 1
ang = 2
direc = 3
count = 4
swit = 5

#tank is [x,y,ang,direc,frame counter,switch counter]
def drawtank(tank):
    #frame counter
    keys = key.get_pressed()
    if keys[K_LEFT] or keys[K_RIGHT]:
        tank[count] += 1

    
    #change the switch counter
    if tank[direc] == "lswitch" or tank[direc] == "rswitch":
        tank[count] = 0
        tank[swit] += 1

        if tank[swit] > 25 and tank[direc] == "rswitch":
            tank[direc] = "left"
        if tank[swit] > 25 and tank[direc] == "lswitch":
            tank[direc] = "right"
    else:
        tank[swit] = 0

    
