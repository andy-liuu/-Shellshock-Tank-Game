#drawtank function
from pygame import *
from math import *

X = 0
Y = 1
ang = 2
direc = 3
count = 0


def switchcount(tank):
    
#change switch counter if needed
    if tank[direc] == "rswitch" or tank[direc] == "lswitch":
        tank[count] += 1

    #frames per pic
    fppic = 5
    if count == fppic*5:
        tank[count] = 0
        if tank[direc] == "rswitch":
            tank[direc] = "left"
        if tank[direc] == "lswitch":
            tank[direc] = "right"
    
