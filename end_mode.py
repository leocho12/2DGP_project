# python
from pico2d import *
import time
import game_framework
import game_world
import title_mode

font = None

def init():
    global font
    if font is None:
        try:
            font = load_font('ENCR10B.TTF', 28)
        except Exception:
            font = None
    # 엔딩 모드 진입 시 타이머 고정
    try:
        if getattr(game_world, 'start_time', None) is not None:
            # 이미 end_time이 설정되어 있지 않다면 현재 시각으로 설정
            if getattr(game_world, 'end_time', None) is None:
                game_world.end_time = time.time()
    except Exception:
        game_world.end_time = time.time()

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
    # 고정된 end_time(있다면)으로 경과 시간 계산
    score = getattr(game_world, 'score', 0)
    ducks = getattr(game_world, 'ducks_killed', 0)
    bullets = getattr(game_world, 'bullets_fired', 0)
    start = getattr(game_world, 'start_time', None)
    end = getattr(game_world, 'end_time', None)

    if start is not None and end is not None:
        elapsed = int(end - start)
    elif start is not None:
        elapsed = int(time.time() - start)
    else:
        elapsed = 0

    mins = elapsed // 60
    secs = elapsed % 60
    timestr = f"{mins:02d}:{secs:02d}"

    w = get_canvas_width()
    h = get_canvas_height()

    lines = [
        f"Score: {score}",
        f"Play Time: {timestr}",
        f"Ducks Killed: {ducks}",
        f"Bullets Fired: {bullets}",
        "",
        "Press ESC to quit"
    ]

    y = h // 2 + 80
    for line in lines:
        if font:
            try:
                font.draw(w//2 - len(line)*14//2, y, line, (255,255,255))
            except Exception:
                pass
        else:
            # 폰트가 없으면 간단한 대체 표시
            from pico2d import draw_rectangle, draw_text
            try:
                # draw_text는 없을 수 있으므로 안전하게 사각형만 그림
                draw_rectangle(w//2 - 200, y - 16, w//2 + 200, y + 16)
            except Exception:
                pass
        y -= 40

    update_canvas()

def finish():
    # 엔딩 종료 시 고정된 end_time 제거하여 다음 플레이에서 타이머 정상 작동
    try:
        game_world.end_time = None
    except Exception:
        pass

def pause():
    pass

def resume():
    pass
