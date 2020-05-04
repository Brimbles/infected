import pygame
import sys
import random



def pixiequeen_animation():
    global pixiequeen_speed_x, pixiequeen_speed_y
    pixiequeen.x += pixiequeen_speed_x
    pixiequeen.y += pixiequeen_speed_y

    if pixiequeen.top <= 0 or pixiequeen.bottom >= screen_height:
        pixiequeen_speed_y *= -1
    if pixiequeen.left <= 0 or pixiequeen.right >= screen_width:
        pixiequeen_speed_x *= -1

    if pixiequeen.collidelist(population) or pixiequeen.collidelist(infectedpopulation):
        #pixiequeen_speed_x *= -1
        if random.randint(1, 100) == 1: #1% chance of direction change
            pixiequeen_speed_x = 1 * random.choice((1, -1))
            pixiequeen_speed_y = 1 * random.choice((1, -1))

def personanimation():
    person.y = person.y + random.randint(-2, 2)
    person.x = person.x + random.randint(-2, 2)
    if person.top <= 0 or person.bottom >= screen_height:
        person.y += -10
    if person.left <= 0 or person.right >= screen_width:
        person.x += -10




# def pixiequeen_start():
#     global pixiequeen_speed_x, pixiequeen_speed_y

#     pixiequeen.center = (screen_width / 2, screen_height / 2)
#     pixiequeen_speed_y *= random.choice((1, -1))
#     pixiequeen_speed_x *= random.choice((1, -1))

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
screen_width = 500
screen_height =  600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('infected')

# Colors
light_grey = (200, 200, 200)
bg_color = pygame.Color('grey12')
red_color = pygame.Color("red")
white_color = pygame.Color("white")
blue_color = pygame.Color("blue")
####################################  my game variables   ###########################

# List of people - they should be born at the birth rate
population = [pygame.Rect(screen_width / 4 , screen_height / 4, 10, 10)] 

# list of infected people
infectedpopulation = [pygame.Rect(screen_width / 2 , screen_height / 2, 10, 10)] 


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
pixiequeen = pygame.Rect(screen_width / 2 - 15, screen_height / 2 - 15, 10, 10)  # pixiequeen starting position and size

# Game Variables
counter = 1
pixiequeen_speed_x = 1 * random.choice((1, -1))
pixiequeen_speed_y = 1 * random.choice((1, -1))

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
                if int(counter/60) >=60: #At least 60 days have passed
                    if random.randint(1, 100) ==1: #1 percent chance of infection:
                        infectedpopulation.append(a)  # add person to the infected population
                        if a in population:
                            population.remove(a) #remove person from the non-infected population


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

    # if pixiequeen.colliderect(player) or pixiequeen.colliderect(opponent):
    # 	pixiequeen_speed_x *= -1

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
            pos_left, pos_top = pixiequeen.left, pixiequeen.top
            population.append(birth_new_person(pos_left + 2, pos_top + 2)) 

    # move pixie to infected population

    # Game Logic
    pixiequeen_animation()
    counter += 1


    # Visuals
    screen.fill(bg_color)
    pygame.draw.ellipse(screen, bg_color, pixiequeen)
    #pygame.draw.aaline(screen, light_grey, (screen_width / 2, 0),(screen_width / 2, screen_height))
    for person in population:
        #screen.fill(red_color, person)#display all people
        pygame.draw.ellipse(screen, white_color, person)
        #pygame.draw.rect(screen,white_color,person)
    for person in infectedpopulation:
        #screen.fill(red_color, person)#display all people
        pygame.draw.ellipse(screen, red_color, person)
        #pygame.draw.rect(screen,red_color,person)

    # display counter

    elapsedtimetext = myfont.render("Elapsed time in days= " + str(int(counter/60)), 1, (200, 0, 0))
    screen.blit(elapsedtimetext, (20, 20))
	
    populationtext = myfont.render("Uninfected population =" +str(len(population)), 1, (200, 0, 0))
    screen.blit(populationtext, (20, 40))

    infectedpopulationtext = myfont.render("Infected population =" +str(len(infectedpopulation)), 1, (200, 0, 0))
    screen.blit(infectedpopulationtext, (40, 60))

    rulestext = myfont.render("Infection can only be be transmitted after day 60, each interaction has a 1 percent chance of transmission ", 1, (200, 0, 0))
    screen.blit(rulestext, (40, 80))

    pygame.display.flip()
    clock.tick(60)
