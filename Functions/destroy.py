#destroyground function
def destroy(hx,hy,ground):
    draw.circle(ground,(0,0,0,255),(hx,hy),5)
    draw.polygon(ground,(0,0,0,255),((hx-5,0),(hx+5,0),(hx+5,hy),(hx-5,hy)))
    

