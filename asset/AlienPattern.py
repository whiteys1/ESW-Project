alien_pattern = [
    [0,0,0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0],
    [0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0],
    [0,0,1,1,1,2,2,1,1,1,1,1,1,2,2,1,1,1,1,0,0,0,0,0],
    [0,1,1,1,2,2,2,2,1,1,1,1,2,2,2,2,1,1,1,1,0,0,0,0],
    [1,1,1,2,2,1,1,2,2,1,1,2,2,1,1,2,2,1,1,1,1,0,0,0],
    [1,1,2,2,1,1,1,1,2,2,2,2,1,1,1,1,2,2,1,1,1,0,0,0],
    [1,1,2,1,1,1,1,1,1,2,2,1,1,1,1,1,1,2,1,1,1,0,0,0],
    [1,1,2,2,1,1,1,1,1,1,1,1,1,1,1,1,2,2,1,1,1,0,0,0],
    [1,1,1,2,2,1,1,1,1,1,1,1,1,1,1,2,2,1,1,1,1,0,0,0],
    [1,1,1,1,2,2,2,1,1,1,1,1,1,2,2,2,1,1,1,1,1,0,0,0],
    [1,1,1,1,1,1,2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,0,0,0],
    [1,1,1,1,1,2,2,1,1,2,2,1,1,2,2,1,1,1,1,1,1,0,0,0],
    [1,1,1,1,2,2,1,1,1,2,2,1,1,1,2,2,1,1,1,1,1,0,0,0],
    [1,1,1,2,2,1,1,1,1,2,2,1,1,1,1,2,2,1,1,1,1,0,0,0],
    [1,1,1,2,1,1,1,1,1,2,2,1,1,1,1,1,2,1,1,1,1,0,0,0],
    [0,1,1,2,1,1,1,1,1,2,2,1,1,1,1,1,2,1,1,1,0,0,0,0],
    [0,1,1,2,2,1,1,1,1,1,1,1,1,1,1,2,2,1,1,0,0,0,0,0],
    [0,0,1,1,2,2,1,1,1,1,1,1,1,1,2,2,1,1,0,0,0,0,0,0],
    [0,0,0,1,1,2,2,2,1,1,1,1,2,2,2,1,1,0,0,0,0,0,0,0],
    [0,0,0,0,1,1,1,2,2,2,2,2,2,1,1,1,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,1,1,2,2,2,2,1,1,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0],
]

# 색상 맵: 초록색 외계인
green_alien_color_map = {
    0: (0, 0, 0, 0),           # 투명
    1: (0, 200, 0, 255),       # 연한 초록색
    2: (0, 100, 0, 255)        # 진한 초록색
}

# 파란색 외계인
blue_alien_color_map = {
    0: (0, 0, 0, 0),           # 투명
    1: (0, 150, 255, 255),     # 연한 파란색
    2: (0, 50, 200, 255)       # 진한 파란색
}

# 빨간색 외계인
red_alien_color_map = {
    0: (0, 0, 0, 0),           # 투명 
    1: (255, 100, 100, 255),   # 연한 빨간색
    2: (200, 0, 0, 255)        # 진한 빨간색
}