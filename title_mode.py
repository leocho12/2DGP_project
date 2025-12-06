# python
from pico2d import *
import game_framework
import play_mode
import threading

image = None
title_font = None
title_font_size = 72
title_margin_top = 140
click_sound = None
instr_font = None
instr_font_size = 28
instr_text = "Press SPACE to Start"

# 백그라운드 사운드 관련 (비동기 로드)
back_sound = None
_back_sound_loaded = False
_back_sound_played = False

def _load_back_sound():
    global back_sound, _back_sound_loaded
    try:
        s = load_wav('fuba.mp3')
        s.set_volume(30)
        back_sound = s
    except Exception:
        back_sound = None
    _back_sound_loaded = True

def init():
    global image, title_font, click_sound, _back_sound_loaded, _back_sound_played, instr_font
    try:
        image = load_image('title.png')
    except Exception:
        image = None

    if title_font is None:
        try:
            title_font = load_font('ENCR10B.TTF', title_font_size)
        except Exception:
            title_font = None

    if instr_font is None:
        try:
            instr_font = load_font('ENCR10B.TTF', instr_font_size)
        except Exception:
            instr_font = None

    if click_sound is None:
        try:
            click_sound = load_wav('duckclick.mp3')
            click_sound.set_volume(1000)
        except Exception:
            click_sound = None

    # 백그라운드 사운드는 별 스레드에서 비동기로 로드하여 init()이 빠르게 반환되게 함
    _back_sound_loaded = False
    _back_sound_played = False
    t = threading.Thread(target=_load_back_sound, daemon=True)
    t.start()

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
    global _back_sound_loaded, _back_sound_played, back_sound
    # 로드 완료되었고 아직 재생하지 않았다면 재생(무한 반복 시도)
    if _back_sound_loaded and not _back_sound_played:
        try:
            if back_sound:
                try:
                    # 우선 repeat_play() 시도 (pico2d 구현마다 메서드명이 다를 수 있으므로 안전하게 시도)
                    back_sound.repeat_play()
                except Exception:
                    try:
                        # play(-1)로 무한 반복 시도
                        back_sound.play(-1)
                    except Exception:
                        # 마지막으로 일반 play() 호출 (반복 불가 시 한 번만 재생)
                        try:
                            back_sound.play()
                        except Exception:
                            pass
        except Exception:
            pass
        _back_sound_played = True

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

    instr_y = 40
    if instr_font:
        try:
            approx_w = instr_font_size * 0.6
            instr_x = cw // 2 - (len(instr_text) * approx_w) / 2
            instr_font.draw(instr_x, instr_y, instr_text, (220, 220, 220))
        except Exception:
            pass
    else:
        # 폰트 없을 때 대체 표시
        from pico2d import draw_rectangle
        draw_rectangle(cw // 2 - 200, instr_y - 14, cw // 2 + 200, instr_y + 14)

    update_canvas()

def finish():
    global image, title_font
    image = None
    title_font = None

def pause():
    pass

def resume():
    pass
