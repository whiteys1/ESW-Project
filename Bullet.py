import numpy as np
from PIL import Image
from BulletPattern import bullet_pattern, bullet_color_map

class Bullet:
    def __init__(self, start_x, start_y, direction):
        self.width = 10
        self.height = 10
        
        # 위치 설정
        self.position = np.array([start_x - self.width/2, 
                                start_y - self.height/2,
                                start_x + self.width/2,
                                start_y + self.height/2])
        
        self.speed = 12
        self.state = 'active'
        self.direction = 'right'  # 항상 오른쪽으로 발사
        
        # 총알 이미지 로드
        self.image = Image.new('RGBA', (self.width, self.height))
        for y in range(self.height):
            for x in range(self.width):
                self.image.putpixel((x, y), bullet_color_map[bullet_pattern[y][x]])

    def move(self):
        if self.state == 'active':
            self.position[0] += self.speed
            self.position[2] += self.speed

    def collision_check(self, enemys):
        if self.state != 'active':
            return
            
        for enemy in enemys:
            if enemy.state == 'alive' and self.overlap(self.position, enemy.position):
                enemy.state = 'die'
                self.state = 'hit'
                break

    def overlap(self, ego_position, other_position):
        return not (ego_position[2] < other_position[0] or
                   ego_position[0] > other_position[2] or
                   ego_position[3] < other_position[1] or
                   ego_position[1] > other_position[3])