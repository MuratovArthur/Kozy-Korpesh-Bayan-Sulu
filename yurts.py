import sys
import pygame
from pygame.locals import *


class Yurta:
    def __init__(self, yurta_location):
        self.yurta_location = self.yurta_door_location = yurta_location
        self.load_images()
        self.player_inside = False
        self.yurta_open = False
        self.height_raised = 0

    def load_images(self):
        self.open_yurta_image = pygame.image.load("data/additional_images/yurt_open.png")
        self.placeholder = pygame.image.load("data/additional_images/placeholder.png")
        self.yurta_door_image = pygame.image.load("data/additional_images/door.png")
        self.yurta_door_rect = pygame.Rect(self.yurta_door_location[0], self.yurta_door_location[1], self.yurta_door_image.get_width(), self.yurta_door_image.get_height())

    def try_open_yurta(self):
        if self.player_at_yurta and not self.yurta_open:
            self.yurta_door_location = (self.yurta_door_location[0], self.yurta_door_location[1] - 1)
            self.height_raised += 1
            if self.height_raised >= 31:
                self.yurta_open = True
        
        elif not self.player_at_yurta and self.height_raised > 0:  
            self.yurta_door_location = (self.yurta_door_location[0], self.yurta_door_location[1] + 1)
            self.height_raised -= 1
            self.yurta_open = False
