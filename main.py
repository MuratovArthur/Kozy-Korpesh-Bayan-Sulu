import sys
import pygame
import json

from pygame.locals import *
from game_engine import GameEngine
from players import Player
from controller import Controller
from gate import Gate
from yurts import Yurta
from location_screen import LocationScreen
from landing_page import LandingPage
from game_graphics import GameGraphics

def pause_game(kozy_korpesh, bayan_sulu):
    kozy_korpesh.stop_player()
    bayan_sulu.stop_player()
    pause_image = pygame.image.load('data/additional_images/pause.png')
    game.screen.blit(pause_image, (0, 0))

    while True:
        pygame.display.update()
        events = pygame.event.get()
        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_SPACE:
                    return

def handle_events(location, game, kozy_korpesh, bayan_sulu, events):
    for event in events:
        if event.type == QUIT:
            close, save = save_message()
            if(close):
                if(save):
                    game.game_data[location]['kozy_korpesh'] = (kozy_korpesh.rect.x, kozy_korpesh.rect.y)
                    game.game_data[location]['bayan-sulu'] = (bayan_sulu.rect.x, bayan_sulu.rect.y)
                else:
                    game.game_data[location] = game_data_default()[location]
                with open('data/saved_data.txt', 'w') as saved_data:
                    json.dump(game.game_data, saved_data)
                pygame.quit()
                sys.exit()

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                close, save = save_message()
                if(close):
                    if(save):
                        game.game_data[location]['kozy_korpesh'] = (kozy_korpesh.rect.x, kozy_korpesh.rect.y)
                        game.game_data[location]['bayan-sulu'] = (bayan_sulu.rect.x, bayan_sulu.rect.y)
                    else:
                        game.game_data[location] = game_data_default()[location]
                    with open('data/saved_data.txt', 'w') as saved_data:
                        json.dump(game.game_data, saved_data)
                    locations_screen()
            if event.key == K_SPACE:
                pause_game(kozy_korpesh, bayan_sulu)
        

def save_message():
    quit_screen_yes = pygame.image.load('data/screens/quit_screen_yes.png')
    quit_screen_no = pygame.image.load('data/screens/quit_screen_no.png')

    game.display.blit(quit_screen_yes, (0, 0))
    selected_button = "yes"
  
    while True:
        game.screen.blit(game.display, (0,0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN:
                if event.key == K_RIGHT:
                    selected_button = "no"
                elif event.key == K_LEFT:
                    selected_button = "yes"
                elif event.key == K_RETURN:
                    if selected_button == "yes":
                        return True, True
                    else:
                        return True, False
                elif event.key == K_ESCAPE:
                    return False, False

        if selected_button == "yes":
            game.display.blit(quit_screen_yes, (0, 0))
        else:
            game.display.blit(quit_screen_no, (0, 0))
            
def game_data_default():
    game_data = {
        'steppe': {
            'kozy_korpesh': (500, 48),
            'bayan-sulu': (16, 336),
            'gate': (365, 32),
            'plates': [(190, 168), (190, 168)],
            'yurta_l': (455, 0),
            'yurta_r': (350, 288)
        },
        'forest': {
            'kozy_korpesh': (16, 336),
            'bayan-sulu': (35, 336),
            'gate': (285, 128),
            'plates': [(210, 160), (460, 160)],
            'yurta_l': (48, 0),
            'yurta_r': (128, 0)
        }
    }
    return game_data

def saved_data():
    game_data = game_data_default()
    try:
        with open('data/saved_data.txt') as saved_data:
            game_data = json.load(saved_data)
    except:
        with open('data/saved_data.txt', 'w') as saved_data:
            json.dump(game_data, saved_data)
    return game_data


def draw_game(gate, yurta_group, player_group, game_graphics):
    game.display.blit(game_graphics.background, (0, 0))
    game.draw_game_graphics(game_graphics)
    game.draw_yurta(yurta_group)
    game.draw_player(player_group)
    game.draw_gate(gate)

def landing_page():
    landing_page = LandingPage()
    game.display.blit(landing_page.background, (0, 0))
    while True:
        game.screen.blit(game.display, (0,0))
        pygame.display.update()
        events = pygame.event.get()
        for event in events:
            if event.type == KEYDOWN:
                if event.key == K_RETURN:
                    locations_screen()
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


def locations_screen():
    location_screen = LocationScreen()
    location = game.select_location(location_screen)
    if location:
        run_game(location)
    else:
        landing_page()


def win_screen():
    win_screen = pygame.image.load('data/screens/win_screen.png')
    game.display.blit(win_screen, (0, 0))

    while True:
        game.screen.blit(game.display, (0,0))
        pygame.display.update()
        events = pygame.event.get()
        for event in events:
            if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        game.game_data = game_data_default()
                        locations_screen()
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()


def lose_screen(location):
    lose_screen = pygame.image.load('data/screens/lose_screen.png')
    game.display.blit(lose_screen, (0, 0))
    while True:
        game.screen.blit(game.display, (0,0))
        pygame.display.update()
        events = pygame.event.get()
        for event in events:
            if event.type == KEYDOWN:
                    if event.key == K_RETURN:
                        game.game_data = game_data_default()
                        run_game(location)
                    if event.key == K_ESCAPE:
                        game.game_data = game_data_default()
                        locations_screen()
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()

def run_game(location):
    game_graphics = GameGraphics(location)

    kozy_korpesh_location = game.game_data[location]['kozy_korpesh']
    bayan_sulu_location = game.game_data[location]['bayan-sulu']

    gate = Gate(game.game_data[location]["gate"], game.game_data[location]["plates"])

    yurta_l = Yurta(game.game_data[location]["yurta_l"])
    yurta_r = Yurta(game.game_data[location]["yurta_r"])
    yurtas = [yurta_l, yurta_r]

    kozy_korpesh = Player(kozy_korpesh_location, 'data/players/kozy-korpesh.png')
    bayan_sulu = Player(bayan_sulu_location, 'data/players/bayan-sulu-back.png')

    clock = pygame.time.Clock()

    while True:
        clock.tick(60)
        events = pygame.event.get()

        draw_game(gate, yurtas, [kozy_korpesh, bayan_sulu], game_graphics)

        kozy_korpesh_controller = Controller({"left": K_LEFT, "right": K_RIGHT, "up": K_UP, "down": K_DOWN})
        bayan_sulu_controller = Controller({"left": K_a, "right": K_d, "up": K_w, "down": K_s})
        kozy_korpesh_controller.control_player(events, kozy_korpesh)
        bayan_sulu_controller.control_player(events, bayan_sulu)

        game.move_player(game_graphics, gate, [kozy_korpesh, bayan_sulu])
        game.check_for_lose(game_graphics, [kozy_korpesh, bayan_sulu])
        game.check_for_gate_press(gate, [kozy_korpesh, bayan_sulu])
        game.check_for_yurta_open(yurta_r, kozy_korpesh)
        game.check_for_yurta_open(yurta_l, bayan_sulu)

        game.screen.blit(game.display, (0, 0))
        pygame.display.update()

        handle_events(location, game, kozy_korpesh, bayan_sulu, events)

        if bayan_sulu.is_inactive() or kozy_korpesh.is_inactive():
            lose_screen(location)

        if game.location_is_done(yurtas):
            win_screen()

pygame.init()
game = GameEngine(saved_data())
landing_page()