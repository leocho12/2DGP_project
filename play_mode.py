import random
from pico2d import *

import game_framework
import game_world

from duck import Duck
from map import Background, Grass
from gun import Gun
from kamikaze import Kamikaze


ducks = []
kamikazes=[]
gun = None
grass = None

WAVE_SIZE=2

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
    global ducks, gun, grass, kamikazes

    # Background (레이어 0)
    background = Background()
    game_world.add_object(background, game_world.LAYER_BACKGROUND)

    # Ducks (레이어 1)
    for _ in range(WAVE_SIZE):
        duck = Duck()
        ducks.append(duck)
        game_world.add_object(duck, game_world.LAYER_FOREGROUND)
    # Kamikazes (레이어 1)
    for _ in range(WAVE_SIZE):
        kamikaze = Kamikaze()
        kamikazes.append(kamikaze)
        game_world.add_object(kamikaze, game_world.LAYER_FOREGROUND)

    # Grass (레이어 2)
    grass = Grass()
    game_world.add_object(grass, game_world.LAYER_GRASS)

    # Gun (레이어 3 / UI)
    gun = Gun()
    game_world.add_object(gun, game_world.LAYER_UI)


def update():
    global ducks, kamikazes
    game_world.update()

    current_ducks=[o for o in game_world.world[game_world.LAYER_FOREGROUND] if isinstance(o,Duck)]
    ducks=current_ducks

    if len(ducks)==0:
        for _ in range(WAVE_SIZE):
            duck = Duck()
            ducks.append(duck)
            game_world.add_object(duck, game_world.LAYER_FOREGROUND)

    if len(kamikazes)==0:
        for _ in range(WAVE_SIZE):
            kamikaze = Kamikaze()
            kamikazes.append(kamikaze)
            game_world.add_object(kamikaze, game_world.LAYER_FOREGROUND)

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