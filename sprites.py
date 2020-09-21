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
class Element(pygame.sprite.Sprite):
    # Alle classene som er nedarvet fra Sprite trenger en image egenskap for at sprite.Group skal kunne
    # tegne dem. Vi kan derfor ha et parmeter som vil brukes av alle de arvede klassene.
    # __init__ er en "magisk" funksjon. Det er den som brukes når en opretter objekt.
    # Eks. objekt = StaticElement(settings.ITEM_CRATE_BROWN, (200, 100)) 
    def __init__(self, graphic):
        # Vi kaller __init__ til den klassen vi har arvet fra
        # Vi bør egentlig bruke "super()" funksjonen for dette, men det kan være lettere
        # å lese når en skriver navnet på klassen en arver fra
        pygame.sprite.Sprite.__init__(self)

        # Vi setter sammen filnavnet til bilde vi skal laste
        filename = os.path.join(settings.ASSETS_DIR, graphic['filename'])
        
        # I utils modulen som vi har laget, så har vi laget en funskjon for å lettere laste og kovertere bilde
        # til et format som pygame enkelt jobber med
        # self er instansen av klassen (også kalt objektet)
        #
        # Når vi setter variabler (også kalt egenskaper) på instansen,
        # Så smaler vi data og kode, variabler og metoder i instansen. 
        # Det er det vi mener med "innkapsling"
        self.image = utils.load_image(filename, graphic['size'])
        
        # Vi finner "rect" ved å sette det likt bilde sin størrelse
        self.rect = self.image.get_rect()

    # Update er funskjonen som kalles fra sprite.Group for å oppdatere objektene våre.
    # Denne update vil aldri kalles direkte, så vi har bare laget litt kode her i forbindelse
    # med evnt. feilsøking eller for lettere å se omkretsen til bildene vi bruker
    def update(self):
        if settings.DEBUG:
            draw_rect = self.rect
            draw_rect = pygame.rect.Rect(0,0, self.rect.width-1, self.rect.height -1)
            pygame.draw.rect(self.image, (255, 0, 0), draw_rect, 1)


# Vi lager en ny klasse som "arver" Elemement klassen vår over
class StaticElement(Element):
    # Denne brukes for statiske elementer - elementer som ikke beveger seg.
    # i __init__ har vi laget et ekstra parameter som angir posisjon
    def __init__(self, graphic, position):
        # Vi kaller __init__ for det arvede objektet
        # Det vil laste bilde og sette rect lik dimensjonene til bilde
        Element.__init__(self, graphic)

        # Rect er satt iv "foreldre" objektet, vi trenger derfor bare å legge inn 
        # posijonen
        self.rect.left = position[0]
        self.rect.top = position[1]

    # def update(self)
    # Vi trenger ikke noen egen update funskjon her, siden det ikke skal skje noe nytt
    # I forhold til update() til forelder. Det er forelder sin update som vil bli brukt av seg selv.
    # Ref. arv

# Vi definerer en klasse for element som beveger seg   
class MovingElement(StaticElement):
    # Siden det beveger seg, så må det også ha en hastighet
    # speed er en liste med to elementer, hastighet i x reting og hastighet i y. retning
    def __init__(self, graphic, position, speed):
        StaticElement.__init__(self, graphic, position)

        # Vi bruker spees for å sette egenskapen / variablene som vi kaller dx og dy
        # Jeg tenker på dem som "delta x" og "delta y" - den greske bokstaven delta brukes ofte
        # i fysikk for differansen mellom to tall.
        self.dx = speed[0]
        self.dy = speed[1]

    # Her overstyrer vi update() fra foreldre klassen og det vil da være denne
    # sprite.Update() vil bruke - ref. polymorfi
    def update(self):
        StaticElement.update(self)
        # Vi endrer x og y posisjonen fil bilde - elementet vårt
        self.rect.left += self.dx
        self.rect.top += self.dy

# Vi lager en spesialisering av MovingElement for å sjekke om vi har truffet endene av skjermen.
# Treffer vi enden så endrer elemtet retning
class BouncingElement(MovingElement):
    def update(self):
        MovingElement.update(self)

        # Disse testene er for enkle. Kommer en litt skeivt ut og objektet beveger seg helt ut av
        # vinduet, så vil det bare sprette frem og tilbake utenfor det synlig vinduet.
        if (self.rect.left <= 0) or (self.rect.right > settings.SCREEN_WIDTH):
            self.dx *= -1
        
        if (self.rect.top <= 0) or (self.rect.bottom >= settings.SCREEN_HEIGHT):
            self.dy *= -1

