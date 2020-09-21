import os
import sys
import random
import pygame
import math
from pygame.locals import *
import settings
import utils

# Vi lager an baseclass for å enkelt kunne gjøre noen endringer som vil påvisrke alle
# klassene våre. Denne klassen "arver" Sprite klassen. sprite.Group jobber med Sprite objekter
# så objektene våre må arve Sprite for å brukes med sprite.Group.
class BasePipe(pygame.sprite.Sprite):
    # Alle classene som er nedarvet fra Sprite trenger en image egenskap for at sprite.Group skal kunne
    # tegne dem. Vi kan derfor ha et parmeter som vil brukes av alle de arvede klassene.
    # __init__ er en "magisk" funksjon. Det er den som brukes når en opretter objekt.
    # Eks. objekt = StaticElement(settings.ITEM_CRATE_BROWN, (200, 100)) 
    def __init__(self, position, flow_dir = settings.FLOW_LR):
        # Vi kaller __init__ til den klassen vi har arvet fra
        # Vi bør egentlig bruke "super()" funksjonen for dette, men det kan være lettere
        # å lese når en skriver navnet på klassen en arver fra
        pygame.sprite.Sprite.__init__(self)

        # Vi setter sammen filnavnet til bilde vi skal laste
        #filename = os.path.join(settings.ASSETS_DIR, graphic['filename'])
        
        # I utils modulen som vi har laget, så har vi laget en funskjon for å lettere laste og kovertere bilde
        # til et format som pygame enkelt jobber med
        # self er instansen av klassen (også kalt objektet)
        #
        # Når vi setter variabler (også kalt egenskaper) på instansen,
        # Så smaler vi data og kode, variabler og metoder i instansen. 
        # Det er det vi mener med "innkapsling"
        #self.image = utils.load_image(filename, graphic['size'])
        
        self.hit = False
        self.image = pygame.Surface((settings.TUBE_SIZE, settings.TUBE_SIZE))
        self.image.fill(settings.BLOCK_BACKGROUND_COLR)

        self.flow_dir = flow_dir
        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.position = position
        self.rect.x = (self.position[0] * settings.TUBE_SIZE) + settings.GRID_OFFSET[0]
        self.rect.y = (self.position[1] * settings.TUBE_SIZE) + settings.GRID_OFFSET[1]




    # Update er funskjonen som kalles fra sprite.Group for å oppdatere objektene våre.
    # Denne update vil aldri kalles direkte, så vi har bare laget litt kode her i forbindelse
    # med evnt. feilsøking eller for lettere å se omkretsen til bildene vi bruker
    def update(self):
        if settings.DEBUG:
            draw_rect = self.rect
            draw_rect = pygame.rect.Rect(0,0, self.rect.width-1, self.rect.height -1)
            pygame.draw.rect(self.image, (255, 0, 0), draw_rect, 1)
            
 
