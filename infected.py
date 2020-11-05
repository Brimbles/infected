import pygame
import sys
import random


def humanbirther_animation():
    global humanbirther_speed_x, humanbirther_speed_y
    humanbirther.x += humanbirther_speed_x
    humanbirther.y += humanbirther_speed_y

    if humanbirther.top <= 0 or humanbirther.bottom >= screen_height:
        humanbirther_speed_y *= -1
    if humanbirther.left <= 0 or humanbirther.right >= screen_width:
        humanbirther_speed_x *= -1

    if humanbirther.collidelist(population) or humanbirther.collidelist(infectedpopulation):
        #humanbirther_speed_x *= -1
        if random.randint(1, 100) == 1: #1% chance of direction change
            humanbirther_speed_x = 1 * random.choice((1, -1))
            humanbirther_speed_y = 1 * random.choice((1, -1))

def personanimation():
    person.y = person.y + random.randint(-2, 2)
    person.x = person.x + random.randint(-2, 2)
    if person.top <= 0 or person.bottom >= screen_height:
        person.y += -10
    if person.left <= 0 or person.right >= screen_width:
        person.x += -10


# def humanbirther_start():
#     global humanbirther_speed_x, humanbirther_speed_y

#     humanbirther.center = (screen_width / 2, screen_height / 2)
#     humanbirther_speed_y *= random.choice((1, -1))
#     humanbirther_speed_x *= random.choice((1, -1))

# def create_red_square(x, y):
#     red_width = 10
#     red_height = 10
#     red_color = pygame.Color("red")
#     red = pygame.Rect(red_x, red_y, red_width, red_height)
#     return red

def birth_new_person(x, y):
    """Return one instance of Rect at position x, y"""

    newperson = pygame.Rect(x, y, 10, 10)
    return newperson

####################################  General Pygame setup stuff  ###########################
# General setup
pygame.init()
clock = pygame.time.Clock()
myfont = pygame.font.SysFont("monospace", 16)

# Main Window
screen_width = 1200
screen_height =  600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('infected')

# Colors
light_grey = (200, 200, 200)
bg_color = pygame.Color('grey12')
red_color = pygame.Color("red")
white_color = pygame.Color("white")
blue_color = pygame.Color("blue")
green_color = pygame.Color("green")
####################################  my game variables   ###########################

# List of people - they should be born at the birth rate
population = [pygame.Rect(screen_width / 4 , screen_height / 4, 10, 10)] 

# list of infected people
infectedpopulation = [pygame.Rect(screen_width / 2 , screen_height / 2, 10, 10)] 

#List of infected that have been killed
infectedpopulationkilled = []

# Infection rates
infectionchance = 0.5

# Mortality rates
lessthan20 = 0
lessthan30 = 0.0001
lessthan40 = 0.001
lessthan50 = 0.002
lessthan60 = 0.006
lessthan70 = 0.02  # 2%
lessthan80 = 0.05
olderthan80 = 0.9

# Game Rectangles
humanbirther = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 10, 10)  # humanbirther starting position and size

# Game Variables
counter = 1
humanbirther_speed_x = 1 * random.choice((1, -1))
humanbirther_speed_y = 1 * random.choice((1, -1))

collisiontext = "no collision yet"


while True:
    # Move the people randomly
    for person in population:
        personanimation()

    # Move the infected people randomly
    for person in infectedpopulation:
        person.y += random.randint(-1, 1)
        person.x += random.randint(-1, 1)

	#Check for new infection
    for a in population:
        for b in infectedpopulation:
            if a.colliderect(b) and a != b:
                if int(counter/60) >=20: #At least 20 days have passed
                    if random.randint(1, 2) == 1: #50 percent chance of infection:
                        infectedpopulation.append(a)  # add person to the infected population
                        if a in population:
                            population.remove(a) #remove person from the non-infected population
    #Check for zombie killed
        for z in infectedpopulation:
            for a in population:
                if z.colliderect(a) and z != a:
                    if len(infectedpopulation) >1 : #zombie patient zero cannot be killed
                        if random.randint(1, 100) <= 5: #5 percent chance of killing zombie
                            infectedpopulationkilled.append(z)  # add to the killed zombies list
                            if z in infectedpopulation:
                                infectedpopulation.remove(z) #remove the zombie from the roaming zombies list

    # for i,obj1 in enumerate(population):
    # 	for j in range(i+1,len(population)):
    # 		obj2 = population[j]
    # 		if collide(obj1,obj2):
    # 			# obj1.kill()
    # 			# obj2.kill()
    # 			obj1.inflate(1,1)
    # 			obj2.inflate(1,1)
    # 			infectedpopulation.append(person)#add person to the infected population
    # 		population.remove(person)

    # if humanbirther.colliderect(player) or humanbirther.colliderect(opponent):
    # 	humanbirther_speed_x *= -1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # if event.type == pygame.KEYDOWN:
        # 	if event.key == pygame.K_UP:
        # 		player_speed -= 6
        # 	if event.key == pygame.K_DOWN:
        # 		player_speed += 6
        # if event.type == pygame.KEYUP:
        # 	if event.key == pygame.K_UP:
        # 		player_speed += 6
        # 	if event.key == pygame.K_DOWN:
        # 		player_speed -= 6

    # birth a new pixie
    if int(counter/60) % 10 == 0: #every 10 seconds
        if random.randint(1, 10) ==1: #10 percent chance of birth
            pos_left, pos_top = humanbirther.left, humanbirther.top
            population.append(birth_new_person(pos_left + 2, pos_top + 2)) 

    # move pixie to infected population

    # Game Logic
    humanbirther_animation()
    counter += 1


    # Visuals
    screen.fill(bg_color)
    pygame.draw.ellipse(screen, bg_color, humanbirther)
    #pygame.draw.aaline(screen, light_grey, (screen_width / 2, 0),(screen_width / 2, screen_height))
    for person in population:
        #screen.fill(red_color, person)#display all people
        pygame.draw.ellipse(screen, white_color, person)
        #pygame.draw.rect(screen,white_color,person)
    for person in infectedpopulation:
        #screen.fill(red_color, person)#display all people
        if int(counter/60) >=20: #At least 20 days have passed
            pygame.draw.ellipse(screen, green_color, person)
        #pygame.draw.rect(screen,red_color,person)

    # display counter

    elapsedtimetext = myfont.render("Elapsed time in days= " + str(int(counter/60)), 1, light_grey)
    screen.blit(elapsedtimetext, (20, 20))
	
    populationtext = myfont.render("Human population =" +str(len(population)), 1, light_grey)
    screen.blit(populationtext, (20, 40))

    if int(counter/60) >=20: #At least 20 days have passed
        infectedpopulationtext = myfont.render("Zombie population =" +str(len(infectedpopulation)), 1, green_color)
        screen.blit(infectedpopulationtext, (20, 60))

    if int(counter/60) >=20: #At least 20 days have passed
        infectedpopulationkilledtext = myfont.render("Zombies killed =" +str(len(infectedpopulationkilled)), 1, green_color)
        screen.blit(infectedpopulationkilledtext, (20, 80))

    rulestext = myfont.render("Infection can only be be transmitted after day 20", 1, light_grey)
    screen.blit(rulestext, (20, 100))
    rulestext1 = myfont.render("Each interaction has a 50 percent chance of transmission", 1, light_grey)
    screen.blit(rulestext1, (20, 120))
    rulestext2 = myfont.render("Each interaction has a 5 percent chance of a human smushing a zombie", 1, light_grey)
    screen.blit(rulestext2, (20, 140))
    rulestext3 = myfont.render("There's a chance the human population will boom every 10 days", 1, light_grey)
    screen.blit(rulestext3, (20, 160))

    pygame.display.flip()
    clock.tick(10)
