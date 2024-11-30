from PIL import Image, ImageDraw
from Enemy import Enemy
from Bullet import Bullet
from Character import Character
from Joystick import Joystick
from Map import Map

def main():
   joystick = Joystick()
   
   # 배경 이미지 로드 및 기본 이미지 생성
   try:
       background = Image.open("asset/background.jpeg")
       background = background.resize((joystick.width, joystick.height))
       background = background.convert('RGB')
       # 기본 이미지를 배경으로 초기화
       # 흰색 이미지와 블렌딩
       white = Image.new('RGB', background.size, 'white')
       # alpha값이 클수록 더 밝아짐 (0.0 ~ 1.0)
       background = Image.blend(background, white, 0.5)
       my_image = background.copy()
   except Exception as e:
       print(f"Warning: Failed to load background: {e}")
       my_image = Image.new("RGB", (joystick.width, joystick.height))
       
   my_draw = ImageDraw.Draw(my_image)
   
   my_character = Character(joystick.width, joystick.height)
   bullets = []
   facing_direction = 'right'
   FIXED_X_POSITION = joystick.width/7 # 캐릭터 고정 위치

   map_data = [
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    ]
   
   my_map = Map(width=240, height=240, tile_size=24, map_data=map_data)
   camera_x = 0
   last_shot_time = 0
   SHOT_COOLDOWN = 10

   while True:
       command = {'move': False, 'up_pressed': False, 'down_pressed': False, 
                 'left_pressed': False, 'right_pressed': False}
       
       if not joystick.button_U.value:
           command['up_pressed'] = True
           command['move'] = True
           
       if not joystick.button_L.value:
           command['left_pressed'] = True
           command['move'] = True
           facing_direction = 'left'
           
       if not joystick.button_R.value:
           command['right_pressed'] = True
           command['move'] = True
           facing_direction = 'right'
       
       # 카메라 위치 업데이트
       max_camera_x = (len(my_map.map_data[0]) * my_map.tile_size) - joystick.width
       if my_character.world_x <= max_camera_x + FIXED_X_POSITION:
           # 일반 상태: 캐릭터 고정, 배경 스크롤
           camera_x = int(my_character.world_x - FIXED_X_POSITION)
           my_character.position[0] = FIXED_X_POSITION
           my_character.position[2] = FIXED_X_POSITION + my_character.width
       else:
           # 맵 끝: 캐릭터 자유 이동
           camera_x = max_camera_x

       camera_x = max(0, min(camera_x, max_camera_x))
       
       if not joystick.button_A.value and (last_shot_time <= 0):
           bullets.append(Bullet(
               my_character.center[0],
               my_character.center[1],
               'right'
           ))
           last_shot_time = SHOT_COOLDOWN
       if last_shot_time > 0:
           last_shot_time -= 1
       
       for bullet in bullets[:]:
           bullet.move()
           if (bullet.position[0] < 0 or 
               bullet.position[2] > joystick.width + 100 or
               bullet.state != 'active'):
               bullets.remove(bullet)
       
       # 매 프레임마다 새로운 프레임 시작
       my_image = background.copy()  # 배경으로 초기화
       my_draw = ImageDraw.Draw(my_image)
       my_map.draw(my_draw, int(camera_x))
       
       my_character.move(command, my_map)
       my_character.update_screen_position(camera_x)
       
       y = int(my_character.position[1])
       my_image.paste(my_character.image.convert('RGB'), 
                     (int(my_character.position[0]), y), 
                     my_character.image.split()[3])
       
       for bullet in bullets:
           my_image.paste(
               bullet.image.convert('RGB'),
               (int(bullet.position[0]), int(bullet.position[1])),
               bullet.image.split()[3]
           )
       
       joystick.disp.image(my_image)

if __name__ == '__main__':
   main()