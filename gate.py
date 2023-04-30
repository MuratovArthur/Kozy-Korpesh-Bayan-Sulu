import sys
import pygame
from pygame.locals import *


class Gate:
    def __init__(self, gate_location, plates_locations):
        self.gate_location = gate_location
        self.plates_locations = plates_locations
        self.plate_is_pressed = False
        self.gate_is_open = False
        self.load_images()

    def load_images(self):
        self.gate_image = pygame.image.load('data/gates_and_plates/gate.png')
        self.plate_image = pygame.image.load('data/gates_and_plates/plate.png')
        self.gate_rect = pygame.Rect(self.gate_location[0], self.gate_location[1], self.gate_image.get_width(), self.gate_image.get_height())
        self.plates = []
        for plate_location in self.plates_locations:
            self.plates.append(pygame.Rect(plate_location[0], plate_location[1], self.plate_image.get_width(), self.plate_image.get_height()))

    def try_open_gate(self):
        
        if self.plate_is_pressed and not self.gate_is_open:
            self.gate_location = (self.gate_location[0], self.gate_location[1] - 32)
            self.gate_rect.y -= 32
            self.gate_is_open = True

        if not self.plate_is_pressed and self.gate_is_open:
            self.gate_location = (self.gate_location[0], self.gate_location[1] + 32)
            self.gate_rect.y += 32
            self.gate_is_open = False

    def get_solid_blocks(self):
        return [self.gate_rect]