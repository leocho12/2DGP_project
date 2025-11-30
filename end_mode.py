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


def handle_events():
    events = get_events()
    for e in events:
        if e.type == SDL_QUIT:
            game_framework.quit()
        elif e.type == SDL_KEYDOWN:
            if getattr(e, 'key', None) == SDLK_SPACE:
                game_framework.change_mode(title_mode)
            elif getattr(e, 'key', None) == SDLK_ESCAPE:
                game_framework.quit()


def update():
    pass


def draw():
    clear_canvas()
    score = getattr(game_world, 'score', 0)
    ducks = getattr(game_world, 'ducks_killed', 0)
    bullets = getattr(game_world, 'bullets_fired', 0)
    start = getattr(game_world, 'start_time', None)
    if start:
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
        "Press SPACE to return to Title, ESC to quit"
    ]

    y = h // 2 + 80
    for line in lines:
        if font:
            try:
                # center text approximately
                font.draw(w//2 - len(line)*8, y, line, (255,255,255))
            except Exception:
                pass
        else:
            from pico2d import draw_rectangle
            draw_rectangle(w//2 - 200, y - 10, w//2 + 200, y + 20)
        y -= 40

    update_canvas()


def pause(): pass

def resume(): pass

def finish(): pass

