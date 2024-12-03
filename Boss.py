import numpy as np
from asset.BossPattern import boss_pattern, boss_color_map
from PIL import Image
from Bullet import BossBullet

class Boss:
    def __init__(self, spawn_position):
        self.pattern_size = 24
        self.scale = 6
        self.width = self.pattern_size * self.scale
        self.height = self.pattern_size * self.scale
        self.state = 'alive'
        
        # 보스 위치
        self.world_x = spawn_position[0]
        self.world_y = spawn_position[1]
        self.position = np.array([
            self.world_x - self.width/2,
            self.world_y - self.height/2,
            self.world_x + self.width/2,
            self.world_y + self.height/2
        ])
        
        # 체력 시스템
        self.max_hp = 50
        self.current_hp = self.max_hp
        
        # HP 관련 warning 시스템
        self.warning_time = 0
        self.first_warning_shown = False
        self.hp60_warning_shown = False
        self.hp30_warning_shown = False
        
        # 레이저 시스템
        self.laser_warning = False
        self.laser_active = False
        self.laser_warning_time = 40  # 1초
        self.laser_cooldown = 80  # 2초
        self.laser_timer = 0
        self.selected_rows = []
        self.selected_cols = []
        
        # 공격 패턴 시스템
        self.attack_pattern = 'basic'
        self.last_shot_time = 0
        self.shot_cooldowns = {
            'basic': 45,
            'phase2': 30,
            'phase3': 20
        }
        
        # 이미지 생성
        self.image = self.create_boss_image()

    def create_boss_image(self):
        img = Image.new('RGBA', (self.width, self.height))
        
        # 왼쪽 절반 그리기
        for y in range(self.pattern_size):
            for x in range(self.pattern_size):
                color = boss_color_map[boss_pattern[y][x]]
                for i in range(self.scale):
                    for j in range(self.scale):
                        pixel_x = x * self.scale + i
                        pixel_y = y * self.scale + j
                        if pixel_x < self.width//2:
                            img.putpixel((pixel_x, pixel_y), color)

        # 오른쪽 미러링
        for y in range(self.height):
            for x in range(self.width//2):
                color = img.getpixel((x, y))
                img.putpixel((self.width - 1 - x, y), color)

        return img

    def take_damage(self):
        self.current_hp -= 1
        if self.current_hp <= 0:
            self.state = 'die'
            return
            
        # HP에 따른 패턴 변경 및 warning 설정
        hp_percent = self.current_hp / self.max_hp
        if hp_percent <= 0.3 and not self.hp30_warning_shown:
            self.hp30_warning_shown = True
            self.warning_time = 60
            self.attack_pattern = 'phase3'
        elif hp_percent <= 0.6 and not self.hp60_warning_shown:
            self.hp60_warning_shown = True
            self.warning_time = 60
            self.attack_pattern = 'phase2'

    def prepare_laser_attack(self, map_data,camera_x):
        if self.laser_cooldown > 0 or self.laser_warning or self.laser_active:
            return
            
        if self.attack_pattern == 'basic':
            return

        # 레이저 가로범위
        valid_rows = range(int(len(map_data) * 0.3), len(map_data))

        #레이저 세로범위
        screen_start_col = camera_x // 24  # 타일 크기로 나누어 타일 인덱스 계산, 카메라 안에 들어오게
        screen_tiles = 240 // 24  # 화면 너비를 타일 수로 변환
        valid_cols = range(int(screen_start_col), int(screen_start_col + screen_tiles))
        
        self.selected_rows = []
        self.selected_cols = []
        
        if self.attack_pattern == 'phase2':
            self.selected_rows.append(np.random.choice(list(valid_rows)))
        else:
            self.selected_rows.append(np.random.choice(list(valid_rows)))
            self.selected_cols.append(np.random.choice(list(valid_cols)))
            
        self.laser_warning = True
        self.laser_warning_time = 60

    def update_laser(self):
        if self.laser_warning:
            self.laser_warning_time -= 1
            if self.laser_warning_time <= 0:
                self.laser_warning = False
                self.laser_active = True
                self.laser_timer = 30
        
        if self.laser_active:
            self.laser_timer -= 1
            if self.laser_timer <= 0:
                self.laser_active = False
                self.laser_cooldown = 120
                self.selected_rows = []
                self.selected_cols = []
                
        if self.laser_cooldown > 0:
            self.laser_cooldown -= 1

    def can_shoot(self):
        if self.state != 'alive':
            return False
            
        self.last_shot_time += 1
        cooldown = self.shot_cooldowns[self.attack_pattern]
        
        if self.last_shot_time >= cooldown:
            self.last_shot_time = 0
            return True
        return False

    def shoot(self):
        if not self.can_shoot():
            return []

        bullets = []
        center_y = self.world_y + self.height/4

        if self.attack_pattern == 'basic':
            # 기본 3방향 발사
            directions = ['left', 'left_up', 'left_down']
            for direction in directions:
                bullets.append(BossBullet(self.world_x, center_y, direction))
                
        elif self.attack_pattern == 'phase2':
            angles = [-30, 0, 30]
            for angle in angles:
                bullet = BossBullet(self.world_x, center_y, 'left')
                bullet.speed_x = -8 * np.cos(np.radians(angle))
                bullet.speed_y = 8 * np.sin(np.radians(angle))
                bullets.append(bullet)
                
        else:  # phase3
            # 특정 각도로 2발 발사 (패턴 동일하게 유지)
            angles = [-30,15 ,0, 15, 30]
            for angle in angles:
                bullet = BossBullet(self.world_x, center_y, 'left')
                bullet.speed_x = -8 * np.cos(np.radians(angle))
                bullet.speed_y = 8 * np.sin(np.radians(angle))
                bullets.append(bullet)

        return bullets

    def update_position(self, camera_x):
        """화면상의 위치 업데이트"""
        screen_x = self.world_x - camera_x
        self.position = np.array([
            screen_x - self.width/2,
            self.world_y - self.height/2,
            screen_x + self.width/2,
            self.world_y + self.height/2
        ])