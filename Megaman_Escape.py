"""
    Turtle Graphics - Game Programming
'''

'''    
    Readme:
    1. If there's any problem related to the font, pelase
       check the best result of display as attached as the file: "Display_with_font.PNG"
"""

import turtle
import time
import random
import pygame
import sys


"""
    Constants and variables
"""

sys.setrecursionlimit(10000)

"""Music System"""
pygame.init()
pygame.mixer.init(buffer=16)
death_sound = pygame.mixer.Sound('Death_sound.wav')
laser_sound = pygame.mixer.Sound('laser.wav')
BGM_f = pygame.mixer.Sound('Chiptune.wav')
BGM_s = pygame.mixer.Sound('Chiptune_Dubstep_1.wav')
BGM_boss = pygame.mixer.Sound('Boss.wav')
BGM_start = pygame.mixer.Sound('start_screen.wav')
timer_sound = pygame.mixer.Sound('Timer.wav')
switch_sound = pygame.mixer.Sound('switch.wav')
switch_sound.set_volume(4)
kill_sound = pygame.mixer.Sound('boom.wav')
kill_sound.set_volume(0.4)
turtle.title('Megaman Escape - Universe Edition')
""" Music System"""

window_height = 600
window_width = 820

update_interval = 25

initial_river_width = 300
river_width = initial_river_width
bandwidth = 130                 #The minimum bandwidth of the river

border_height = 650

river_width_update = 0.3

safe_distance_from_border = border_height / 2 + 9
safe_distance_from_crocodile = 33

max_no = 36                     #My Student ID no: 20110916
default_value = 4               #Default value

crocodile_number = max_no
req_croc = default_value
croc_speed = default_value

crocodiles = []
crocodile_speeds = []
crocodile_width = 100
crocodile_height = 40
crocodile_speed_min, croc_speed_max = 1, max_no

menu_pos = {'y' : window_height//6, 'x' : window_width//7}
menu_color = 'Red'              #Menu Color

survival_time = -3
run_cnt = 0
dead = False
score = 0
Z = 100                          #Score per unit croc

counter_run_liao = False

'''Ranking'''
rank = []
return_button = turtle.Turtle()
return_button.hideturtle()


'''Laser'''
laser_speed = 70
laser_impact_dis = 35
laser_kill_pt = 90             #Score per laser kill
laser_set = []
blast_kill_pt = 30             #Score per blast kill

laser_cost = 150                  # Cost per laser
blast_cost = 1000                 # Cost per blast

"""
    Barebone functions of the whole program
"""
'''Time_Value Turtle + Score Turtle'''
turtle.tracer(False)
time_value = turtle.Turtle()
time_value.hideturtle()
time_value.up()

score_value = turtle.Turtle()
score_value.hideturtle()
score_value.up()
score_value.goto((window_width//2 - window_width//4), (window_height//2 - window_height//10))
score_value.color('white')
'''Time_Value Turtle (END)'''

''' Additional shapes here'''
turtle.addshape('Death.gif')
''' Additional shapes here'''

'''Permanent message'''
per_mess = turtle.Turtle()
per_mess.hideturtle()
per_mess.up()

for i in range(8):
    turtle.addshape('megaman_' + str(i) + '.gif')
turtle_frame = 0
def megaman_ani_game():
    global turtle_frame
    if not(dead) and start_clicked:
        turtle.shape('megaman_' + str(turtle_frame % 8) + '.gif')
        turtle_frame += 1
        turtle.update()
        turtle.ontimer(megaman_ani_game, 50)


for i in range(26):
    turtle.addshape('showup_' + str(i) + '.gif')
show_frame = 0
def megaman_showup():
    global show_frame
    if show_frame in range(25):
        turtle.shape('showup_' + str(show_frame % 25) + '.gif')
        show_frame += 1
        turtle.update()
        turtle.ontimer(megaman_showup, 50)


def display_per_mess():
    per_mess.clear()
    per_mess.goto(-window_width/2 + 10, -window_height/2 + 29)
    per_mess.color('black')
    per_mess.write('--> Press \" s \": Kill all aliens @$' + str(blast_cost)\
    + ' (Remaining: ' + str(score//blast_cost) + ') ', font=('Euphemia', 12))
    per_mess.goto(-window_width/2 + 9, -window_height/2 + 30)
    per_mess.color('cyan')
    per_mess.write('--> Press \" s \": Kill all aliens @$' + str(blast_cost)\
    + ' (Remaining: ' + str(score//blast_cost) + ') ', font=('Euphemia', 12))

    per_mess.goto(-window_width/2 + 10, -window_height/2 + 69)
    per_mess.color('black')
    per_mess.write('--> Press \" m \": Return to menu ', font=('Euphemia', 12))
    per_mess.goto(-window_width/2 + 9, -window_height/2 + 70)
    per_mess.color('cyan')
    per_mess.write('--> Press \" m \": Return to menu ', font=('Euphemia', 12))
    
    per_mess.goto(-window_width/2 + 10, -window_height/2 + 49)
    per_mess.color('black')
    per_mess.write('--> Press \" a \": Shoot laser  @$' + str(laser_cost)\
    + ' (Remaining: ' + str(score//laser_cost) + ') ', font=('Euphemia', 12))
    per_mess.goto(-window_width/2 + 9, -window_height/2 + 50)
    per_mess.color('cyan')
    per_mess.write('--> Press \" a \": Shoot laser  @$' + str(laser_cost)\
    + ' (Remaining: ' + str(score//laser_cost) + ') ', font=('Euphemia', 12))
'''Permanent message'''

stop_timer = False
def time_record():
    if not dead and not(stop_timer):
        time_value.clear()
        survival_time += 1
        if survival_time > 0:
            time_value.goto((-window_width//2 + window_width//10 + 1), (window_height//2 - window_height//10 - 1))
            turtle.colormode(255)
            time_value.color(10, 10, 10)
            time_value.write('Time: '+ str(survival_time), font=("Agency FB", 15, 'bold'))
            
            time_value.goto((-window_width//2 + window_width//10), (window_height//2 - window_height//10))
            time_value.color(240, 240, 240)
            time_value.write('Time: '+ str(survival_time), font=("Agency FB", 15, 'bold'))
            global survival_time
        turtle.ontimer(time_record, 1000)
        return

start_clicked = False

blast = turtle.Turtle()
blast.up()
blast.hideturtle()
blast_frame = 0
blast_speed = 30
for i in range(4):
    turtle.addshape('blast_' + str(i) + '.gif')
def blast_ani():
    if blast_frame == 0:
        blast.goto(turtle.xcor(), turtle.ycor())
    if blast.xcor() < (window_width/2 + 50):
        blast.showturtle()
        if blast_frame < 4:
            blast.shape('blast_' + str(blast_frame) + '.gif')
            blast_frame += 1
        elif blast_frame == 4:
            blast_frame = 1
        blast.forward(blast_speed)
        global blast_frame
    else:
        blast.hideturtle()
    turtle.ontimer(blast_ani, 50)

def kill_all():
    global score
    if (blast_cost <= score) and start_clicked and not(dead):
        blast_ani()
        blast_frame = 0
        global blast_frame
        
        kill_sound.play()
        display_per_mess()
        for mv_croc_no in range(req_croc):
            if (crocodiles[mv_croc_no].xcor() < window_width/2):
                score += blast_kill_pt
        
        for i in range(req_croc):   #Reset the positions of all crocodiles
            x = (window_width + crocodile_width) / 2 + (crocodile_width/3)
            y = random.uniform(-(river_width-crocodile_height)/2, (river_width-crocodile_height)/2)
            crocodiles[i].goto(x, y)

        score -= blast_cost

''' Restart Button'''
def restart_game():  

    if not(dead) and start_clicked:
        FinalStat('')                       # Display the final score and the time survived
        time.sleep(2)
    score = 0
    global score
    
    BGM_start.fadeout(500)
    death_sound.fadeout(1000)
    BGM_f.fadeout(1000)
    BGM_s.fadeout(1000)
    BGM_boss.fadeout(1000)
    BGM_start.play(-1)
    
    show_frame = 0                      #Reset the frames of animation
    global show_frame
    turtle_frame = 0
    global turtle_frame
    death_frame = 0
    global death_frame
    blast_frame = 0
    global blast_frame
    blast.hideturtle()
    
    turtle.bgpic("start_up_screen.gif")
    
    start_clicked = False
    global start_clicked
    
    counter_run_liao = False
    global counter_run_liao
    counter_sec = 3
    global counter_sec
    
    display_per_mess()
    
    megaman_showup()                    #Megaman Shows up again
    turtle.goto(0, 0)                   #Reset the position of turtle
    turtle.ondrag(None)
    
    
    score_value.clear()
    time_value.clear() 
    gmover_msg.clear()                  #Remove gameover message
    time_value.clear()                  #Reset time of survival
    stop_timer = True
    global stop_timer
    
    survival_time = -3
    global survival_time               
    
    river_width = initial_river_width   #Reset River width
    global river_width
    
    for i in range(crocodile_number):   #Reset the positions of all crocodiles    
        x = (window_width + crocodile_width) / 2 + (crocodile_width/3)
        y = random.uniform(-(river_width-crocodile_height)/2, (river_width-crocodile_height)/2)
        crocodiles[i].goto(x, y)
       
    upper_border.sety((border_height + river_width) / 2)            #Reset the position of borders
    lower_border.sety(-(border_height + river_width) / 2)    

    start_button.showturtle()           #Show buttons
    left_arrow.showturtle()
    right_arrow.showturtle()
    left_arrow_no.showturtle()
    right_arrow_no.showturtle()
    
    
    #return_button.clear()
    #return_button.hideturtle()
    rank_button.clear()
    rank_button.showturtle()
    rank_button.goto(rank_button_x, rank_button_y)
    rank_button.color("black")
    rank_button.begin_fill()
    for _ in range(2):
        rank_button.forward(80)
        rank_button.left(90)
        rank_button.forward(25)
        rank_button.left(90)
    rank_button.end_fill()
    rank_button.color("white")
    rank_button.goto(rank_button_x + 40, rank_button_y + 5)
    rank_button.write("RANKING", font=("Arial", 10, "bold"), align="center")
    rank_button.goto(rank_button_x + 40, rank_button_y + 13)
    rank_button.color("")
    rank_button.shape("square")
    
    label_turtle.clear()
    label_turtle.goto(-window_width/2 + 31, -130)
    label_turtle.color('black')
    label_turtle.write('HELP! Megaman has to get back to his spaceship for weapons \
    \n Click and Drag to move Megaman \
    \n Try not to touch the aliens and the narrowing gate\
    \n or it will be Megaman\'s grave.', font=('Consolas', 13))

    label_turtle.goto(-window_width/2 + 30, -129)
    label_turtle.color('LIMEGREEN')
    label_turtle.write('HELP! Megaman has to get back to his spaceship for weapons \
    \n Click and Drag to move Megaman \
    \n Try not to touch the aliens and the narrowing gate\
    \n or it will be Megaman\'s grave.', font=('Consolas', 13))

    label_turtle.goto(menu_pos['x']-240, menu_pos['y']+12)
    label_turtle.color(menu_color)
    label_turtle.write("MAXIMUM SPEED OF ALIENS:", font=("Agency FB", 15, "bold"))

    label_turtle.goto(menu_pos['x']-240, menu_pos['y']-8)
    label_turtle.color(menu_color)
    label_turtle.write("NUMBER OF ALIENS:", font=("Agency FB", 15, "bold"))
    
    Stat_Display()                      #Show back the user_values
    
    """ Add the start button """        #Reset the start button
    button_width = 80
    start_button.goto((turtle.xcor()-(button_width//2) - 2), menu_pos['y']-45)
    start_button.color("blue")
    start_button.begin_fill()
    for _ in range(2):
        start_button.forward(button_width + 4)
        start_button.left(90)
        start_button.forward(29)
        start_button.left(90)
    start_button.end_fill()

    start_button.goto((turtle.xcor()-(button_width//2)), menu_pos['y']-43)
    start_button.color("black")
    start_button.begin_fill()
    for _ in range(2):
        start_button.forward(button_width)
        start_button.left(90)
        start_button.forward(25)
        start_button.left(90)
    start_button.end_fill()

    start_button.color("white")
    start_button.goto((turtle.xcor()-(button_width//2))+40, menu_pos['y']-39)
    start_button.write("START", font=("Trebuchet MS", 9, "bold"), align="center")
        ### The invisiblle Button, Woo ###
        
    start_button.goto((turtle.xcor()-(button_width//2))+40, menu_pos['y']-38)
    start_button.shape('square')
    start_button.shapesize(1.25, 4)
    start_button.color('')
    """ Button added """
    
    for i in range(crocodile_number):   #Reset the speed of all crocs to 0    
        crocodile_speeds[i] = 0
        global crocodile_speeds
        

    if laser_set:                       #In case of sudden restart game
        for i in range(len(laser_set)):
            laser_set[i].hideturtle()
            laser_set[i] = None
            del laser_set[i]
    laser_set = []
    global laser_set
    
    dead = False                        #Reset the state of death
    global dead
    
    turtle.update()
    
''' Restart Button'''
  
def FinalStat(message):
    gmover_msg.goto(1, -7)
    turtle.colormode(255)
    gmover_msg.color(10, 10, 10)
    gmover_msg.write(message + '\n  Total Score: $' + str(score) + \
    '\n  Total Time survived: ' + str(survival_time) + ' sec', align="center", font=("Aharoni", 18, "normal"))
    
    gmover_msg.goto(0, -6)
    gmover_msg.color(200, 0, 0)
    gmover_msg.write(message + '\n  Total Score: $' + str(score) + \
    '\n  Total Time survived: ' + str(survival_time) + ' sec', align="center", font=("Aharoni", 18, "normal"))
    
    score_value.clear()
    time_value.clear()    
    
    global rank
    if score > min(rank):
        rank.pop()
        rank.append(score)
        rank = sorted(rank, reverse=True)
        if score > max(rank):
            label_turtle.goto(0, -50)
            label_turtle.write("You broke a RECORD!" , align="center", font=("Impact", 24, "normal"))
                
        ranking_file = open('ranking.txt', 'w')
        for i in range(len(rank)):
            score_lin = str(rank[i]) + '\t' + '\n'
            ranking_file.write(score_lin)

        ranking_file.close()

  
def gameover(message):
    
    if laser_set:                       #Clear all turtles after death
        for i in range(len(laser_set)):
            laser_set[i].hideturtle()
            laser_set[i] = None
            del laser_set[i]
    laser_set = []
    global laser_set
    
    blast.hideturtle()                  #Clear the blast

    BGM_f.stop()
    BGM_s.stop()
    BGM_boss.stop()
    if dead:
        death_sound.play()
    
    turtle.shape('Death.gif')
    turtle.update()
    
    turtle.update()
    FinalStat(message)
    

def moveturtle(x, y):
    if x > -window_width / 2 and x < window_width / 2:
        if y > -window_width / 2 and y < window_width / 2:
            turtle.goto(x, y)

def movecroc():
    for i in range(req_croc):
        crocodiles[i].forward(crocodile_speeds[i])
        if crocodiles[i].xcor() < -(window_width+crocodile_width)/2:
            score += Z
            global score
            display_per_mess()
            x = (window_width + crocodile_width)/2
            y = random.uniform(-(river_width - crocodile_height)/2, \
            (river_width - crocodile_height)/2)
            crocodiles[i].goto(x, y)
            crocodile_speeds[i] = random.uniform(crocodile_speed_min, croc_speed)
            
        if turtle.distance(crocodiles[i]) < safe_distance_from_crocodile:
            dead = True
            global dead
            gameover("Oh! Megaman is dead T.T")
            return 1
                
def list_rank(null_x, null_y):
    
    turtle.onkeypress(restart_game, 'm')
    
    turtle.bgpic('start_up_screen_1.gif')
    user_value.clear()
    rank_button.clear()
    start_button.clear()
    start_button.hideturtle()
    label_turtle.clear()
    user_value.clear()
    left_arrow.hideturtle()
    right_arrow.hideturtle()
    left_arrow_no.hideturtle()
    right_arrow_no.hideturtle()
    turtle.update()


    label_turtle.goto(0, 190)
    label_turtle.color("Red")
    label_turtle.write("RANK BOARD", font=("Times", 25, "bold"), align="center")
    filename = 'ranking.txt'
    myfile = open(filename, 'r')
    scorer = 0
    del rank[0:len(rank)]
    for line in myfile:
        scorer = line.rstrip().split("\t")
        scorer[0] = int(scorer[0])
        rank.append(scorer[0])
    myfile.close()
    for i in range(1, len(rank)+1):
        label_turtle.goto(0, (170-(30*i)))
        label_turtle.write(str(i) + "\t\t\t" + str(rank[i - 1]), font=("Estrangelo Edessa", 15, "bold"), align="center")
    turtle.update()    
                
                
def moving_laser():
    for mv_laser in laser_set:
        if (mv_laser.xcor() < (window_width/2 - 10)):
            mv_laser.forward(laser_speed)   #If laser has not reached the right-most of screen, move it
            for i in range(req_croc):   #Search for moving crocodiles
                if (mv_laser.distance(crocodiles[i]) < laser_impact_dis):
                    score += laser_kill_pt
                    global score
                    
                    mv_laser.hideturtle()
                    laser_set.remove(mv_laser)  #Remove the used laser
                    global laser_set
                    mv_laser = None
                    del mv_laser   #Delete the turtle so that it won't stuck in the memory
                    
                    x = (window_width + crocodile_width)/2
                    y = random.uniform(-(river_width - crocodile_height)/2, \
                    (river_width - crocodile_height)/2)
                    crocodiles[i].goto(x, y)
                    crocodile_speeds[i] = random.uniform(crocodile_speed_min, croc_speed)
                    
                    break   #crocodile has been killed, stop searching
        elif (mv_laser.xcor() >= (window_width/2 - 10)):
            mv_laser.hideturtle()
            laser_set.remove(mv_laser)     #Remove the out-of-screen laser
            global laser_set
            mv_laser = None
            del mv_laser       #Delete the turtle so that it won't stuck in the memory

            
            
            
def updatescreen():
    """
        This function does:
            1. Decrease the width of the river
            2. Check if the player has won the game
            3. Check if the player has hit the borders
            4. Move the crocodiles
            5. Check if the player has collided with a crocodile
            6. Update the screen
            7. Schedule the next update
    """
    
    '''Update score
    if not(stop_timer):
        score_value.clear()
        score_value.write('Total Score: $' + str(score), font=("Agency FB", 15, 'bold'))
    Update score'''

    if counter_run_liao:   
    
        if not(stop_timer):
            score_value.clear()
            score_value.write('Total Score: $' + str(score), font=("Agency FB", 15, 'bold'))
        
        if (river_width >= bandwidth) and not(stop_timer):
            global river_width
            upper_border.sety(upper_border.ycor() - river_width_update)
            lower_border.sety(lower_border.ycor() + river_width_update)
            river_width -= 2 * river_width_update
            
        if (upper_border.ycor() - turtle.ycor() < safe_distance_from_border) or \
        turtle.ycor() - lower_border.ycor() < safe_distance_from_border:
            dead = True
            global dead
            gameover("AAUGH! Your megaman \n was killed by the saw")
            return
        if movecroc():
            return
    
    if not(dead) and laser_set:
        moving_laser()
    
    turtle.update() 
    turtle.ontimer(updatescreen, update_interval)

turtle.setup(window_width, window_height)
turtle.bgpic('start_up_screen.gif')
turtle.tracer(False)
turtle.setundobuffer(None)

turtle.addshape('Croc_0.gif')

""" Creating Crocodiles before border """
for i in range(crocodile_number):
    crocodile = turtle.Turtle()
    crocodile.left(180)
    crocodile.up()
    crocodile.shape('Croc_0.gif')
    x = (window_width + crocodile_width) / 2 + (crocodile_width/3)
    y = random.uniform(-(river_width-crocodile_height)/2, (river_width-crocodile_height)/2)
    crocodile.goto(x, y)
    crocodiles.append(crocodile)
    crocodile_speeds.append(random.uniform(crocodile_speed_min, croc_speed))
megaman_showup()
turtle.up()



""" Creating borders after crocodiles creation """
upper_border = turtle.Turtle()
upper_border.up()
lower_border = turtle.Turtle()
lower_border.up()
turtle.addshape("upper_border.gif")
turtle.addshape("lower_border.gif")
upper_border.shape("upper_border.gif")
lower_border.shape("lower_border.gif")
upper_border.sety((border_height + river_width) / 2)
lower_border.sety(-(border_height + river_width) / 2)
""" Creating borders """



"""
    Displaying some texts
"""
label_turtle = turtle.Turtle()
label_turtle.up()
label_turtle.hideturtle()

label_turtle.goto(-window_width/2 + 31, -130)
label_turtle.color('black')
label_turtle.write('HELP! Megaman has to get back to his spaceship for weapons \
\n Click and Drag to move Megaman \
\n Try not to touch the aliens and the narrowing gate\
\n or it will be Megaman\'s grave.', font=('Consolas', 13))

label_turtle.goto(-window_width/2 + 30, -129)
label_turtle.color('LimeGreen')
label_turtle.write('HELP! Megaman has to get back to his spaceship for weapons \
\n Click and Drag to move Megaman \
\n Try not to touch the aliens and the narrowing gate\
\n or it will be Megaman\'s grave.', font=('Consolas', 13))


label_turtle.goto(menu_pos['x']-240, menu_pos['y']+12) # Put the text next to the spinner control
label_turtle.color(menu_color)
label_turtle.write("MAXIMUM SPEED OF ALIENS:", font=("Agency FB", 15, "bold"))

label_turtle.goto(menu_pos['x']-240, menu_pos['y']-8) # Put the text next to the spinner control
label_turtle.color(menu_color)
label_turtle.write("NUMBER OF ALIENS:", font=("Agency FB", 15, "bold"))

""" Finish declaration """

""" Here comes the user_value """
user_value = turtle.Turtle()
user_value.hideturtle()
user_value.up()
user_value.color('white')

stat_mess_color = 'limegreen'
def Stat_Display():
    user_value.clear()
    user_value.color(menu_color)
    user_value.goto(menu_pos['x']+20, menu_pos['y']+11)
    user_value.write(str(croc_speed), font=("Agency FB", 15), align="center")
    user_value.goto(menu_pos['x']+20, menu_pos['y']-9)
    user_value.write(str(req_croc), font=("Agency FB", 15), align="center")
    
    if croc_speed <= 10:
        user_value.color(stat_mess_color)
        user_value.goto(70, menu_pos['y']-39)
        user_value.write('(Stage.1/3: Speed < 11)', font=('Agency FB', 15, 'bold'))
        user_value.color(menu_color)
    if (croc_speed > 10) and (req_croc < 21):
        user_value.color(stat_mess_color)
        user_value.goto(70, menu_pos['y']-60)
        user_value.write('(Stage.2/3: Speed > 10 \n No. of aliens < 21)', font=('Agency FB', 15, 'bold'))
        user_value.color(menu_color)
    if (croc_speed > 10) and (req_croc > 20):
        user_value.color(stat_mess_color)
        user_value.goto(70, menu_pos['y']-39)
        user_value.write('(Stage.BOSS: Get insane with this stage >.<)', font=('Agency FB', 15, 'bold'))
        user_value.color(menu_color)
Stat_Display()
"""That's it"""



""" Functions for Speed changing"""
def decrease_speed (null_x, null_y):
    global croc_speed
    if croc_speed > crocodile_speed_min + 1:
        croc_speed -= 1
        Stat_Display()
        
def increase_speed (null_x, null_y):
    global croc_speed
    if croc_speed + 1 <= croc_speed_max:
        croc_speed += 1
        Stat_Display()
""" That's all """

""" Add spinners (For max speed)"""
left_arrow = turtle.Turtle()
left_arrow.shape('arrow')
left_arrow.color(menu_color)
left_arrow.shapesize(0.75, 1.5)
left_arrow.left(180)
left_arrow.up()
left_arrow.goto(menu_pos['x'], menu_pos['y']+20)
left_arrow.onclick(decrease_speed)

right_arrow = turtle.Turtle()
right_arrow.shape('arrow')
right_arrow.color(menu_color)
right_arrow.shapesize(0.75, 1.5)
right_arrow.up()
right_arrow.goto(menu_pos['x']+40, menu_pos['y']+20)
right_arrow.onclick(increase_speed)
""" Added arrows """

""" Functions for Number of croc changing"""
def decrease_no (null_x, null_y):
    global req_croc
    if req_croc > 2:
        req_croc -= 1
        Stat_Display()
        movecroc()
        
def increase_no (null_x, null_y):
    global req_croc
    if req_croc + 1 <= max_no:
        req_croc += 1
        Stat_Display()
        movecroc()
""" That's all """

""" Add spinners (For number of crocs)"""
left_arrow_no = turtle.Turtle()
left_arrow_no.shape('arrow')
left_arrow_no.color(menu_color)
left_arrow_no.shapesize(0.75, 1.5)
left_arrow_no.left(180)
left_arrow_no.up()
left_arrow_no.goto(menu_pos['x'], menu_pos['y'])
left_arrow_no.onclick(decrease_no)

right_arrow_no = turtle.Turtle()
right_arrow_no.shape('arrow')
right_arrow_no.color(menu_color)
right_arrow_no.shapesize(0.75, 1.5)
right_arrow_no.up()
right_arrow_no.goto(menu_pos['x']+40, menu_pos['y'])
right_arrow_no.onclick(increase_no)
""" Added arrows """




counter_sec = 3
def counter_for_game():
    turtle.onkeypress(None, 'm')
    global first_time_played
    if first_time_played:
        timer_sound.play()
        first_time_played = False
        
    global counter_sec
    if start_clicked and (counter_sec >= 1):
        timer_cnt.clear()
        timer_cnt.write(str(counter_sec) , font=("Courier New", 40, "bold"), align="center")
        turtle.update()
        counter_sec -= 1
        turtle.update()
        turtle.ontimer(counter_for_game, 1000)
    else:
        timer_cnt.clear()
        counter_run_liao = True
        global counter_run_liao
        turtle.onkeypress(restart_game, 'm')
        
        if croc_speed <= 10:
            BGM_s.play(-1)
        if (croc_speed > 10) and (req_croc < 21):
            BGM_f.play(-1)
        if (croc_speed > 10) and (req_croc > 20):
            BGM_boss.play(-1)
        megaman_ani_game()
   
   
""" Function of startgame """

def startgame(null_x, null_y):

    BGM_start.fadeout(500)

    start_clicked = True
    global start_clicked
    
    turtle.bgpic("Background.gif")
    
    #null_x, null_y = 0, 0
    turtle.onkeypress(restart_game, 'm')
    turtle.onkeypress(kill_all, 's')
    
    switch_sound.play()
    dead = False
    global dead
    stop_timer = False
    global stop_timer
    
    turtle.ondrag(moveturtle)
    start_button.clear()
    start_button.hideturtle()
    label_turtle.clear()
    user_value.clear()
    left_arrow.hideturtle()
    right_arrow.hideturtle()
    left_arrow_no.hideturtle()
    right_arrow_no.hideturtle()
    
    rank_button.hideturtle()
    rank_button.clear()
    
    first_time_played = True
    global first_time_played
    counter_for_game()
    
    #megaman_ani_game()
    #turtle.update()
    
    time_record()
        
    display_per_mess()
    
    for i in range(crocodile_number):
        crocodile_speeds[i] = random.uniform(crocodile_speed_min, croc_speed)
    turtle.ontimer(updatescreen, update_interval)
    
    return
""" End of the function """

start_button = turtle.Turtle()
start_button.up()

timer_cnt = turtle.Turtle()
timer_cnt.up()
timer_cnt.hideturtle()
timer_cnt.color('white')
timer_cnt.goto(0, 180)

""" Add the start button """
button_width = 80
start_button.goto((turtle.xcor()-(button_width//2) - 2), menu_pos['y']-45)
start_button.color("blue")
start_button.begin_fill()
for _ in range(2):
    start_button.forward(button_width + 4)
    start_button.left(90)
    start_button.forward(29)
    start_button.left(90)
start_button.end_fill()

start_button.goto((turtle.xcor()-(button_width//2)), menu_pos['y']-43)
start_button.color("black")
start_button.begin_fill()
for _ in range(2):
    start_button.forward(button_width)
    start_button.left(90)
    start_button.forward(25)
    start_button.left(90)
start_button.end_fill()

start_button.color("white")
start_button.goto((turtle.xcor()-(button_width//2))+40, menu_pos['y']-39)
start_button.write("START", font=("Trebuchet MS", 9, "bold"), align="center")
    ### The invisiblle Button, Woo ###
    
start_button.goto((turtle.xcor()-(button_width//2))+40, menu_pos['y']-38)
start_button.shape('square')
start_button.shapesize(1.25, 4)
start_button.color('')
start_button.onclick(startgame)
""" Button added """

''' Read Rankings'''
rank = []
filename = 'ranking.txt'
myfile = open(filename, 'r')
scores = 0

for line in myfile:
    scores = line.rstrip().split("\t")
    scores[0] = int(scores[0])
    rank.append(scores[0])
    

myfile.close()
''' Read Rankings'''



BGM_start.play(-1)

''' Weapon Firing '''
#turtle.addshape('laser.gif')

def fire_laser():
    global score
    if start_clicked and (laser_cost <= score):
        display_per_mess()
        laser = turtle.Turtle()
        laser.up()
        laser.shape('square')
        laser.color('skyblue')
        laser.shapesize(0.25, 1)
        laser_sound.play()
        x = turtle.xcor() + 40      #Laser in front of the Megaman
        y = turtle.ycor() + 5       #Laser in line with Megaman's hand
        laser.goto(x, y)
        laser_set.append(laser)
        score -= laser_cost

turtle.onkeypress(fire_laser, 'a')


''' Weapon Firing '''
rank_button_x = -130
rank_button_y = menu_pos['y']-43
rank_button = turtle.Turtle()
rank_button.up()
rank_button.goto(rank_button_x, rank_button_y)
rank_button.color("black")
rank_button.begin_fill()

for _ in range(2):
    rank_button.forward(80)
    rank_button.left(90)
    rank_button.forward(25)
    rank_button.left(90)
rank_button.end_fill()
rank_button.color("white")
rank_button.goto(rank_button_x + 40, rank_button_y + 5)
rank_button.write("RANKING", font=("Arial", 10, "bold"), align="center")
rank_button.goto(rank_button_x + 40, rank_button_y + 13)
rank_button.shape("square")
rank_button.shapesize(1.25, 4) 
rank_button.color("")
rank_button.onclick(list_rank)


display_per_mess()
gmover_msg = turtle.Turtle()
gmover_msg.clear()
gmover_msg.up()
gmover_msg.hideturtle()

turtle.listen()
turtle.update()
turtle.done()

