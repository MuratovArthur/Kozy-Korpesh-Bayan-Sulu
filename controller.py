import sys
import pygame
from pygame.locals import *

class Controller:
    def __init__(self, control_keys): 
        self.controls = control_keys

    def control_player(self, events, player):
        for event in events:
            key_action = {KEYDOWN: True, KEYUP: False}.get(event.type)
            if key_action is not None:
                for k, v in self.controls.items():
                    if event.key == v: setattr(player, f"moving_{k}", key_action)
                    if event.key == self.controls["up"] and player.time_in_air < 6: player.jumping = key_action