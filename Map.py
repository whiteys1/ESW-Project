class Map:
    map_data = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]
    def __init__(self, width, height, tile_size, map_data):
        self.width = width
        self.height = height
        self.tile_size = tile_size
        self.map_data = map_data
        self.scroll_x = 0
        self.camera_x = 0
        self.player_screen_x = width // 2  # 플레이어의 고정 스크린 x좌표
        self.background_layer = []
        self.collision_layer = []
        self.decoration_layer = []
        self.tile_properties = {
           0: {"walkable": True, "color": (255, 255, 255)},
           1: {"walkable": False, "color": (0, 0, 0)},
           2: {"walkable": True, "color": (0, 255, 0)},
           3: {"walkable": False, "color": (139, 69, 19)},
           4: {"walkable": True, "color": (0, 0, 255)}
       }
        self.initialize_layers()

    def initialize_layers(self):
        for row in self.map_data:
            collision_row = []
            for tile in row:
                collision_row.append(not self.tile_properties[tile]["walkable"])
            self.collision_layer.append(collision_row)

    def draw(self, canvas, player_x):
        # 플레이어의 실제 맵상 x좌표를 기준으로 camera_x 계산
        self.camera_x = player_x - self.player_screen_x
    
        # 카메라가 맵 경계를 벗어나지 않도록 제한
        max_camera_x = (len(self.map_data[0]) * self.tile_size) - self.width
        self.camera_x = max(0, min(self.camera_x, max_camera_x))
    
        # 화면에 보이는 타일 범위 계산
        start_col = max(0, self.camera_x // self.tile_size)
        visible_tiles = self.width // self.tile_size + 2
        end_col = min(len(self.map_data[0]), start_col + visible_tiles)
    
        # 타일 그리기
        for y in range(len(self.map_data)):
            for x in range(start_col, end_col):
                tile_type = self.map_data[y][x]
                color = self.tile_properties[tile_type]["color"]
                screen_x = x * self.tile_size - self.camera_x
                screen_y = y * self.tile_size
            
                canvas.rectangle(
                    (screen_x, screen_y, 
                    screen_x + self.tile_size, 
                    screen_y + self.tile_size),
                    fill=color,
                    outline=None
                )
                    