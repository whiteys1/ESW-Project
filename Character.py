import numpy as np
from PIL import Image,ImageEnhance

class Character:
    def __init__(self, width, height):
        self.width = width    # 화면 너비 저장
        self.height = height  # 화면 높이 저장
        self.appearance = 'circle'
        self.state = None
        self.position = np.array([width/2 - 20, height/2 - 20, width/2 + 20, height/2 + 20])
        # 총알 발사를 위한 캐릭터 중앙 점 추가
        self.center = np.array([(self.position[0] + self.position[2]) / 2, (self.position[1] + self.position[3]) / 2])
        self.outline = "#FFFFFF"

        self.image = Image.open("asset/hero.png").convert('RGBA')
        self.image = self.image.resize((40, 40))
        
        # 이미지 밝기 조정
        enhancer = ImageEnhance.Brightness(self.image)
        self.image = enhancer.enhance(1.5)

        # 점프 관련 변수 추가
        self.is_jumping = False
        self.jump_velocity = 0
        self.jump_speed = 15  # 초기 점프 속도
        self.gravity = 1      # 중력
        self.ground_y = height/2 - 20  # 캐릭터의 기본 y좌표 (바닥 위치

    def move(self, command = None):
        if command['move'] == False:
            self.state = None
            self.outline = "#FFFFFF" #검정색상 코드!
        
        else:
            self.state = 'move'
            self.outline = "#FF0000" #빨강색상 코드!

            if command['up_pressed'] and not self.is_jumping:
                self.is_jumping = True
                self.jump_velocity = -15  # 위쪽은 음수

            if command['down_pressed']:
                self.position[1] += 5
                self.position[3] += 5

            if command['left_pressed']:
                self.position[0] -= 5
                self.position[2] -= 5
                
            if command['right_pressed']:
                self.position[0] += 5
                self.position[2] += 5
                
        if self.is_jumping:
            #print(f"Jumping: velocity={self.jump_velocity}, y={self.position[1]}")  # 디버깅용
            # 현재 위치에 속도 적용
            self.position[1] += self.jump_velocity
            self.position[3] += self.jump_velocity
            
            # 중력 적용
            self.jump_velocity += 1.5  # 중력 가속도
            
            # 바닥 충돌 체크
            if self.position[1] >= self.height/2 - 20:  # 기존 초기 위치로 돌아옴
                self.position[1] = self.height/2 - 20
                self.position[3] = self.height/2 + 20
                self.jump_velocity = 0
                self.is_jumping = False
               

        #center update
        self.center = np.array([(self.position[0] + self.position[2]) / 2, (self.position[1] + self.position[3]) / 2]) 