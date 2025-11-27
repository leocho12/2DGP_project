# File: `scoreboard.py`
from pico2d import load_font, get_canvas_width, get_canvas_height
import game_world

class ScoreBoard:
    font = None

    def __init__(self, font_size=24, margin=12):
        if ScoreBoard.font is None:
            try:
                ScoreBoard.font = load_font('ENCR10B.TTF', font_size)
            except Exception:
                ScoreBoard.font = None
        self.font_size = font_size
        self.margin = margin

    def update(self):
        # UI 업데이트 필요 없음 (점수는 외부에서 갱신됨)
        pass

    def draw(self):
        text = f"Score: {game_world.score}"
        # 대충의 문자 너비 추정으로 우측 정렬 (안정성 위해 고정 여백 사용)
        approx_char_w = self.font_size * 0.6
        text_w = len(text) * approx_char_w
        x = get_canvas_width() - 10 - text_w
        y = get_canvas_height() - self.margin - self.font_size
        if ScoreBoard.font:
            try:
                ScoreBoard.font.draw(x, y, text)
            except Exception:
                pass
        else:
            # 폰트 로드 실패 시 간단한 대체 표시 (사각형)
            from pico2d import draw_rectangle
            draw_rectangle(x - 4, y - 4, x + text_w + 4, y + self.font_size + 4)
