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

        # 화면을 덮을 하늘 타일 개수 계산 (여유분 포함)
        screen_width = get_canvas_width()
        tile_count = (screen_width // self.sky_tile_width) + 3

        # 하늘 타일 위치 초기화
        for i in range(tile_count):
            x = i * self.sky_tile_width
            self.sky_tiles.append(x)

    def draw(self):
        for x in self.sky_tiles:
            self.sky_image.draw(x + self.sky_tile_width // 2,
                              get_canvas_height() - self.sky_image.h // 2)
        self.image.draw(self.cw//2, self.h//2, self.w, self.h)

        for img, (x, y) in zip(self.grass_images, self.grass_positions):
            img.draw(x, y)

    def update(self):
        pass
