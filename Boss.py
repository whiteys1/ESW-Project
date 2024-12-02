import numpy as np
from asset.BossPattern import boss_pattern,boss_color_map
from PIL import Image
from Bullet import BossBullet

class Boss:
    def __init__(self, spawn_position):
        self.pattern_size = 24    # 패턴의 기본 크기
        self.scale = 6           # 6배 확대 (24 * 6 = 144)
        self.width = self.pattern_size * self.scale   # 144 pixels
        self.height = self.pattern_size * self.scale  # 144 pixels
        self.state = 'alive'      # 상태 초기화 추가
        
        # 월드 좌표
        self.world_x = spawn_position[0]
        self.world_y = spawn_position[1]
        
        # 화면상 위치
        self.position = np.array([
            self.world_x - self.width/2,
            self.world_y - self.height/2,
            self.world_x + self.width/2,
            self.world_y + self.height/2
        ])
        
        # 체력 설정
        self.max_hp = 50
        self.current_hp = self.max_hp
        
        # 공격 관련
        self.attack_pattern = 'basic'  # basic, special1, special2
        self.last_shot_time = 0
        self.basic_shot_cooldown = 45
        self.special1_cooldown = 90
        self.special2_cooldown = 120
        self.warning_displayed = False
        self.attack_warning_time = 0
        
        # 이미지 생성
        self.image = self.create_boss_image()
        
    def create_boss_image(self):
        img = Image.new('RGBA', (self.width, self.height))

        # 왼쪽 절반 그리기
        for y in range(self.pattern_size):
            for x in range(self.pattern_size):
                color = boss_color_map[boss_pattern[y][x]]
                # scale x scale 크기로 확대
                for i in range(self.scale):
                    for j in range(self.scale):
                        pixel_x = x * self.scale + i
                        pixel_y = y * self.scale + j
                        if pixel_x < self.width//2:  # 왼쪽 절반만
                            img.putpixel((pixel_x, pixel_y), color)

        # 오른쪽 절반은 왼쪽을 미러링
        for y in range(self.height):
            for x in range(self.width//2):
                color = img.getpixel((x, y))
                mirror_x = self.width - 1 - x
                img.putpixel((mirror_x, y), color)

        return img
        
    def take_damage(self):
        print(f"Boss taking damage! Current HP: {self.current_hp}")
        self.current_hp -= 1
        # 체력에 따른 공격 패턴 변경
        if self.current_hp <= 0:
            self.state = 'die'
            print("Boss died!")
        elif self.current_hp <= self.max_hp * 0.3:
            self.attack_pattern = 'special2'
            print("Boss entered rage mode! (special2)")
        elif self.current_hp <= self.max_hp * 0.6:
            self.attack_pattern = 'special1'
            print("Boss changed attack pattern! (special1)")
    
    def can_shoot(self):
        if self.state != 'alive':
            return False
            
        self.last_shot_time += 1
        cooldown = {
            'basic': self.basic_shot_cooldown,
            'special1': self.special1_cooldown,
            'special2': self.special2_cooldown
        }[self.attack_pattern]
        
        if self.last_shot_time >= cooldown:
            self.last_shot_time = 0
            return True
        return False
    
    def shoot(self):
        if not self.can_shoot():
            return []

        bullets = []
        center_y = self.world_y + self.height/4  # 보스의 중앙 높이

        # 기본 3방향 발사
        if self.attack_pattern == 'basic':
            directions = ['left', 'left_up', 'left_down']
            for direction in directions:
                bullets.append(BossBullet(self.world_x, center_y, direction))
            
        # 특수 공격 1: 연속 발사
        elif self.attack_pattern == 'special1':
            for _ in range(3):  # 3발 연속 발사
                bullets.append(BossBullet(self.world_x, center_y, 'left'))
            
        # 특수 공격 2: 전방위 공격
        elif self.attack_pattern == 'special2':
            angles = [-45, -30, -15, 0, 15, 30, 45]  # 부채꼴 형태로 발사
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