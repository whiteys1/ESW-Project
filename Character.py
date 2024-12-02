import numpy as np
from PIL import Image, ImageEnhance

class Character:
    def __init__(self, width, height):
        # 캐릭터 크기
        self.width = 40
        self.height = 40
        
        # 월드 좌표 (실제 맵상의 위치)
        self.world_x = 24 * 1  # 시작 x 위치
        self.world_y = height - 40 -24  # 시작 y 위치
        
        # 물리 변수
        self.velocity_y = 0
        self.gravity = 1.0
        self.is_jumping = False
        self.is_grounded = False
        self.jump_speed = -12
        self.move_speed = 5
        self.max_fall_speed = 15  # 최대 낙하 속도 제한
        
        # 화면 표시용 position (캐릭터 그리기용)
        self.position = np.array([0, 0, self.width, self.height])
        
        # 이미지 로드
        self.image = Image.open("asset/hero.png").convert('RGBA')
        self.image = self.image.resize((self.width, self.height))
        enhancer = ImageEnhance.Brightness(self.image)
        self.image = enhancer.enhance(1.5)
        
        # 충돌 마스크 생성 - 투명하지 않은 픽셀의 위치 저장
        self.collision_mask = []
        for y in range(self.height):
            for x in range(self.width):
                pixel = self.image.getpixel((x, y))
                if pixel[3] > 0:  # 알파 값이 0보다 크면 (투명하지 않으면)
                    self.collision_mask.append((x, y))

        self.state = None
        self.outline = "#FFFFFF"
        self.center = np.array([0, 0])  # 중심점은 화면 좌표에 따라 업데이트됨

    def apply_gravity(self, world_map):
        if not self.is_grounded:
            self.velocity_y += self.gravity
            self.velocity_y = min(self.velocity_y, 12)
        
        # 새로운 y 위치 계산
        new_y = self.world_y + self.velocity_y
        
        # 발 위치의 타일 확인
        feet_tile = world_map.get_tile(self.world_x + self.width/2, new_y + self.height)
        
        # 충돌 체크 및 처리
        if feet_tile == 1:  # 벽 타일과 충돌
            self.is_grounded = True
            # 타일 크기로 정확히 정렬
            new_y = ((new_y + self.height) // world_map.tile_size) * world_map.tile_size - self.height
            self.velocity_y = 0
        else:
            self.is_grounded = False
        
        self.world_y = new_y

    def move(self, command, world_map):
        if command['move']:
            self.state = 'move'
            self.outline = "#FF0000"
            
            # 점프
            if command['up_pressed'] and self.is_grounded:
                self.velocity_y = self.jump_speed
                self.is_grounded = False
            
            # 좌우 이동
            if command['left_pressed']:
                new_x = self.world_x - self.move_speed
                if world_map.get_tile(new_x, self.world_y + self.height - 1) != 1:
                    self.world_x = new_x
            
            if command['right_pressed']:
                new_x = self.world_x + self.move_speed
                if world_map.get_tile(new_x + self.width, self.world_y + self.height - 1) != 1:
                    self.world_x = new_x
        else:
            self.state = None
            self.outline = "#FFFFFF"
        
        # 중력 적용
        self.apply_gravity(world_map)

    def update_screen_position(self, camera_x):
        """화면상의 위치 업데이트"""
        screen_x = self.world_x - camera_x
        
        self.position[0] = screen_x
        self.position[2] = screen_x + self.width
        self.position[1] = self.world_y
        self.position[3] = self.world_y + self.height
        
        # 중심점 업데이트
        self.center = np.array([screen_x + self.width/2, self.world_y + self.height/2])

    def get_collision_points(self):
        """실제 충돌 체크에 사용될 월드 좌표의 픽셀 포인트들을 반환"""
        collision_points = []
        for local_x, local_y in self.collision_mask:
            world_x = self.world_x + local_x
            world_y = self.world_y + local_y
            collision_points.append((world_x, world_y))
        return collision_points