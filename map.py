from pico2d import load_image, get_canvas_width, get_canvas_height


class Background:
    def __init__(self):
        # ground
        self.ground_image = load_image('ground.png')
        self.cw = get_canvas_width()
        self.h = 200

        # sky
        self.sky_image = load_image('sky.png')
        self.sky_tiles = []
        self.sky_tile_width = self.sky_image.w

        # 화면을 덮을 하늘 타일 개수 계산 (여유분 포함)
        screen_width = get_canvas_width()
        tile_count = (screen_width // self.sky_tile_width) + 3
        # 하늘 타일 위치 초기화
        for i in range(tile_count):
            x = i * self.sky_tile_width
            self.sky_tiles.append(x)

    def draw(self):
        # sky
        for x in self.sky_tiles:
            self.sky_image.draw(x + self.sky_tile_width // 2,
                                get_canvas_height() - self.sky_image.h // 2)
        # ground
        self.ground_image.draw(self.cw // 2, self.h // 2, self.cw, self.h)

    def update(self):
        pass


class Grass:
    """
    grass_items 항목 구조:
      {
        'img': <pico2d.Image>,
        'x': float,          # 화면상의 x 좌표 (중심 기준)
        'y': float,          # 기준 y 좌표: anchor == 'bottom'이면 바닥(y), 'center'이면 중심(y)
        'scale': float,
        'anchor': 'bottom'|'center'
      }
    """

    def __init__(self):
        self.grass_items = []
        # 기본 예시 아이템들
        try:
            img_left = load_image('grass_left.png')
        except Exception:
            img_left = None
        try:
            img_center = load_image('grass_center.png')
        except Exception:
            img_center = None
        try:
            img_right = load_image('grass_right.png')
        except Exception:
            img_right = None

        if img_left:
            self.add_grass(img_left, 100, 60, 1.6, anchor='bottom')
        if img_center:
            self.add_grass(img_center, 400, 60, 1.0, anchor='bottom')
        if img_right:
            self.add_grass(img_right, 700, 60, 1.0, anchor='bottom')

    # API: 아이템 추가
    def add_grass(self, image, x, y, scale=1.0, anchor='bottom'):
        item = {'img': image, 'x': x, 'y': y, 'scale': scale, 'anchor': anchor}
        self.grass_items.append(item)
        return len(self.grass_items) - 1  # 추가된 인덱스 반환

    # API: 위치 조정 (인덱스 사용)
    def set_grass_position(self, index, x=None, y=None):
        if 0 <= index < len(self.grass_items):
            if x is not None:
                self.grass_items[index]['x'] = x
            if y is not None:
                self.grass_items[index]['y'] = y

    # API: 스케일 조정
    def set_grass_scale(self, index, scale):
        if 0 <= index < len(self.grass_items):
            self.grass_items[index]['scale'] = scale

    # API: 제거
    def remove_grass(self, index):
        if 0 <= index < len(self.grass_items):
            self.grass_items.pop(index)

    def draw(self):
        for item in self.grass_items:
            img = item['img']
            if img is None:
                continue
            x = item['x']
            y = item['y']
            scale = item.get('scale', 1.0)
            anchor = item.get('anchor', 'bottom')

            orig_w = getattr(img, 'w', 80)
            orig_h = getattr(img, 'h', 80)

            new_w = orig_w * scale
            new_h = orig_h * scale

            if anchor == 'bottom':
                # 저장된 y를 '바닥(y)'로 보고 중심 Y로 변환
                new_center_y = y + new_h / 2.0
            else:
                # 'center'라면 y는 중심 Y
                new_center_y = y

            img.draw(x, new_center_y, new_w, new_h)

    def update(self):
        pass


# 호환성을 위해 Map 클래스를 유지하되 내부에 Background와 Grass를 합친 간단한 래퍼로 제공
class Map:
    def __init__(self):
        self.background = Background()
        self.grass = Grass()

    def draw(self):
        self.background.draw()
        self.grass.draw()

    def update(self):
        self.background.update()
        self.grass.update()
