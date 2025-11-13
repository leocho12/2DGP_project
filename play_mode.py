import random
from pico2d import *

import game_framework
import game_world

from duck import Duck
from map import Background, Grass
from gun import Gun


ducks = []
gun = None
grass = None


def handle_events():
    event_list = get_events()
    for event in event_list:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        else:
            for duck in ducks:
                duck.handle_event(event)  # Duck 인스턴스의 메서드 호출
            if gun:
                gun.handle_event(event)


def init():
    global ducks, gun, grass

    # Background (레이어 0)
    background = Background()
    game_world.add_object(background, game_world.LAYER_BACKGROUND)

    # Ducks (레이어 1)
    NUM_DUCK = 5
    for _ in range(NUM_DUCK):
        duck = Duck()
        ducks.append(duck)
        game_world.add_object(duck, game_world.LAYER_FOREGROUND)

    # Grass (레이어 2) - 앞쪽 레이어로 추가하여 오리가 풀보다 뒤에 나오도록 함
    grass = Grass()
    game_world.add_object(grass, game_world.LAYER_GRASS)

    # Gun (레이어 3 / UI)
    gun = Gun()
    game_world.add_object(gun, game_world.LAYER_UI)


def update():
    game_world.update()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def finish():
    global gun, grass
    game_world.clear()
    ducks.clear()
    gun = None
    grass = None


def pause(): pass
def resume(): pass