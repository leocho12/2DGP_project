# python
import random
from pico2d import *
import time

import game_framework
import game_world

from duck import Duck
from map import Background, Grass
from gun import Gun
from kamikaze import Kamikaze
from scoreBoard import ScoreBoard


ducks = []
kamikazes=[]
gun = None
grass = None
scoreboard = None

WAVE_SIZE=2 # 웨이브당 오리 수
KAMIKAZE_PER_WAVE=1 # 웨이브당 자폭 오리 수

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

def spawn_wave():
    # 점수 기준(300점 단위)을 넘었는지 확인하고, 넘었다면 다음 웨이브가 스폰되기 전에 속도 배수와 플레이어 HP 회복을 적용
    increases = 0
    try:
        while game_world.score >= game_world.next_speed_threshold:
            game_world.speed_multiplier *= game_world.speed_increment_factor
            game_world.next_speed_threshold += 300
            increases += 1
    except Exception:
        increases = 0

    if increases > 0:
        print(f'[play_mode] Applied speed increase x{increases}, multiplier={game_world.speed_multiplier:.3f}, next_threshold={game_world.next_speed_threshold}')
        # 플레이어(Gun)의 HP를 증가시킴 (gun은 전역 변수)
        try:
            if gun is not None:
                old_hp = gun.hp
                gun.hp = min(gun.max_hp, gun.hp + increases)
                print(f'[play_mode] Gun HP restored {old_hp} -> {gun.hp}')
        except Exception:
            pass

    # 실제 웨이브 스폰 (속도 적용은 위에서 이미 반영되므로, 새로 생성된 오브젝트는 다음 프레임부터 증가된 배수를 사용함)
    for _ in range(WAVE_SIZE):
        duck = Duck()
        ducks.append(duck)
        game_world.add_object(duck, game_world.LAYER_FOREGROUND)
    for _ in range(KAMIKAZE_PER_WAVE):
        kamikaze = Kamikaze()
        kamikazes.append(kamikaze)
        # Kamikaze는 오리와 같은 전경 레이어에 추가하여 일관성 유지
        game_world.add_object(kamikaze, game_world.LAYER_FOREGROUND)

def init():
    global ducks, gun, grass, kamikazes, scoreboard

    # Background (레이어 0)
    background = Background()
    game_world.add_object(background, game_world.LAYER_BACKGROUND)

    # Grass (레이어 2)
    grass = Grass()
    game_world.add_object(grass, game_world.LAYER_GRASS)

    # Gun (레이어 3 / UI) — 플레이어는 먼저 생성되어야 함
    gun = Gun()
    game_world.add_object(gun, game_world.LAYER_UI)

    # ScoreBoard (우측 상단) - UI 레이어
    scoreboard = ScoreBoard()
    game_world.add_object(scoreboard, game_world.LAYER_UI)

    # 플레이 시작 시간 기록
    try:
        game_world.start_time = time.time()
    except Exception:
        game_world.start_time = None

    # 오브젝트(오리/자폭) 스폰은 플레이어가 준비된 이후에 수행
    spawn_wave()


def update():
    global ducks, kamikazes
    game_world.update()

    current_ducks=[o for o in game_world.world[game_world.LAYER_FOREGROUND] if isinstance(o,Duck)]
    ducks=current_ducks

    current_kamikazes = [o for o in game_world.world[game_world.LAYER_FOREGROUND] if isinstance(o, Kamikaze)]
    kamikazes = current_kamikazes

    if len(ducks) == 0 and len(kamikazes) == 0:
        spawn_wave()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def finish():
    global gun, grass, scoreboard
    game_world.clear()
    ducks.clear()
    kamikazes.clear()
    gun = None
    grass = None
    scoreboard = None


def pause(): pass
def resume(): pass
