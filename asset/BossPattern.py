boss_pattern = [
    # 48x48 패턴 - 문어 모양 (왼쪽 절반)
    [0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1],
    [0,0,0,0,0,0,0,0,1,1,1,1,2,2,2,2,2,2,2,2,2,2,1,1],
    [0,0,0,0,0,0,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1],
    [0,0,0,0,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,0],
    [0,0,0,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,0,0],
    [0,0,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,0,0,0],
    [0,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,0,0,0,0],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,0,0,0,0,0],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,0,0,0,0,0,0],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,0,0,0,0,0,0,0],
    [1,2,2,2,3,3,2,2,2,2,3,3,2,2,2,1,0,0,0,0,0,0,0,0],
    [1,2,2,2,3,4,3,2,2,2,3,4,3,2,2,1,0,0,0,0,0,0,0,0],
    [1,2,2,2,3,3,2,2,2,2,3,3,2,2,2,1,0,0,0,0,0,0,0,0],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,0,0,0,0,0,0,0],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,0,0,0,0,0,0],
    [1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,0,0,0,0,0],
    [0,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,0,0,0,0],
    [0,0,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,0,0,0],
    [0,0,0,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,0,0],
    [0,0,0,0,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1,0],
    [0,0,0,0,0,0,1,1,2,2,2,2,2,2,2,2,2,2,2,2,2,2,1,1],
    [0,0,0,0,0,0,0,0,1,1,1,1,2,2,2,2,2,2,2,2,2,2,1,1],
    [0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1],
    [0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0,0,1,1,0],  # 촉수
]

boss_color_map = {
    0: (0, 0, 0, 0),          # 투명
    1: (255, 255, 255, 255),  # 테두리 (흰색)
    2: (128, 0, 128, 255),    # 몸체 (보라색)
    3: (255, 255, 255, 255),  # 눈 테두리 (흰색)
    4: (255, 0, 0, 255)       # 눈동자 (빨간색)
}