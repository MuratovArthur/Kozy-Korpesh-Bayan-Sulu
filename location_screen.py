import pygame

class LocationScreen:
    def __init__(self):
        self.screen = pygame.image.load('data/screens/locations.png')
        self.choices = [pygame.image.load('data/screens/steppe.png'), pygame.image.load('data/screens/forest.png')]
        self.indicator_image = pygame.image.load('data/additional_images/arrow-indicator.png')
        self.left_player = pygame.transform.scale(pygame.image.load('data/players/kozy-korpesh.png'), (163, 381))
        self.right_player = pygame.transform.scale(pygame.image.load('data/players/bayan-sulu-front.png'), (168, 381))