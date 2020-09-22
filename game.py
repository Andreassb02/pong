import os
import sys
import pygame
import ast
from pygame.locals import *
import settings
import utils
import random
from start_pipe import StartPipe
from straight_pipe import StraightPipe
from bent_pipe import BentPipe
from cross_pipe import CrossPipe
from grid import draw_grid
from score import draw_scores

# Importerer bare de classene vi trenger fra sprites filen
#from sprites import StaticElement, MovingElement, BouncingElement

# Sentrerer pygame vinduet
os.environ['SDL_VIDEO_CENTERED'] = '1'

# Initaliserer Pygame modulen
pygame.init()

# Bruker pygame.time modulen for å holde en kostant Framerate
clock = pygame.time.Clock()
pygame.font.init() # Initaliserer fonter

# Gjentagelse av tastetrykk
pygame.key.set_repeat(10, 10)

# Lager et display objekt.
# Denne gir fullskjerm
#screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN | pygame.DOUBLEBUF) 
# Denne bruker variablene fra settings.py for å bestemme vinduets bredde og høyde
screen = pygame.display.set_mode((settings.SCREEN_WIDTH, settings.SCREEN_HEIGHT)) 

# Lager en surface (Et ark) som er like stort som skjermen
surface = pygame.Surface(screen.get_size())
# Setter Pixel formatet til det samme som "Display"
surface.convert()

# En sprite group er en liste med sprite objekter
planned = pygame.sprite.Group()
placed = pygame.sprite.Group()

#test_base_tube = BaseTube((9,6))


#for x in range(settings.GRID[0]):
#    for y in range(settings.GRID[1]):
#        placed.add(StartPipe((x,y)))

pipes = (StraightPipe, BentPipe, CrossPipe)
coming_pipes = [random.choice(pipes) for r in range(4)]
grid_taken = []

placed.add(coming_pipes[3]((-2,0)))
placed.add(coming_pipes[2]((-2,1)))
placed.add(coming_pipes[1]((-2,2)))
placed.add(coming_pipes[0]((-2,3)))

while True:
    # Event pump sjekker om det har skjedd noe eks. tastetyrkk og musklikk
    # Andreas jobber med dette. Kan teste StartPipe?
    next_pipe = coming_pipes[0]
    pygame.event.pump()
    for event in pygame.event.get():
        # Avslutter ved Window X eller Q tast
        if (event.type == QUIT) or ((event.type == KEYDOWN) and (event.key == K_q)):
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONUP:
            mouse_coords = pygame.mouse.get_pos()
            x_grid = int((mouse_coords[0]-200)/80)
            y_grid = int((mouse_coords[1]-80)/80)
            if mouse_coords[0] < 200 or mouse_coords[1] < 80 or x_grid > 9 or y_grid > 6 or f"{x_grid},{y_grid}" in grid_taken:
                pass
            else:
                placed.add(next_pipe((x_grid,y_grid)))
                grid_taken.append(f"{x_grid},{y_grid}")
                print(grid_taken)
                coming_pipes.pop(0)
                coming_pipes.append(random.choice(pipes))
                placed.add(coming_pipes[3]((-2,0)))
                placed.add(coming_pipes[2]((-2,1)))
                placed.add(coming_pipes[1]((-2,2)))
                placed.add(coming_pipes[0]((-2,3)))
            

    # Fyller surface med farge (RGB)
    surface.fill((255, 255, 255))
    
    # Listen har en update() funksjon. Den kaller i tur og orden update() funksjonen 
    # på objektene vi har lagt til i elements listen. 
    # eks. For sprite in elements.sprites:
    #   sprite.update()
    # Selv om spritene er av forskjellig type, så vil en kunne kalle update() uten å sjekke type.
    # Det er det som menes med "polymorfi" i objektorientertprogramering.
    planned.update()
    placed.update()
    draw_grid(surface)

    # elements.draw() går gjennom alle objektene i listen.
    # Fuksjonen bruker så image og rect egenskapene fra spritene for å tegne dem på "surface"
    planned.draw(surface)
    placed.draw(surface)

    # Her blir surface tegnet på skjerm
    screen.blit(surface, (0,0))
 
    # Disse funksjonene forteller pygame at "skjermen" skal oppdateres med innholdet i "screen"
    pygame.display.flip()
    pygame.display.update()

    # Her tar programmet en pause for at det skal kjøre med en hastighet på frames pr. second.
    # FPS er en "konstant" vi har opprettet i settings modulen 
    clock.tick(settings.FPS)