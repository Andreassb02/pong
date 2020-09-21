import os
import sys
import random
import pygame
import math
from pygame.locals import *
import settings
import utils
from base_pipe import BasePipe

# Denne jobber Noah med
class StraightPipe(BasePipe):
    def __init__(self, position):
        BasePipe.__init__(self, position)
        self.current_pos_X = 0
        self.current_pos_y = 0
        self.flow_rect = Rect(0,0,settings.FLOW_WIDTH, 0)
        self.flow_rect.left = (settings.TUBE_SIZE / 2) - (settings.FLOW_WIDTH / 2)
        
    def update(self):
        BasePipe.update(self)
        if self.current_pos_y < settings.TUBE_SIZE:
            self.current_pos_y += 1
        self.flow_rect.bottom = self.current_pos_y
        pygame.draw.rect(self.image, settings.FLOW_COLOR, self.flow_rect, 1)
        self.image.blit(utils.debug_text('Noah'), (3,3))