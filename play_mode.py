import random
from pico2d import *

import game_framework
import game_world

from duck import Duck
from map import Map

duck = None

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            Duck.handle_event(event)

def init():
    global duck

    map = Map()
    game_world.add_object(map, 0)

    duck = Duck()
    game_world.add_object(duck, 1)


def update():
    game_world.update()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def finish():
    game_world.clear()

def pause(): pass
def resume(): pass