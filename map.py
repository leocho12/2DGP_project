from pico2d import load_image, get_canvas_width, get_canvas_height


class Map:
    def __init__(self):
        # grass
        self.image = load_image('ground.png')
        self.cw=get_canvas_width()
        self.ch=get_canvas_height()
        self.w=self.cw
        self.h=200
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
        # grass
        self.grass_items = []
        # 예시: 기존 이미지 3개를 아이템으로 추가
        self.add_grass(load_image('grass_left.png'), 100, 60, 1.6, anchor='bottom')
        self.add_grass(load_image('grass_center.png'), 400, 60, 1.0, anchor='bottom')
        self.add_grass(load_image('grass_right.png'), 700, 60, 1.0, anchor='bottom')
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
        # sky
        for x in self.sky_tiles:
            self.sky_image.draw(x + self.sky_tile_width // 2,
                              get_canvas_height() - self.sky_image.h // 2)
        # ground
        self.image.draw(self.cw//2, self.h//2, self.w, self.h)
        # grass
        for item in self.grass_items:
            img = item['img']
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
