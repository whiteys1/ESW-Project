import numpy as np
from PIL import Image
from asset.BlueAlienPattern import blue_alien_pattern, alien_color_map
from asset.GreenAlienPattern import green_alien_pattern
from asset.RedAlienPattern import red_alien_pattern

class Enemy:
    def __init__(self, spawn_position, enemy_type=1):
        self.width = 48
        self.height = 48
        self.state = 'alive'
        self.position = np.array([spawn_position[0] - 24, spawn_position[1] - 24, 
                                spawn_position[0] + 24, spawn_position[1] + 24])
        self.center = np.array([(self.position[0] + self.position[2]) / 2,
                              (self.position[1] + self.position[3]) / 2])
        self.world_x = spawn_position[0]
        self.world_y = spawn_position[1]
        
        # 적 타입과 체력 설정
        self.type = enemy_type
        if enemy_type == 1:  # 초록
            self.max_hp = 1 
            pattern = green_alien_pattern
        elif enemy_type == 2:  # 파랑
            self.max_hp = 2
            pattern = blue_alien_pattern
        else:  # 빨강
            self.max_hp = 3
            pattern = red_alien_pattern
        
        self.current_hp = self.max_hp
        
        # 총알 관련
        self.last_shot_time = 0
        self.SHOT_COOLDOWN = 30  # 1초마다 발사 (60프레임 기준)
        
        # 이미지 생성
        self.image = Image.new('RGBA', (self.width, self.height))
        for y in range(24):
            for x in range(24):
                color = alien_color_map[pattern[y][x]]
                # 2x2로 확대
                for i in range(2):
                    for j in range(2):
                        self.image.putpixel((x*2 + i, y*2 + j), color)
    
    def take_damage(self):
        self.current_hp -= 1
        if self.current_hp <= 0:
            self.state = 'die'
    
    def can_shoot(self):
        self.last_shot_time += 1
        if self.last_shot_time >= self.SHOT_COOLDOWN:
            self.last_shot_time = 0
            return True
        return False
