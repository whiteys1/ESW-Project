import numpy as np
from PIL import Image
from asset.BulletPattern import bullet_pattern, bullet_color_map
from asset.EnemyBullet import enemy_bullet_pattern, enemy_bullet_color_map

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
        # 적 총알 패턴으로 이미지 생성
        self.image = Image.new('RGBA', (self.width, self.height))
        for y in range(10):
            for x in range(10):
                self.image.putpixel((x, y), enemy_bullet_color_map[enemy_bullet_pattern[y][x]])

    def check_collision_with_player(self, player):
        if self.state != 'active':
            return False
        return self.overlap(self.position, player.position)