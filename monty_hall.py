#%%
from random import choice
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.backends.backend_agg as agg
matplotlib.use("Agg")

import os 
#os.chdir(r"/home/ted/Desktop/monty_hall")
os.chdir(r"C:\Users\theodore-tinker\Desktop\monty_hall")

import pygame

bg   = pygame.image.load('images/background.png')
d1   = pygame.image.load('images/door_1.png')
d2   = pygame.image.load('images/door_2.png')
d3   = pygame.image.load('images/door_3.png')
goat = pygame.image.load('images/goat.png')
car  = pygame.image.load('images/car.png')

pygame.init()
screen = pygame.display.set_mode([bg.get_rect()[2], bg.get_rect()[3]])

text_box = pygame.Surface((bg.get_rect()[2]-20, 80))
text_box.fill((0,0,0))
my_font = pygame.font.SysFont("arial", 25)
text_surface = my_font.render("", False, (255, 255, 255))
def put_text(text):
    screen.blit(text_box, (10,10))
    text = my_font.render(text, False, (255, 255, 255))
    screen.blit(text, (bg.get_rect()[2]/2 - text.get_rect()[2]/2, 30))



def door_click(pos):
    if(pos[1] >= 99):
        if(pos[0] >= 213 and pos[0] <= 550): return(1)
        if(pos[0] >= 571 and pos[0] <= 908): return(2)
        if(pos[0] >= 929 and pos[0] <= 1267): return(3)
    return(None)

def door_state(d1_state = "closed", d2_state = "closed", d3_state = "closed"):
    screen.blit(bg, (0, 0))
    
    if(d1_state == "closed"): screen.blit(d1, (213, 99))
    if(d2_state == "closed"): screen.blit(d2, (571, 99))
    if(d3_state == "closed"): screen.blit(d3, (929, 99))
    
    if(d1_state == "goat"): screen.blit(goat, (223, 470))
    if(d2_state == "goat"): screen.blit(goat, (581, 470))
    if(d3_state == "goat"): screen.blit(goat, (939, 470))
    
    if(d1_state == "car"): screen.blit(car, (273, 180))
    if(d2_state == "car"): screen.blit(car, (631, 180))
    if(d3_state == "car"): screen.blit(car, (989, 180))
    


step = "start"
games = 0 ; switch_wins = 0 ; stay_wins = 0 ; switch_win_probs = []
car_door = choice([1,2,3]) ; door_options = [1,2,3] ; door_choice = None
    
running = True
while running:
    end_step = False
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
    
    if(step == "start"):
        car_door = choice([1,2,3])
        door_options = [1,2,3]
        door_choice = None
        door_state()
        put_text("Can you win a car? Choose a door!")
        step = "wait_1" ; end_step = True
    
    if(step == "wait_1"):
        for event in events:
            if(end_step): break
            if event.type == pygame.MOUSEBUTTONUP:
                clicked_door = door_click(pygame.mouse.get_pos())
                if(clicked_door != None and clicked_door in door_options):
                    door_choice = clicked_door 
                    step = "open_1" ; end_step = True
                
    if(step == "open_1"):
        alt_door = choice([d for d in door_options if not d in [door_choice, car_door]])
        door_state(
            "goat" if alt_door == 1 else "closed", 
            "goat" if alt_door == 2 else "closed", 
            "goat" if alt_door == 3 else "closed")
        put_text("You chose door {}. Notice door {} has a goat behind it. Will you switch to door {}?".format(
            door_choice, alt_door, [d for d in door_options if not d in [door_choice, alt_door]][0]))
        prev_door = door_choice; door_choice = None
        door_options = [d for d in door_options if d != alt_door]
        step = "wait_2" ; end_step = True
        
    if(step == "wait_2"):
        for event in events:
            if(end_step): break
            if event.type == pygame.MOUSEBUTTONUP:
                clicked_door = door_click(pygame.mouse.get_pos())
                if(clicked_door != None and clicked_door in door_options):
                    door_choice = clicked_door 
                    switched = door_choice != prev_door
                    step = "open_2" ; end_step = True
                    
    if(step == "open_2"):
        door_state(
            "goat" if alt_door == 1 or (door_choice == 1 and car_door != 1) else "car" if (door_choice == 1 and car_door == 1) else "closed", 
            "goat" if alt_door == 2 or (door_choice == 2 and car_door != 2) else "car" if (door_choice == 2 and car_door == 2) else "closed", 
            "goat" if alt_door == 3 or (door_choice == 3 and car_door != 3) else "car" if (door_choice == 3 and car_door == 3) else "closed", )
        put_text("Behind door {}: {}!          Click to see graph.".format(
            door_choice, "car" if door_choice == car_door else "goat"))
        games += 1
        switch_wins += 1 if (switched and door_choice == car_door) or (not switched and door_choice != car_door) else 0
        stay_wins   += 1 if (switched and door_choice != car_door) or (not switched and door_choice == car_door) else 0
        switch_win_probs.append(100*(switch_wins / games))
        step = "wait_3" ; end_step = True
        
    if(step == "wait_3"):
        for event in events:
            if(end_step): break
            if event.type == pygame.MOUSEBUTTONUP:
                step = "graph" ; end_step = True
                
    if(step == "graph"):
        put_text("Look at the graph. Is it better to stay or switch?")
        
        w = 10; h = 6
        fig = plt.figure(figsize=[w, h], dpi=100)
        ax = fig.gca()
        ax.set_title("Games won with staying or switching")
        ax.set_xlabel("Games played")
        ax.set_ylabel("Proportion of wins by staying or switching")
        ax.plot([g+1 for g in range(games)], [50 for g in range(games)], color = (0,0,0,.5), linestyle = "--")
        ax.plot([g+1 for g in range(games)], [100/3 for g in range(games)], color = (0,0,0,.3), linestyle = "--")
        ax.plot([g+1 for g in range(games)], [200/3 for g in range(games)], color = (0,0,0,.3), linestyle = "--")
        ax.plot([g+1 for g in range(games)], switch_win_probs, color = "blue", label = "Switch")
        ax.plot([g+1 for g in range(games)], [100-p for p in switch_win_probs], color = "green", label = "Stay")
        ax.set_ylim([0,100])
        ax.set_yticks([0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
        ax.set_yticklabels([str(i) + "%" for i in [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]])
        ax.text(1,100/3, "33%", color = (0,0,0,.3)); ax.text(1,200/3, "66%", color = (0,0,0,.3)) 
        ax.text(games,switch_win_probs[-1], str(round(switch_win_probs[-1],3)) + "%", color = "blue")
        ax.text(games,100-switch_win_probs[-1], str(round(100-switch_win_probs[-1],3)) + "%", color = "green")
        ax.legend()
        canvas = agg.FigureCanvasAgg(fig)
        canvas.draw()
        size = canvas.get_width_height()
        renderer = canvas.get_renderer()
        raw_data = renderer.tostring_rgb()
        surf = pygame.image.fromstring(raw_data, size, "RGB")
        screen.blit(surf, (bg.get_rect()[2]/2-w*100/2, 130))
        
        step = "wait_4" ; end_step = True
        
    if(step == "wait_4"):
        for event in events:
            if(end_step): break
            if event.type == pygame.MOUSEBUTTONUP:
                plt.close()
                step = "start" ; end_step = True
                
    pygame.display.flip()
pygame.quit()
# %%
