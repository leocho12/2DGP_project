import random
from pico2d import *

import game_framework
import game_world

from duck import Duck
from map import Map
from gun import Gun

ducks = []
gun=None

def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            for duck in ducks:
                duck.handle_event(event)  # Duck 클래스가 아닌 duck 인스턴스의 메서드 호출
            if gun:
                gun.handle_event(event)


def init():
    global ducks,gun

    game_map = Map()
    game_world.add_object(game_map, 0)

    NUM_DUCK=5
    for _ in range(NUM_DUCK):
        duck = Duck()
        ducks.append(duck)
        game_world.add_object(duck, 1)

    gun=Gun()
    game_world.add_object(gun,2)


def update():
    game_world.update()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def finish():
    global gun
    game_world.clear()
    ducks.clear()
    gun=None

def pause(): pass
def resume(): pass