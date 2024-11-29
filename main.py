from PIL import Image, ImageDraw
from Enemy import Enemy
from Bullet import Bullet
from Character import Character
from Joystick import Joystick
from Map import Map

def main():
   joystick = Joystick()
   my_image = Image.new("RGB", (joystick.width, joystick.height))
   my_draw = ImageDraw.Draw(my_image)
   
   my_character = Character(joystick.width, joystick.height)
   bullets = []
   facing_direction = 'right'
   FIXED_X_POSITION = joystick.width/7  # 캐릭터 고정 위치

   map_data = [
       [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
       [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
       [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
       [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
       [1,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,1],
       [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
       [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
       [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
       [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
       [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
   ]
   
   my_map = Map(width=240, height=240, tile_size=24, map_data=map_data)
   camera_x = 0
   last_shot_time = 0
   SHOT_COOLDOWN = 10  # 발사 간격 제어

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
       
       my_draw.rectangle((0, 0, joystick.width, joystick.height), fill=(255, 255, 255, 100))
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