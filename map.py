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
        # grass
        self.grass_images = [
            load_image('grass_left.png'),
            load_image('grass_center.png'),
            load_image('grass_right.png')
        ]
        self.grass_positions = [
            (100, 60),  # 왼쪽 잔디
            (400, 60),  # 중앙 잔디
            (700, 60)  # 오른쪽 잔디
        ]
        self.grass_scales = [
            1.6,  # 왼쪽 잔디를 160% 크기로 표시
            1.0,
            1.0
        ]

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
        self.image.draw(self.cw//2, self.h//2, self.w, self.h)
        # grass
        for i, (img, (x, center_y)) in enumerate(zip(self.grass_images, self.grass_positions)):
            scale = self.grass_scales[i] if i < len(self.grass_scales) else 1.0
            orig_w = getattr(img, 'w', 80)
            orig_h = getattr(img, 'h', 80)

            new_w = orig_w * scale
            new_h = orig_h * scale

            # 기존 중심 기준에서 '아래쪽(바닥)' 위치를 유지하도록 중심 Y 보정
            prev_bottom = center_y - (orig_h / 2)
            new_center_y = prev_bottom + (new_h / 2)

            img.draw(x, new_center_y, new_w, new_h)

    def update(self):
        pass
