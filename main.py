from PIL import Image, ImageDraw
from Enemy import Enemy
from Bullet import EnemyBullet,PlayerBullet
from Character import Character
from Joystick import Joystick
from Map import Map

def handle_input(joystick):
   command = {'move': False, 'up_pressed': False, 'down_pressed': False, 
             'left_pressed': False, 'right_pressed': False}
   
   if not joystick.button_U.value:
       command['up_pressed'] = True
       command['move'] = True
       
   if not joystick.button_L.value:
       command['left_pressed'] = True
       command['move'] = True
       
   if not joystick.button_R.value:
       command['right_pressed'] = True
       command['move'] = True
       
   return command

def update_bullets(player_bullets, enemy_bullets, my_character, enemies, last_shot_time, joystick, SHOT_COOLDOWN):
   # 플레이어 총알 발사
   if not joystick.button_A.value and (last_shot_time <= 0):
       player_bullets.append(PlayerBullet(
           my_character.center[0],
           my_character.center[1]
       ))
       last_shot_time = SHOT_COOLDOWN
   if last_shot_time > 0:
       last_shot_time -= 1

   # 적 총알 발사
   for enemy in enemies:
       if enemy.state == 'alive' and enemy.can_shoot():
           enemy_bullets.append(EnemyBullet(
               enemy.center[0],
               enemy.center[1]
           ))

   # 총알 이동 및 제거
   for bullet in player_bullets[:]:
       bullet.move()
       if (bullet.position[0] < 0 or 
           bullet.position[2] > joystick.width + 100 or
           bullet.state != 'active'):
           player_bullets.remove(bullet)

   for bullet in enemy_bullets[:]:
       bullet.move()
       if (bullet.position[0] < 0 or 
           bullet.position[2] > joystick.width or
           bullet.state != 'active'):
           enemy_bullets.remove(bullet)
       if bullet.check_collision_with_player(my_character):
           return True, last_shot_time  # 게임 오버
   
   return False, last_shot_time

def update_game_state(my_character, command, my_map, camera_x, FIXED_X_POSITION, joystick):
   max_camera_x = (len(my_map.map_data[0]) * my_map.tile_size) - joystick.width
   if my_character.world_x <= max_camera_x + FIXED_X_POSITION:
       camera_x = int(my_character.world_x - FIXED_X_POSITION)
       my_character.position[0] = FIXED_X_POSITION
       my_character.position[2] = FIXED_X_POSITION + my_character.width
   else:
       camera_x = max_camera_x

   camera_x = max(0, min(camera_x, max_camera_x))
   my_character.move(command, my_map)
   my_character.update_screen_position(camera_x)
   
   return camera_x

def draw_game(my_image, my_draw, background, my_map, my_character, 
             player_bullets, enemy_bullets, camera_x):
   # 배경 그리기
   my_image = background.copy()
   my_draw = ImageDraw.Draw(my_image)

   # 맵 그리기
   my_map.draw(my_draw, int(camera_x))

   # 캐릭터 그리기
   y = int(my_character.position[1])
   my_image.paste(my_character.image.convert('RGB'), 
                 (int(my_character.position[0]), y), 
                 my_character.image.split()[3])
   
   #적 그리기
   for enemy in my_map.enemies:
        if enemy.state == 'alive':
            enemy_screen_x = int(enemy.position[0] - camera_x)  # 카메라 위치 고려
            enemy_screen_y = int(enemy.position[1])
            my_image.paste(
                enemy.image.convert('RGB'),
                (enemy_screen_x, enemy_screen_y),
                enemy.image.split()[3]
            )


   # 총알 그리기
   for bullet in player_bullets:
       my_image.paste(
           bullet.image.convert('RGB'),
           (int(bullet.position[0]), int(bullet.position[1])),
           bullet.image.split()[3]
       )
       
   for bullet in enemy_bullets:
       my_image.paste(
           bullet.image.convert('RGB'),
           (int(bullet.position[0]), int(bullet.position[1])),
           bullet.image.split()[3]
       )
   
   return my_image, my_draw

def main():
   joystick = Joystick()
   
   background = Image.open("asset/background.jpeg") 
   background = background.resize((joystick.width, joystick.height))
   background = background.convert('RGB')
   # 배경을 밝게 하기
   white = Image.new('RGB', background.size, 'white')
   background = Image.blend(background, white, 0.3)
   my_image = background.copy()
       
   my_draw = ImageDraw.Draw(my_image)
   
   my_character = Character(joystick.width, joystick.height)
   facing_direction = 'right'
   FIXED_X_POSITION = joystick.width/7

   map_data = [
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,3,0,4,0,5,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    ]
   
   my_map = Map(width=240, height=240, tile_size=24, map_data=map_data)
   #enemies = my_map.enemies

   camera_x = 0
   last_shot_time = 0
   SHOT_COOLDOWN = 10

   bullets = []  # 플레이어 총알
   enemy_bullets = []  # 적 총알
   enemies = my_map.enemies  # 적 리스트

   while True:
       command = handle_input(joystick)
       
       game_over, last_shot_time = update_bullets(bullets, enemy_bullets, 
                                                my_character, enemies, 
                                                last_shot_time, joystick, 
                                                SHOT_COOLDOWN)
       if game_over:
           print("Game Over!")
           break
           
       camera_x = update_game_state(my_character, command, my_map, camera_x, 
                                  FIXED_X_POSITION, joystick)
       
       my_image, my_draw = draw_game(my_image, my_draw, background, my_map, 
                                   my_character, bullets, enemy_bullets, camera_x)
       
       joystick.disp.image(my_image)

if __name__ == '__main__':
   main()