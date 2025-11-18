import random
import math
from pico2d import *
import game_world
import game_framework


# bird Fly Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
Fly_SPEED_KMPH = 10.0  # Km / Hour
Fly_SPEED_MPM = (Fly_SPEED_KMPH * 1000.0 / 60.0)
Fly_SPEED_MPS = (Fly_SPEED_MPM / 60.0)
Fly_SPEED_PPS = (Fly_SPEED_MPS * PIXEL_PER_METER)

# bird Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 3.0

animation_names = ['Fly','Hit','Die']

class Duck:

    images=None

    def load_images(self):
        if Duck.images is None:
            Duck.images = {}
            for name in animation_names:
                frames = []
                for i in range(1, 4):
                    path = f"./duck/{name} ({i}).png"
                    try:
                        frames.append(load_image(path))
                    except Exception:
                        pass
                if not frames:
                    try:
                        img = load_image(f"./duck/{name}.png")
                        frames = [img]
                    except Exception:
                        frames = []
                if frames:
                    Duck.images[name] = frames

    def __init__(self, world=None):
        # world는 선택적 인자로 저장(필요시 사용)
        self.world = world
        self.x=random.randint(0,800)
        self.y=100
        self.load_images()
        self.frame=0
        self.dir=random.choice([-1,1])
        self.angle = random.randint(30, 60)  # 비행 각도
        self.speed = Fly_SPEED_PPS
        # 상승 속도 비율 (0.0 ~ 1.0, 작을수록 상승이 느려짐)
        self.upward_scale = 1.0
        # 체력
        self.max_hp=3
        self.hp=self.max_hp
        # 상태 관리
        self.state = 'Fly'  # 'Fly' | 'Hit' | 'Die'
        self.hit_timer = 0.0
        self.hit_duration = 0.4
        self.die_fall_speed = 0.0
        self.die_rotate = 0.0
        self.die_rotate_speed = 0.0

    def get_bb(self):
        # 죽으면 히트박스 비활성화
        if self.state != 'Fly':
            return (0, 0, 0, 0)
        half_width = 40  # 이미지 너비의 절반 (80/2)
        half_height = 40  # 이미지 높이의 절반 (80/2)
        return (
            self.x - half_width,  # 왼쪽
            self.y - half_height,  # 아래
            self.x + half_width,  # 오른쪽
            self.y # 위
        )

    def take_damage(self, damage):
        # 이미 죽었거나 히트 상태라면 무시
        if self.state in ('Hit', 'Die'):
            return
        # 데미지 적용
        self.hp -= damage
        if self.hp <= 0:
            # 사망 처리: Die 상태로 전환하고 낙하/회전 초기화
            self.state = 'Die'
            self.die_fall_speed = 0.0
            self.die_rotate_speed = random.uniform(-360.0, 360.0)  # deg/sec
            # 프레임 초기화
            self.frame = 0.0
        else:
            # 피격 상태로 전환 (짧게 보여줌)
            self.state = 'Hit'
            self.hit_timer = self.hit_duration
            self.frame = 0.0

    def handle_event(self, event):
        pass

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        if self.state == 'Fly':
            # 방향 전환 확률
            if random.random() < 0.005:
                self.dir *= -1
                self.angle = random.randint(30, 60)

            # 대각선 이동 계산
            angle_rad = math.radians(self.angle)
            # 가로 이동
            self.x += self.speed * self.dir * math.cos(angle_rad) * game_framework.frame_time
            # 세로 이동: 상승일 때만 scale 적용
            vertical = self.speed * math.sin(angle_rad) * game_framework.frame_time
            if vertical > 0:
                vertical *= self.upward_scale
            self.y += vertical

            # 화면 경계 처리
            if self.x < 0:
                self.dir = 1
            elif self.x > 800:
                self.dir = -1

            #Y축이 620 이상이면 삭제
            if self.y > 620:
                game_world.remove_object(self)

            self.x = clamp(0, self.x, 800)
        elif self.state == 'Hit':
            # 피격 애니메이션 재생 및 시간 경과 후 원래 상태로 복귀
            self.hit_timer -= game_framework.frame_time
            if self.hit_timer <= 0.0:
                self.state = 'Fly'
                self.frame = 0.0

        elif self.state == 'Die':
            # 죽은 후 회전하며 아래로 떨어짐
            # 낙하 가속도 효과
            gravity = 400.0  # pixel/s^2
            self.die_fall_speed += gravity * game_framework.frame_time
            self.y -= self.die_fall_speed * game_framework.frame_time
            # 회전
            self.die_rotate += self.die_rotate_speed * game_framework.frame_time

            # 화면 아래로 충분히 떨어지면 제거
            if self.y < 80:
                try:
                    game_world.remove_object(self)
                except Exception:
                    pass

    def draw(self):
        img_list = Duck.images.get(self.state, Duck.images.get('Fly', []))
        if img_list:
            idx = int(self.frame) % max(1, len(img_list))
            img = img_list[idx]
            w = getattr(img, 'w', 80)
            h = getattr(img, 'h', 80)
            if self.state == 'Die':
                # 회전하면서 그리기
                img.composite_draw(math.radians(self.die_rotate), ' ', self.x, self.y, w, h)
            else:
                # 좌우 반전 처리 (Fly, Hit)
                if self.dir < 0:
                    img.composite_draw(0, 'h', self.x, self.y, w, h)
                else:
                    img.draw(self.x, self.y, w, h)
        # 히트박스는 살아있는 경우에만 표시 (디버그 목적)
        if self.state != 'Die':
            draw_rectangle(*self.get_bb())