world = [[], [], [], []]  # 게임 내 객체들을 담는 리스트

# 렌더 순서를 Background -> Grass -> Foreground -> UI 로 변경
# (이전에는 Foreground가 1, Grass가 2라서 풀이 오리 위에 그려졌음)
LAYER_BACKGROUND = 0    # 배경 레이어
LAYER_GRASS = 1         # 풀 레이어 (배경 다음)
LAYER_FOREGROUND = 2    # 오리 레이어 (풀이 뒤)
LAYER_UI = 3            # UI 레이어

# 게임 통계
score = 0

# 점수에 따른 속도 보정 관련
speed_multiplier = 1.0
next_speed_threshold = 300
# 증가 비율(예: 1.1 -> 10% 증가)
speed_increment_factor = 1.10

# 플레이 통계
start_time = None
ducks_killed = 0
bullets_fired = 0


def add_object(o, depth=0):
    world[depth].append(o)


def add_objects(ol, depth=0):
    world[depth] += ol


def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            return
    raise ValueError('Cannot delete non existing object')


def update():
    # 게임 오브젝트들 업데이트만 수행합니다.
    for layer in world:
        for o in list(layer):
            o.update()


def render():
    for layer in world:
        for o in list(layer):
            o.draw()


def clear():
    global world

    for layer in world:
        layer.clear()