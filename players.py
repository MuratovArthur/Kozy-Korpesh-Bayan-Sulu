import sys
import pygame
from pygame.locals import *

class Player:
    def __init__(self, position, image_path):
        self.image = pygame.transform.scale(pygame.image.load(image_path), (16, 32))
        self.rect = pygame.Rect(position[0], position[1], self.image.get_width(), self.image.get_height())
        self.moving_right = self.moving_left = self.jumping = False
        self.y_velocity = self.time_in_air = 0
        self.active = True
        self.last_move = "right"

    def calc_movement(self):
        self._movement = [3 if self.moving_right else -3 if self.moving_left else 0, self.y_velocity]
        if self.jumping: self.y_velocity = -4; self.jumping = False
        self._movement[1] += self.y_velocity
        self.y_velocity += (1 - 0.8)

    def stop_player(self): self.moving_right = self.moving_left = self.jumping = False
    def unactivate(self): self.active = False
    def get_movement(self): return self._movement
    def is_inactive(self): return self.active is False
    def get_type(self): return self._type
