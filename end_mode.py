# python
from pico2d import *
import time
import game_framework
import game_world
import title_mode

font = None


def init():
    global font,back_sound
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

    w = get_canvas_width()
    h = get_canvas_height()

    # 검은 배경으로 전체 캔버스 채우기 (set_color는 0.0~1.0 값을 사용)
    try:
        set_color(0.0, 0.0, 0.0, 1.0)  # RGBA (0..1)
        # draw_rectangle는 경우에 따라 윤곽만 그릴 수 있으므로, 안전하게 사각형을 채우려면
        # draw_rectangle(0,0,w,h)로 충분한 경우가 많음. 예외를 대비해 try/except 처리.
        draw_rectangle(0, 0, w, h)
    except Exception:
        # 실패해도 무시(격자가 보이는 문제를 막기 위해 clear_canvas() 이후
        # 반드시 뭔가 그려야 한다면 이미지로 대체하거나 별도 처리 필요)
        pass
    finally:
        # 텍스트는 흰색으로 그리기 위해 색 복구
        try:
            set_color(1.0, 1.0, 1.0, 1.0)
        except Exception:
            pass

    # 이후 기존의 텍스트 출력 코드를 그대로 사용
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
                # font.draw의 색 인자는 (r,g,b) 0..255를 허용하므로 흰색 사용
                font.draw(w//2 - len(line)*14//2, y, line, (255,255,255))
            except Exception:
                pass
        else:
            try:
                # 폰트가 없을 때는 흰색 사각형(대체)
                set_color(1.0, 1.0, 1.0, 1.0)
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
