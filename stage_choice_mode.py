from pico2d import *
import game_framework
import game_world

font = None
pending_increases = 0  # play_mode에서 설정해서 전달
_remaining = 0
click_sound = None

def init():
    global font, _remaining, pending_increases
    try:
        if font is None:
            font = load_font('ENCR10B.TTF', 28)
    except Exception:
        font = None

    global click_sound
    if click_sound is None:
        try:
            click_sound = load_wav('duckclick.mp3')
            try:
                click_sound.set_volume(1000)
            except Exception:
                pass
        except Exception:
            click_sound = None

    _remaining = pending_increases
    pending_increases = 0

    # 안전장치: 증가가 없으면 즉시 되돌아감
    if _remaining <= 0:
        game_framework.pop_mode()


def handle_events():
    global _remaining
    events = get_events()
    for e in events:
        if e.type == SDL_QUIT:
            game_framework.quit()
        elif e.type == SDL_KEYDOWN:
            if e.key == SDLK_1:
                apply_choice('damage')
            elif e.key == SDLK_2:
                apply_choice('heal')
            elif e.key == SDLK_ESCAPE:
                game_framework.pop_mode()


def find_gun():
    try:
        for o in game_world.world[game_world.LAYER_UI]:
            if hasattr(o, 'hp') and hasattr(o, 'max_hp'):
                return o
    except Exception:
        pass
    return None


def apply_choice(choice):
    global _remaining
    gun = find_gun()
    if choice == 'damage':
        if gun is not None:
            try:
                gun.damage = getattr(gun, 'damage', 1) + 1
            except Exception:
                pass
    elif choice == 'heal':
        if gun is not None:
            try:
                gun.hp = min(gun.max_hp, gun.hp + 1)
            except Exception:
                pass
    # 클릭 사운드 재생
    try:
        if click_sound:
            try:
                click_sound.play()
            except Exception:
                pass
    except Exception:
        pass
    _remaining -= 1
    if _remaining <= 0:
        game_framework.pop_mode()


def update():
    pass


def draw():
    clear_canvas()
    w = get_canvas_width()
    h = get_canvas_height()

    # play_mode에서 사용하는 Background와 Grass를 그대로 그리기
    try:
        # Background 레이어 그리기
        for o in list(game_world.world[game_world.LAYER_BACKGROUND]):
            try:
                o.draw()
            except Exception:
                pass
        # Grass 레이어 그리기
        for o in list(game_world.world[game_world.LAYER_GRASS]):
            try:
                o.draw()
            except Exception:
                pass
    except Exception:
        # game_world 구성이 아직 준비되지 않았으면 무시
        pass

    # (배경 채우기 대신 텍스트만 오버레이)

    title = "Stage Up! Choose Upgrade"
    opt1 = "1: Increase Gun Damage (+1)"
    opt2 = "2: Restore 1 HP (up to max)"
    remain = f"Remaining choices: {_remaining}"

    y = h // 2 + 60
    if font:
        font.draw(w//2 - 200, y, title, (255,255,255))
        font.draw(w//2 - 200, y - 48, opt1, (200,200,255))
        font.draw(w//2 - 200, y - 96, opt2, (200,255,200))
        font.draw(w//2 - 200, y - 150, remain, (255,255,0))
    else:
        draw_rectangle(w//2 - 250, y + 20, w//2 + 250, y - 180)

    update_canvas()


def finish():
    pass


def pause():
    pass


def resume():
    pass
