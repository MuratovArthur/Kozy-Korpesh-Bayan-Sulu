import sys
import pygame
from pygame.locals import *

class GameEngine:
    def __init__(self, game_data):
        self.screen = pygame.display.set_mode((544, 400))
        pygame.display.set_caption("nFactorial Incubator 2023")
        self.display = pygame.Surface((544, 400))
        self.game_data = game_data
        icon = pygame.image.load("data/additional_images/icon.png")
        pygame.display.set_icon(icon)

    def draw_location_screen(self, locations):
        self.display.blit(locations.screen, (0, 0))
        for i in range(2):
            image = locations.choices[i]
            self.display.blit(image, (225.5, 50 * i + 100))
        self.display.blit(locations.left_player, (10, 70))
        self.display.blit(locations.right_player, (370, 60))


    def _blit_images(self, screen, choices, left_player, right_player):
        self.display.blit(screen, (0, 0))
        for i, image in enumerate(choices):
            self.display.blit(image, (225.5, 50 * i + 100))
        self.display.blit(left_player, (10, 70))
        self.display.blit(right_player, (370, 60))

    def select_location(self, locations):
        location_index = 0
        locations_dict = {0: "steppe", 1: "forest"}
        while True:
            self.draw_location_screen(locations)
            events = pygame.event.get()
            location_index = self._handle_events(events, location_index)
            if location_index is None:
                return None
            self.draw_location_select_indicator(locations, location_index)
            if self._location_selected(events):
                return locations_dict[location_index]

    def _handle_events(self, events, location_index):
        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_DOWN:
                    location_index = (location_index + 1) % 2
                elif event.key == K_UP:
                    location_index = (location_index - 1) % 2
                elif event.key == K_ESCAPE:
                    return None
            elif event.type == QUIT:
                pygame.quit()
                sys.exit()
        return location_index

    def _location_selected(self, events):
        for event in events:
            if event.type == KEYDOWN and event.key == K_RETURN:
                return True
        return False

    def draw_location_select_indicator(self, locations, location_index):
        location_y = location_index * 50 + 96
        self.display.blit(locations.indicator_image, (225, location_y))
        self.screen.blit(self.display, (0, 0))
        pygame.display.update()

    def draw_game_graphics(self, game_graphics):
        game_graphics_textures = game_graphics.board_textures
        for y, row in enumerate(game_graphics.game_map):
            for x, tile in enumerate(row):
                if tile != '-1':
                    self.display.blit(game_graphics_textures[f"{tile}"], (x * 16, y * 16))

    def draw_gate(self, gate):
        self.display.blit(gate.gate_image, gate.gate_location)
        for location in gate.plates_locations:
            self.display.blit(gate.plate_image, location)

    def draw_yurta(self, yurtas):
        for yurta in yurtas:
            self.display.blit(yurta.placeholder, yurta.yurta_location)
            self.display.blit(yurta.yurta_door_image, yurta.yurta_door_location)
            self.display.blit(yurta.open_yurta_image, yurta.yurta_location)

    def draw_player(self, players):
        for player in players:
            player_image = self._get_player_image(player)
            self.display.blit(player_image, (player.rect.x, player.rect.y))

    def _get_player_image(self, player):
        if player.moving_right:
            return player.image
        elif player.moving_left:
            return pygame.transform.flip(player.image, True, False)
        elif player.last_move=="right":
            return player.image
        else: 
            return pygame.transform.flip(player.image, True, False)

    def move_player(self, game_graphics, gate, players):
        for player in players:
            player.calc_movement()
            movement = player.get_movement()
            if(movement[0]>0):
                player.last_move = "right"
            elif(movement[0]<0):
                player.last_move = "left"
            collide_blocks = self._get_collide_blocks(game_graphics, gate)
            self._update_player_position(player, movement, collide_blocks)

    def _get_collide_blocks(self, game_graphics, gate):
        return game_graphics.collidable_blocks + gate.get_solid_blocks()

    def _update_player_position(self, player, movement, collide_blocks):
        collision_types = self._update_player_horizontal_position(player, movement, collide_blocks)
        self._update_player_vertical_position(player, movement, collide_blocks, collision_types)

    def _update_player_horizontal_position(self, player, movement, collide_blocks):
        collision_types = {'top': False, 'bottom': False, 'right': False, 'left': False}
        player.rect.x += movement[0]
        hit_list = self.collision_test(player.rect, collide_blocks)
        for tile in hit_list:
            if movement[0] > 0:
                player.rect.right = tile.left
                collision_types['right'] = True
            elif movement[0] < 0:
                player.rect.left = tile.right
                collision_types['left'] = True
        return collision_types

    def _update_player_vertical_position(self, player, movement, collide_blocks, collision_types):
        player.rect.y += movement[1]
        hit_list = self.collision_test(player.rect, collide_blocks)
        for tile in hit_list:
            if movement[1] > 0:
                player.rect.bottom = tile.top
                collision_types['bottom'] = True
            elif movement[1] < 0:
                player.rect.top = tile.bottom
                collision_types['top'] = True
        self._handle_vertical_collisions(player, collision_types)

    def _handle_vertical_collisions(self, player, collision_types):
        if collision_types['bottom']:
            player.y_velocity = 0
            player.time_in_air = 0
        else:
            player.time_in_air += 1
        if collision_types['top']:
            player.y_velocity = 0

    def check_for_lose(self, game_graphics, players):
        for player in players:
            if self.collision_test(player.rect, game_graphics.water_blocks):
                player.unactivate()

    def check_for_gate_press(self, gate, players):
        plate_collisions = [self.collision_test(player.rect, gate.plates) for player in players]
        gate.plate_is_pressed = any(plate_collisions)
        gate.try_open_gate()

    def check_for_yurta_open(self, yurta, player):
        yurta.player_at_yurta = bool(self.collision_test(player.rect, [yurta.yurta_door_rect]))
        yurta.try_open_yurta()

    def location_is_done(self, yurtas):
        return all([yurta.yurta_open for yurta in yurtas])

    def collision_test(self, rect, tiles):
        return [tile for tile in tiles if rect.colliderect(tile)]
