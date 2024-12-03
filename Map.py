from asset.BlockPattern import grass_ground_pattern, color_map
from Boss import Boss
from PIL import Image, ImageDraw
import numpy as np
from Enemy import Enemy


class Map:
    def __init__(self, width, height, tile_size, map_data):
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.map_data = map_data
        self.enemies = self.create_enemies()  # 여기에 추가
        # 레이저 시스템을 위한 색상 정의
        self.warning_color = (255, 0, 0, 128)  # 반투명 빨강
        self.laser_color = (255, 255, 0, 180)  # 반투명 노랑



    def create_enemies(self):
        enemies = []
        for y in range(len(self.map_data)):
            for x in range(len(self.map_data[0])):
                if self.map_data[y][x] in [3, 4, 5]:  # 적 타입 체크
                    # 실제 월드 좌표로 변환
                    world_x = x * self.tile_size + self.tile_size/2
                    world_y = y * self.tile_size + self.tile_size/2
                    spawn_position = [world_x, world_y]
                    enemy_type = self.map_data[y][x] - 2  # 3->1, 4->2, 5->3
                    enemy = Enemy(spawn_position, enemy_type)
                    # 월드 좌표 저장
                    enemy.world_x = world_x
                    enemy.world_y = world_y
                    enemies.append(enemy)
                elif self.map_data[y][x] == 6:  # 보스
                    world_x = x * self.tile_size + self.tile_size/2
                    world_y = y * self.tile_size + self.tile_size/2
                    spawn_position = [world_x, world_y]
                    boss = Boss(spawn_position)  # Boss 클래스의 인스턴스 생성
                    enemies.append(boss)
        return enemies
        
    def draw(self, canvas, camera_x):
        # 현재 camera_x 저장
        current_camera_x = int(camera_x)  # 정수로 고정하여 흔들림 방지
    
        # 화면에 그려질 타일의 시작과 끝 인덱스 계산
        start_col = int(current_camera_x // self.tile_size)
        visible_tiles = (self.width // self.tile_size) + 2
        end_col = min(len(self.map_data[0]), start_col + visible_tiles)
    
        # 맵 그리기
        for y in range(len(self.map_data)):
            for x in range(start_col, end_col):
                screen_x = (x * self.tile_size) - current_camera_x
                screen_y = y * self.tile_size
            
                if x < len(self.map_data[0]):  # 맵 범위 체크
                    tile_type = self.map_data[y][x]
                    if tile_type == 1:  # grass_ground_pattern 사용
                        for py in range(24):
                            for px in range(24):
                                pixel_color = color_map[grass_ground_pattern[py][px]]
                                canvas.point((screen_x + px, screen_y + py), fill=pixel_color)

        # 레이저 그리기 (맵 그린 후에 처리)
        for enemy in self.enemies:
            if isinstance(enemy, Boss):
                if enemy.laser_warning or enemy.laser_active:
                    color = list(self.warning_color if enemy.laser_warning else self.laser_color)
                
                    # 가로 레이저 그리기
                    for row in enemy.selected_rows:
                        y = row * self.tile_size
                        canvas.rectangle([
                            (0, y),
                            (self.width, y + self.tile_size)
                        ], fill=tuple(color), outline=None)
                
                    # 세로 레이저 그리기
                    for col in enemy.selected_cols:
                        x = (col * self.tile_size) - current_camera_x
                        canvas.rectangle([
                            (x, 0),
                            (x + self.tile_size, self.height)
                        ], fill=tuple(color), outline=None)

    def get_tile(self, x, y):
        """실제 월드 좌표를 타일 좌표로 변환하여 해당 타일 값을 반환"""
        tile_x = int(x // self.tile_size)
        tile_y = int(y // self.tile_size)
        
        if 0 <= tile_y < len(self.map_data) and 0 <= tile_x < len(self.map_data[0]):
            return self.map_data[tile_y][tile_x]
        return 1  # 맵 밖은 벽으로 처리