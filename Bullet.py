import numpy as np
from PIL import Image
from asset.BulletPattern import bullet_pattern, bullet_color_map, enemy_bullet_color_map

# Bullet.py
class Bullet:
    def __init__(self, start_x, start_y, direction):
        self.width = 10
        self.height = 10
        self.position = np.array([start_x - self.width/2, 
                                start_y - self.height/2,
                                start_x + self.width/2,
                                start_y + self.height/2])
        self.speed = 12 if direction == 'right' else -8
        self.state = 'active'
        self.direction = direction


    def move(self):
        if self.state == 'active':
            self.position[0] += self.speed
            self.position[2] += self.speed

    def overlap(self, ego_position, other_position):
        return not (ego_position[2] < other_position[0] or
                   ego_position[0] > other_position[2] or
                   ego_position[3] < other_position[1] or
                   ego_position[1] > other_position[3])

class PlayerBullet(Bullet):
    def __init__(self, start_x, start_y):
        super().__init__(start_x, start_y, 'right')
        # 플레이어 총알 패턴으로 이미지 생성
        self.image = Image.new('RGBA', (self.width, self.height))
        for y in range(10):
            for x in range(10):
                self.image.putpixel((x, y), bullet_color_map[bullet_pattern[y][x]])
        self.world_x = start_x  # 월드 좌표 추가

    def collision_check(self, enemys):
        if self.state != 'active':
            return
        for enemy in enemys:
            if enemy.state == 'alive' and self.overlap(self.position, enemy.position):
                enemy.take_damage()
                self.state = 'hit'
                break

class EnemyBullet(Bullet):
    def __init__(self, start_x, start_y):
        super().__init__(start_x, start_y, 'left')
        # world 좌표로 시작
        self.world_x = start_x
        self.position = np.array([
            self.world_x - self.width / 2, 
            start_y - self.height / 2,
            self.world_x + self.width / 2,
            start_y + self.height / 2
        ])
        
        # 이미지 생성
        self.image = Image.new('RGBA', (self.width, self.height))
        # 충돌 마스크 생성
        self.collision_mask = []
        for y in range(10):
            for x in range(10):
                reversed_x = 9 - x
                color = enemy_bullet_color_map[bullet_pattern[y][reversed_x]]
                self.image.putpixel((x, y), color)
                if color[3] > 0:  # 투명하지 않은 픽셀은 충돌 마스크에 추가
                    self.collision_mask.append((x, y))

    def move(self):
        if self.state == 'active':
            # 월드 좌표 업데이트
            self.world_x += self.speed
            # position 업데이트
            self.position[0] = self.world_x - self.width / 2
            self.position[2] = self.world_x + self.width / 2

    def check_collision_with_player(self, player):
        if self.state != 'active':
            return False

        # 1. 박스 충돌 검사
        bullet_box = np.array([
            self.world_x - self.width / 2,
            self.position[1],
            self.world_x + self.width / 2,
            self.position[3]
        ])

        player_box = np.array([
            player.world_x,
            player.world_y,
            player.world_x + player.width,
            player.world_y + player.height
        ])

        # 박스가 겹치지 않으면 충돌 없음
        if not self.overlap(bullet_box, player_box):
            return False

        # 2. 픽셀 단위 충돌 검사
        bullet_left = int(self.world_x - self.width / 2)
        bullet_top = int(self.position[1])

        bullet_pixels = set()
        for px, py in self.collision_mask:
            bullet_pixels.add((bullet_left + px, bullet_top + py))

        player_pixels = set(player.get_collision_points())

        # 두 집합의 교집합이 있으면 충돌
        return len(bullet_pixels.intersection(player_pixels)) > 0


class BossBullet(EnemyBullet):
    def __init__(self, start_x, start_y, direction):
        super().__init__(start_x, start_y)
        self.width = 15
        self.height = 15
        self.state = 'active'

        # 방향별 속도 설정
        if direction == 'left':
            self.speed_x = -8
            self.speed_y = 0
        elif direction == 'left_up':
            self.speed_x = -8
            self.speed_y = -8
        elif direction == 'left_down':
            self.speed_x = -8
            self.speed_y = 8

        self.world_x = start_x
        self.position = np.array([
            start_x - self.width / 2,
            start_y - self.height / 2,
            start_x + self.width / 2,
            start_y + self.height / 2
        ])
       
        # 이미지 생성
        self.image = Image.new('RGBA', (self.width, self.height))
        self.collision_mask = []
        for y in range(10):
            for x in range(10):
                reversed_x = 9 - x
                color = enemy_bullet_color_map[bullet_pattern[y][reversed_x]]
                scale = 1.5
                # scale x scale 크기로 확대
                scaled_x = int(x * scale)
                scaled_y = int(y * scale)
                if scaled_x < self.width and scaled_y < self.height:
                    self.image.putpixel((scaled_x, scaled_y), color)
                    if color[3] > 0:
                        self.collision_mask.append((scaled_x, scaled_y))

    def move(self):
        if self.state == 'active':
            self.world_x += self.speed_x
            self.position[0] += self.speed_x
            self.position[2] += self.speed_x

            if hasattr(self, 'speed_y'):
                self.position[1] += self.speed_y
                self.position[3] += self.speed_y

    def check_collision_with_player(self, player):
        if self.state != 'active':
            return False

        # 1. 박스 충돌 검사
        bullet_box = np.array([
            self.world_x - self.width / 2,
            self.position[1],
            self.world_x + self.width / 2,
            self.position[3]
        ])

        player_box = np.array([
            player.world_x,
            player.world_y,
            player.world_x + player.width,
            player.world_y + player.height
        ])

        # 박스가 겹치지 않으면 충돌 없음
        if not self.overlap(bullet_box, player_box):
            return False

        # 2. 픽셀 단위 충돌 검사
        bullet_left = int(self.world_x - self.width / 2)
        bullet_top = int(self.position[1])

        bullet_pixels = set()
        for px, py in self.collision_mask:
            bullet_pixels.add((bullet_left + px, bullet_top + py))

        player_pixels = set(player.get_collision_points())

        # 두 집합의 교집합이 있으면 충돌
        return len(bullet_pixels.intersection(player_pixels)) > 0
