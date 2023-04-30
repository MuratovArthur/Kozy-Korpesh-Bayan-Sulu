import sys
import pygame
from pygame.locals import *
import csv

class GameGraphics:
    def __init__(self, location):
        self.load_map(f'data/csvs/{location}.csv')
        self.load_images(f'data/additional_images/{location}.png')
        self.collidable_blocks()
        self.make_water_blocks()
        
    def load_map(self, path):
       
        with open(path) as csvfile:
            reader = csv.reader(csvfile)
            rows = list(reader)
            
        self.game_map = rows

    def load_images(self, img_path):
        self.background = pygame.image.load(img_path)
        self.board_textures = {}
        for i in range(625):
            filename = f"data/tiles/{i}.png"
            texture = pygame.image.load(filename)
            self.board_textures[str(i)] = texture

    def collidable_blocks(self):
        CHUNKS_SIZE = 16
        self.collidable_blocks = []
        for y, row in enumerate(self.game_map):
            for x, cell in enumerate(row):
                if cell not in ['-1','481','482','483','484','96','95','94','119','120','121','122','180','181','182','183','184','205','206','207','208','209']:
                    self.collidable_blocks.append(pygame.Rect(x * 16, y * 16, 16, 16))

    def make_water_blocks(self):  
        self.water_blocks = []
        for y, row in enumerate(self.game_map):
            for x, cell in enumerate(row):
                if cell in ['481','482','483','484']:
                    self.water_blocks.append(
                        pygame.Rect(x * 16, y * 16 + 16 / 2, 16, 16 / 2))
