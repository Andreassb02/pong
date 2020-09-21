import os
import sys
import random
import pygame
import math
from pygame.locals import *
import settings
import utils
from base_pipe import BasePipe

# Denne jobber TØH
class StartPipe(BasePipe):
    def __init__(self, position):
        BasePipe.__init__(self, position)
        # Flyttet initaliseringen av flow til en egen init funksjon - mer ryddig og lettere å test
        self.init_flow()


    def init_flow(self):
        self.image.fill(settings.BLOCK_BACKGROUND_COLR)

        # Plasserer flow i forhold til valgt retning
        self.current_pos_X = 0
        self.current_pos_y = 0
        if (self.flow_dir == settings.FLOW_TB) or (self.flow_dir == settings.FLOW_BT):
            self.flow_rect = Rect(0,0,settings.FLOW_WIDTH, 0)
            self.flow_rect.left = (settings.TUBE_SIZE / 2) - (settings.FLOW_WIDTH / 2)
            self.current_pos_y = settings.TUBE_SIZE / 2
            
        if (self.flow_dir == settings.FLOW_LR) or (self.flow_dir == settings.FLOW_RL):
            self.flow_rect = Rect(0,0,0,settings.FLOW_WIDTH)
            self.flow_rect.left = (settings.TUBE_SIZE / 2)
            self.flow_rect.top = (settings.TUBE_SIZE / 2) - (settings.FLOW_WIDTH / 2)
            self.current_pos_x = (settings.TUBE_SIZE / 2)  - (settings.FLOW_WIDTH / 2)

    def update(self):
        BasePipe.update(self)
        if self.flow_dir == settings.FLOW_TB:
            if self.current_pos_y < settings.TUBE_SIZE:
                self.current_pos_y += 1
                self.flow_rect.bottom = self.current_pos_y
            else:
                # Dette er testkode for å sjekke alle retninger
                self.flow_dir = settings.FLOW_BT
                self.init_flow()

        elif self.flow_dir == settings.FLOW_BT:
            if self.current_pos_y > 0:
                self.current_pos_y -= 1
                self.flow_rect.top = self.current_pos_y
            else:
                self.flow_dir = settings.FLOW_LR
                self.init_flow()

        elif self.flow_dir == settings.FLOW_LR:
            if self.current_pos_x < settings.TUBE_SIZE:
                self.current_pos_x += 1
                self.flow_rect.right = self.current_pos_x
            else:
                self.flow_dir = settings.FLOW_RL
                self.init_flow()

        elif self.flow_dir == settings.FLOW_RL:
            if self.current_pos_x > 0:
                self.current_pos_x -= 1
                self.flow_rect.left = self.current_pos_x
            else:
                self.flow_dir = settings.FLOW_TB
                self.init_flow()




 
        pygame.draw.rect(self.image, settings.FLOW_COLOR, self.flow_rect, 1)
        self.image.blit(utils.debug_text('Tom'), (3,3))
        font = pygame.font.SysFont('', 40)
        # font.render returnerer et surface
        font_surface = font.render('S', True, (0, 0, 0))
        self.image.blit(font_surface, (settings.TUBE_SIZE/2-10,settings.TUBE_SIZE/2-10))
        