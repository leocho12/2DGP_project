from pico2d import *
import game_framework
import play_mode

image=None

def init():
    global image
    try:
        image=load_image('title.png')
    except Exception:
        image=None

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            # 스페이스바 누르면 play_mode로 전환
            if getattr(event, 'key', None) == SDLK_SPACE:
                game_framework.change_mode(play_mode)
            # ESC 종료
            elif getattr(event, 'key', None) == SDLK_ESCAPE:
                game_framework.quit()

def update():
    pass

def update():
    pass

def draw():
    clear_canvas()
    if image:
        image.draw(get_canvas_width() // 2, get_canvas_height() // 2)
    update_canvas()

def finish():
    global image
    image = None

def pause():
    pass

def resume():
    pass