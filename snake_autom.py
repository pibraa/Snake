import pygame
pygame.init()
from random import *
#fonction move depend on the direction you want 
def move(pos,direction):
    vel = 10
    old_pos=pos[0]
    direction=automatic_player(pos,pos_food,direction)

        
    x=pos[-1][0]
    y=pos[-1][1]
    if direction=="right":x+=vel
    if direction=="left":x-=vel
    if direction=="up":y-=vel
    if direction=="down":y+=vel
    
    if x==(win_width):
        x=0
    if x==-10:
        x=win_width
    if y==(win_height):
        y=0
    if y==-10:
        y=win_height
    del pos[0]
    pos.append([x,y])
    
    return pos, direction,old_pos

#fonction draw draw the game on th window
def draw(pos):
    for pos_square in range(len(pos)-3):
        pygame.draw.rect(win, (255,0,0), (pos[pos_square][0], pos[pos_square][1], width, height)) 
    pygame.draw.rect(win, (0,0,255), (pos[-1][0], pos[-1][1], width, height)) 
    pygame.draw.rect(win, (255,0,255), (pos[-2][0], pos[-2][1], width, height)) 
    pygame.draw.rect(win, (255,0,255), (pos[-3][0], pos[-3][1], width, height)) 

    pygame.draw.rect(win, (0,255,0), (pos_food[0], pos_food[1], width, height))

    text=font_score.render("score:"+ str(score),1,(255,255,0))
    win.blit(text,(0,0))

#fonction add, add the last pose to the tail of the snake
def add(pos,old_pos):
    pos.insert(0,old_pos)
    return pos
#creat position randomly on the map for the food 
def creat_food(pos):
    x_food=round(random()*(win_width-11)/10)*10
    y_food=round(random()*(win_height-11)/10)*10
    while [x_food,y_food] in pos :
        x_food=round(random()*(win_width-11)/10)*10
        y_food=round(random()*(win_height-11)/10)*10
    return [x_food,y_food]    

#if the head of the snake is on the pos of the food the snake grow
def eat(pos,ols_pos,pos_food,score):
    if pos[-1]==pos_food:
        pos=add(pos,old_pos)
        pos_food=creat_food(pos)
        score+=1
    return pos,pos_food, score

#check if you lose 
def test_lose(pos,lose):
    lose=False
    test_pos=pos[0:-1]
    for position in test_pos:
        if position==pos[-1]:
            lose = True
    return lose

#check if you want to continue
def continu_game(keys,continu):
    if keys[pygame.K_y]: continu="yes"
    if keys[pygame.K_n]: continu="no"
    
    return continu

#reset the parameters 
def reset():
    pos=[[50,50],[60,50],[70,50]]
    direction="down"
    return pos, direction 






 
def automatic_player(pos,pos_food,direction):
    vel=10
    will_die=False
    old_direction=direction 
    dist_x=(pos[-1][0]-pos_food[0])
    dist_y=(pos[-1][1]-pos_food[1])
    if abs(dist_x)>=abs(dist_y):
        if dist_x>0:  direction="left"
        else: direction="right"
    else:
        if dist_y>0: direction="up"
        else:direction="down"
           
    if (old_direction=="left" and direction=="right") or (old_direction=="right" and direction=="left") or (old_direction=="up" and direction=="down") or (old_direction=="down" and direction=="up") :
         direction=old_direction    
    
    x=pos[-1][0]
    y=pos[-1][1]
    if direction=="right":x+=vel
    if direction=="left":x-=vel
    if direction=="up":y-=vel
    if direction=="down":y+=vel
    next_pos=[x,y]
    
    for square in pos:
        if square==next_pos:
            will_die=True
    count=0
    while will_die and count<10 :
        x=pos[-1][0]
        y=pos[-1][1]
        if count%4==0 and old_direction!="left":direction="right"
        if count%4==1 and old_direction!="right":direction="left"
        if count%4==2 and old_direction!="up":direction="down"
        if count%4==3 and old_direction!="down":direction="up"

        if direction=="right":x+=vel
        if direction=="left":x-=vel
        if direction=="up":y-=vel
        if direction=="down":y+=vel
        next_pos=[x,y]
        
        if next_pos in pos:
            will_die=True
        else:
            will_die=False
        count+=1
    
         
         
    return direction








#set parameters
score=0
win_height=400
win_width=400
win = pygame.display.set_mode((win_width,win_height))
pygame.display.set_caption("snake")
direction="down"
width = 9
height = 9
pos=[[50,50],[60,50],[70,50],[100,200]]
pos_food=creat_food(pos)
run = True
lose=False
font_score=pygame.font.SysFont('comicsans',30)
continu=""

while run:
    keys = pygame.key.get_pressed()
    pygame.time.delay(10)
    win.fill((80,80,80))   
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False        
    lose=test_lose(pos,lose)    
    if not lose:
        pos, direction, old_pos,=move(pos,direction)
        pos, pos_food,score=eat(pos,old_pos,pos_food,score)
        draw(pos)
        
    elif lose:
        continu=continu_game(keys,continu)
        draw(pos)

        if continu=="yes":
            pos,direction=reset()
            lose=False
            continu=""
            score=0
        if continu=="no":
            run=False
            
    pygame.display.update() 

pygame.quit()