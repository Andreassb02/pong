import os
import sys
import pygame
from pygame.locals import *
import settings
import utils
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

placed.add(StartPipe((2,3)))
placed.add(StraightPipe((4,3)))
placed.add(BentPipe((6,3)))
placed.add(CrossPipe((8,3)))




#for x in range(settings.GRID[0]):
#    for y in range(settings.GRID[1]):
#        placed.add(StartPipe((x,y)))



while True:
    # Event pump sjekker om det har skjedd noe eks. tastetyrkk og musklikk
    # Andreas jobber med dette. Kan teste StartPipe?
    pygame.event.pump()
    for event in pygame.event.get():
        # Avslutter ved Window X eller Q tast
        if (event.type == QUIT) or ((event.type == KEYDOWN) and (event.key == K_q)):
            pygame.quit()
            sys.exit()

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
