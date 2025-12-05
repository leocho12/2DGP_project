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
import stage_choice_mode


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
    # 점수 기준(300점 단위)을 넘었는지 확인하고, 넘었다면 다음 웨이브가 스폰되기 전에 속도 배수 적용 및 플레이어 선택 모드로 전환
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
        # 플레이어가 선택하도록 stage_choice_mode로 전환
        try:
            stage_choice_mode.pending_increases = increases
            game_framework.push_mode(stage_choice_mode)
        except Exception:
            # 실패 시 폴백으로 자동 회복 적용
            try:
                if gun is not None:
                    old_hp = gun.hp
                    gun.hp = min(gun.max_hp, gun.hp + increases)
                    print(f'[play_mode] (fallback) Gun HP restored {old_hp} -> {gun.hp}')
            except Exception:
                pass
        # 선택 모드에서 돌아올 때까지 웨이브 생성 중단
        return

    # 실제 웨이브 스폰
    for _ in range(WAVE_SIZE):
        duck = Duck()
        ducks.append(duck)
        game_world.add_object(duck, game_world.LAYER_FOREGROUND)
    for _ in range(KAMIKAZE_PER_WAVE):
        kamikaze = Kamikaze()
        kamikazes.append(kamikaze)
        # 변경: 자폭 오리는 풀보다 앞에(더 위에) 그려지도록 UI 레이어에 추가
        game_world.add_object(kamikaze, game_world.LAYER_UI)

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

    # 변경: 자폭오리는 이제 UI 레이어에 있을 수 있으므로 모든 레이어를 스캔하여 Kamikaze 인스턴스 수집
    current_kamikazes = [o for layer in game_world.world for o in layer if isinstance(o, Kamikaze)]
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
