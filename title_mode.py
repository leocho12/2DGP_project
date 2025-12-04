# python
from pico2d import *
import game_framework
import play_mode

image = None
title_font = None
title_font_size = 72
title_margin_top = 140
click_sound = None

def init():
    global image, title_font, click_sound
    try:
        image = load_image('title.png')
    except Exception:
        image = None

    if title_font is None:
        try:
            title_font = load_font('ENCR10B.TTF', title_font_size)
        except Exception:
            title_font = None

    if click_sound is None:
        try:
            click_sound = load_wav('duckclick.mp3')
            click_sound.set_volume(1000)
        except Exception:
            click_sound = None

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN:
            # 스페이스바 누르면 play_mode로 전환
            if getattr(event, 'key', None) == SDLK_SPACE:
                game_framework.change_mode(play_mode)
                try:
                    if click_sound:
                        try:
                            click_sound.play()
                        except Exception:
                            pass
                except Exception:
                    pass
            # ESC 종료
            elif getattr(event, 'key', None) == SDLK_ESCAPE:
                game_framework.quit()

def update():
    pass

def draw():
    clear_canvas()
    cw = get_canvas_width()
    ch = get_canvas_height()

    if image:
        image.draw(cw // 2, ch // 2)

    # 타이틀 텍스트 그리기 (중앙 상단)
    text = "Duck Hunt"
    approx_char_w = title_font_size * 0.6
    text_w = len(text) * approx_char_w
    x = cw // 2 - text_w / 2
    y = ch - title_margin_top - title_font_size // 2

    if title_font:
        try:
            title_font.draw(x, y, text)
        except Exception:
            pass
    else:
        # 폰트 없을 때는 간단한 사각형으로 대체 표시
        from pico2d import draw_rectangle
        draw_rectangle(x - 8, y - 8, x + text_w + 8, y + title_font_size + 8)

    update_canvas()

def finish():
    global image, title_font
    image = None
    title_font = None

def pause():
    pass

def resume():
    pass
