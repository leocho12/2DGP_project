from pico2d import load_image, get_canvas_width, get_canvas_height, draw_rectangle
import game_framework
import game_world

class DamageOverlay:
    image = None

    def __init__(self, duration=0.4):
        if DamageOverlay.image is None:
            try:
                DamageOverlay.image = load_image('demage.png')
            except Exception:
                DamageOverlay.image = None
        self.duration = duration
        self.timer = duration

    def update(self):
        # 시간 경과 후 자동 제거
        self.timer -= game_framework.frame_time
        if self.timer <= 0.0:
            try:
                game_world.remove_object(self)
            except Exception:
                pass

    def draw(self):
        w = get_canvas_width()
        h = get_canvas_height()
        if DamageOverlay.image:
            # 화면 전체에 이미지 스케일로 그림
            DamageOverlay.image.draw(w // 2, h // 2, w, h)
        else:
            # 이미지 없을 때 간단한 빨간 사각형(대체)
            draw_rectangle(0, 0, w, h)
