from asset.BlockPattern import grass_ground_pattern, color_map
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

    def create_enemies(self):
        enemies = []
        for y in range(len(self.map_data)):
            for x in range(len(self.map_data[0])):
                if self.map_data[y][x] in [3, 4, 5]:  # 적 타입 체크
                    spawn_position = [x * self.tile_size + self.tile_size/2, 
                                   y * self.tile_size + self.tile_size/2]
                    enemy_type = self.map_data[y][x] - 2  # 3->1, 4->2, 5->3
                    enemies.append(Enemy(spawn_position, enemy_type))
        return enemies
        
    def draw(self, canvas, camera_x):
        # 화면에 그려질 타일의 시작과 끝 인덱스 계산
        start_col = int(camera_x // self.tile_size)
        visible_tiles = (self.width // self.tile_size) + 2
        end_col = min(len(self.map_data[0]), start_col + visible_tiles)
        
        # 각 타일을 화면상의 적절한 위치에 그림
        for y in range(len(self.map_data)):
            for x in range(start_col, end_col):
                screen_x = (x * self.tile_size) - camera_x
                screen_y = y * self.tile_size
                
                if x < len(self.map_data[0]):  # 맵 범위 체크
                    tile_type = self.map_data[y][x]
                    if tile_type == 1:  # grass_ground_pattern 사용
                        # 패턴의 각 픽셀을 그림
                        for py in range(24):  # 24x24 패턴
                            for px in range(24):
                                pixel_color = color_map[grass_ground_pattern[py][px]]
                                canvas.point((screen_x + px, screen_y + py), fill=pixel_color)

    def get_tile(self, x, y):
        """실제 월드 좌표를 타일 좌표로 변환하여 해당 타일 값을 반환"""
        tile_x = int(x // self.tile_size)
        tile_y = int(y // self.tile_size)
        
        if 0 <= tile_y < len(self.map_data) and 0 <= tile_x < len(self.map_data[0]):
            return self.map_data[tile_y][tile_x]
        return 1  # 맵 밖은 벽으로 처리