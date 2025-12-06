# python
from pico2d import *
import time
import game_framework
import game_world

font = None
_saved_timestr = None

def init():
    global font, _saved_timestr
    try:
        if font is None:
            font = load_font('ENCR10B.TTF', 28)
    except Exception:
        font = None

    # 엔딩 진입 시점의 플레이 시간 고정(타이머 멈춤 효과)
    try:
        start_time = getattr(game_world, 'start_time', None)
        if start_time:
            elapsed = int(time.time() - start_time)
            minutes = elapsed // 60
            seconds = elapsed % 60
            _saved_timestr = f"{minutes:02d}:{seconds:02d}"
        else:
            _saved_timestr = "N/A"
    except Exception:
        _saved_timestr = "N/A"

def handle_events():
    events = get_events()
    for e in events:
        if e.type == SDL_QUIT:
            game_framework.quit()
        elif e.type == SDL_KEYDOWN:
            if getattr(e, 'key', None) == SDLK_ESCAPE:
                game_framework.quit()

def update():
    pass

def draw():
    clear_canvas()

    # Background / Grass 레이어를 안전하게 그려서 플레이 화면을 배경으로 재사용
    try:
        for o in list(game_world.world[game_world.LAYER_BACKGROUND]):
            try:
                o.draw()
            except Exception:
                pass
        for o in list(game_world.world[game_world.LAYER_GRASS]):
            try:
                o.draw()
            except Exception:
                pass
    except Exception:
        # game_world 구성이 준비되지 않았으면 무시
        pass

    cw = get_canvas_width()
    ch = get_canvas_height()

    score = getattr(game_world, 'score', 0)
    timestr = _saved_timestr if _saved_timestr is not None else "N/A"
    ducks = getattr(game_world, 'ducks_killed', 0)
    bullets = getattr(game_world, 'bullets_fired', 0)

    lines = [
        f"Score: {score}",
        f"Play Time: {timestr}",
        f"Ducks Killed: {ducks}",
        f"Bullets Fired: {bullets}",
        "",
        "Press ESC to quit"
    ]

    line_height = 36
    start_y = ch // 2 + (len(lines)//2) * line_height
    x = cw // 2

    for i, line in enumerate(lines):
        y = start_y - i * line_height
        if font:
            try:
                # 폰트 draw는 좌상단 기준이므로 텍스트 너비를 대략 계산해 중앙정렬
                approx_char_w = 14
                font.draw(x - len(line) * approx_char_w // 2, y, line, (255, 255, 255))
            except Exception:
                pass
        else:
            # 폰트 실패 시 간단한 폴백 표시
            draw_rectangle(x - 200, y - 14, x + 200, y + 14)

    update_canvas()

def finish():
    global font, _saved_timestr
    font = None
    _saved_timestr = None

def pause(): pass
def resume(): pass
