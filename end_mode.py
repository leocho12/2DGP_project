# python
from pico2d import *
import time
import game_framework
import game_world


font = None

# 엔딩 시점의 고정된 시간 문자열을 저장할 변수
_saved_timestr = None

def init():
    global font, badge_left, badge_right, _saved_timestr
    try:
        if font is None:
            font = load_font('ENCR10B.TTF', 28)
    except Exception:
        font = None

    # 엔딩 모드로 진입한 시점의 플레이 시간을 캡처하여 고정한다 (타이머 멈춤 효과)
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
        pass


    cw = get_canvas_width()
    ch = get_canvas_height()


    # 통계 문자열 준비 (저장된 고정 시간 사용)
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

    # 텍스트 그리기 (중앙 정렬)
    line_height = 36
    start_y = ch // 2 + (len(lines)//2) * line_height
    x = cw // 2

    for i, line in enumerate(lines):
        y = start_y - i * line_height
        if font:
            try:
                font.draw(x - len(line) * 8, y, line, (255, 255, 255))
            except Exception:
                pass
        else:
            # 폴백: 간단한 사각형 및 텍스트 위치 표시
            draw_rectangle(x - 200, y - 14, x + 200, y + 14)


    update_canvas()

def finish():
    global font, badge_left, badge_right, _saved_timestr
    font = None
    badge_left = None
    badge_right = None
    _saved_timestr = None

def pause(): pass
def resume(): pass
