import pygame
pygame.init()
from random import *
import numpy as np
#fonction move depend on the direction you want 
def move(pos,direction,action):
    vel = 10
    old_pos=pos[0]
    old_direction=direction
    if action==0:direction="left"
    if action==1:direction="right"
    if action==2:direction="up"
    if action==3:direction="down"
    
    if (old_direction=="left" and direction=="right") or (old_direction=="right" and direction=="left") or (old_direction=="up" and direction=="down") or (old_direction=="down" and direction=="up") :
         direction=old_direction      
    x=pos[-1][0]
    y=pos[-1][1]
    if direction=="right":x+=vel
    if direction=="left":x-=vel
    if direction=="up":y-=vel
    if direction=="down":y+=vel
    
    if x==(win_width)+10:
        x=0
    if x==-10:
        x=win_width
    if y==(win_height+10):
        y=0
    if y==-10:
        y=win_height
    del pos[0]
    pos.append([x,y])
    
    return pos, direction,old_pos

#fonction draw draw the game on th window
def draw(pos,win_height):
    for pos_square in range(len(pos)-1):
        pygame.draw.rect(win, (255,0,0), (pos[pos_square][0], pos[pos_square][1], width, height)) 
    pygame.draw.rect(win, (0,0,255), (pos[-1][0], pos[-1][1], width, height)) 
    pygame.draw.rect(win, (0,255,0), (pos_food[0], pos_food[1], width, height))
    win.fill((200,200,200),(win_height,0,win_height+220,win_height))

    
    text1=font_score.render("score:"+ str(score),1,(0,0,0))
    win.blit(text1,(win_width,0))
    text2=font_score.render("gen:"+ str(gen),1,(0,0,0))
    win.blit(text2,(win_width,30))
    text3=font_score.render("learning rate:"+ str(learning_rate),1,(0,0,0))
    win.blit(text3,(win_width,60))
    text4=font_score.render("discount:"+ str(discount),1,(0,0,0))
    win.blit(text4,(win_width,90))
    text5=font_score.render("random decision:"+ str(abs(epsilon)),1,(0,0,0))
    win.blit(text5,(win_width,120))
    text6=font_score.render("best score:"+ str(best_score)+"at gen"+str(best_gen),1,(0,0,0))
    win.blit(text6,(win_width,150))


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
def eat(pos,old_pos,pos_food,score,reward):
    ate=False
    if pos[-1]==pos_food:
        pos=add(pos,old_pos)
        pos_food=creat_food(pos)
        score+=1
        reward=reward_plus
        ate=True
    return pos,pos_food, score,reward,ate

#check if you lose 
def test_lose(pos,lose,reward,loop):
    lose=False
    test_pos=pos[0:-3]
    for position in test_pos:
        if position==pos[-1]:
            lose = True
            reward=reward_minus
            loop=0
            print(pos[-1])
            print(state)
            

    return lose,reward,loop



#reset the parameters 
def reset():
    head=[round(random()*(win_width-11)/10)*10,round(random()*(win_width-11)/10)*10]
    pos=[head,[head[0]+10,head[1]],[head[0]+20,head[1]],[head[0]+30,head[1]],[head[0]+40,head[1]]]
    direction="down"
    score=0
    lose=False
    return pos, direction ,lose, score
 
# 0:up,1:up left,2:left,3:down left,4:down,5:down right,6:right,7:up right
        
def get_state(pos,pos_food,direction):
    dir_food_x=pos[-1][0]-pos_food[0]
    dir_food_y=pos[-1][1]-pos_food[1]
    if dir_food_x==0 and dir_food_y>0:
        dir_food=0
    if dir_food_x>0 and dir_food_y>0:
        dir_food=1
    if dir_food_x>0 and dir_food_y==0:
        dir_food=2
    if dir_food_x>0 and dir_food_y<0:
        dir_food=3
    if dir_food_x==0 and dir_food_y<0:
        dir_food=4
    if dir_food_x<0 and dir_food_y<0:
        dir_food=5
    if dir_food_x<0 and dir_food_y==0:
        dir_food=6
    if dir_food_x<0 and dir_food_y>0:
        dir_food=7
       
    #if there is an obstacle obs=1
    test_pos=pos
    obs_up,obs_left,obs_down,obs_right=0,0,0,0
    pos_up,pos_down,pos_right,pos_left = get_pos_around(pos[-1])
    
    if pos_up in pos:
        obs_up=1
    if pos_down in pos:
        obs_down=1
    if pos_right in pos:
        obs_right=1
    if pos_left in pos:
        obs_left=1
        
    if direction=="left":direc=0
    if direction=="right":direc=1
    if direction=="up":direc=2
    if direction=="down":direc=3
    
    return direc ,obs_up,obs_left,obs_down,obs_right,dir_food    

def get_pos_around(head):
    x=head[0]
    y=head[1]
    
    if y==0:
        y_up=win_width
    else:
        y_up=y-10
    pos_up=[x,y_up]
    
    if y==win_width:
        y_down=0
    else:
        y_down=y+10
    pos_down=[x,y_down]
    
    if x==win_width:
        x_right=0
    else:
        x_right=x+10
    pos_right=[x_right,y]
    
    if x==0:
        x_left=win_width
    else:
        x_left=x-10
    pos_left=[x_left,y]
    
    
    return pos_up,pos_down,pos_right,pos_left
        
def get_action(epsilon,state,q_table):
    if random()<epsilon:
            action=int(np.floor(random()*4))
    else:
        action = np.argmax(q_table[state])
    return action

def play(pos,direction,action,pos_food,reward,lose,loop,score):
    
    pos, direction, old_pos=move(pos,direction,action)
    pos, pos_food,score, reward, ate=eat(pos,old_pos,pos_food,score,reward)
    lose,reward,loop=test_lose(pos,lose,reward,loop) 
    
    return pos,direction,old_pos,pos_food,score,reward,lose,loop,ate

def improve_q_table(q_table,new_state,state,action,reward,learning_rate,dicount):
    max_future_q = np.max(q_table[new_state])
    current_q=q_table[state + (action, )]
    new_q=(1- learning_rate) * current_q +learning_rate * (reward + discount* max_future_q)
    q_table[state + (action, )]=new_q 
    return q_table 

def reduce_epsilon(epsilon,epsilon_decay,ate):
    if ate and epsilon>0:
            epsilon-=epsilon_decay
    if epsilon<0:
            epsilon=0
    return epsilon
#set parameters
    
def check_ate(ate,count,lose,loop,epsilon):
    if ate:
        count=0     
    elif count>500:
        loop+=1
        lose=True
        count=0  
    if loop==5:
        epsilon=0.1
    return loop,lose,count,epsilon
              

win_height=400
win_width=400
win = pygame.display.set_mode((win_width+220,win_height))
pos, direction ,lose, score=reset()
pygame.display.set_caption("snake with dir")
width = 9
height = 9
pos_food=creat_food(pos)
run = True
font_score=pygame.font.SysFont('comicsans',30)

q_table= np.random.uniform(low=-1, high=1,size=(4,2,2,2,2,8,4))
state=get_state(pos,pos_food,direction)
learning_rate=0.077
discount=0.96
epsilon=0.1
epsilon_decay=0.001
reward_plus=0.97
reward_minus=-4.4
reward=0
count=0
action=0
gen=0
best_score=0
best_gen=0
loop=0
score=0

while run:
    reward=0
    count+=1
    keys = pygame.key.get_pressed()
    win.fill((80,80,80))   
    
    #check if close window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False 
    
    if not lose:
        action=get_action(epsilon,state,q_table)
        
        pos,direction,old_pos,pos_food,score,reward,lose,loop,ate=play(pos,direction,action,pos_food,reward,lose,loop,score)
        
        draw(pos,win_height)
       
        epsilon=reduce_epsilon(epsilon,epsilon_decay,ate)
               
        loop,lose,count,epsilon=check_ate(ate,count,lose,loop,epsilon)

        new_state=get_state(pos,pos_food,direction)
        
        q_table=improve_q_table(q_table,new_state,state,action,reward,learning_rate,discount)
                
        state=new_state
              
    if lose:
        
        if score>best_score:
            best_score=score
            best_gen=gen
            
        
        gen+=1
        pos, direction ,lose,score=reset()
        pos_food=creat_food(pos)

        
            
    pygame.display.update() 

pygame.quit()