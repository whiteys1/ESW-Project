from PIL import Image, ImageDraw
from Enemy import Enemy
from Bullet import EnemyBullet,PlayerBullet
from Character import Character
from Joystick import Joystick
from Map import Map
from Boss import Boss
from PIL import ImageFont
import time

def draw_title_screen(joystick):
    background = Image.new('RGB', (joystick.width, joystick.height), 'black')
    my_draw = ImageDraw.Draw(background)
    
    title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
    
    # 첫 줄과 둘째 줄을 분리
    title1 = "Resistance"
    title2 = "Alien Attack"
    
    # 각 줄의 너비 계산
    title1_width = title_font.getlength(title1)
    title2_width = title_font.getlength(title2)
    
    # 각 줄의 위치 계산
    title1_pos = ((joystick.width - title1_width) // 2, joystick.height // 3)
    title2_pos = ((joystick.width - title2_width) // 2, joystick.height // 3 + 30)  # 30은 줄 간격
    
    guide_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 16)
    guide = "Press [A] to Start"
    guide_width = guide_font.getlength(guide)
    guide_pos = ((joystick.width - guide_width) // 2, joystick.height * 2 // 3)
    
    my_draw.text(title1_pos, title1, font=title_font, fill="white")
    my_draw.text(title2_pos, title2, font=title_font, fill="white")
    my_draw.text(guide_pos, guide, font=guide_font, fill="white")
    
    return background

def draw_game_over_screen(joystick, is_clear=False):
    # 배경
    background = Image.new('RGB', (joystick.width, joystick.height), 'black')
    my_draw = ImageDraw.Draw(background)
    
    # 결과 텍스트
    result_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 32)
    result_text = "GAME CLEAR!" if is_clear else "GAME OVER"
    text_width = result_font.getlength(result_text)
    text_pos = ((joystick.width - text_width) // 2, joystick.height // 2)
    
    my_draw.text(text_pos, result_text, font=result_font, fill="white")
    return background

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

def update_bullets(player_bullets, enemy_bullets, my_character, enemies, last_shot_time, joystick, SHOT_COOLDOWN, camera_x):
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
        if enemy.state == 'alive':
            if isinstance(enemy, Boss):  # 보스인 경우
                new_bullets = enemy.shoot()  # shoot 메서드 호출
                enemy_bullets.extend(new_bullets)
            else:  # 일반 적인 경우
                if enemy.can_shoot():
                    enemy_bullets.append(EnemyBullet(enemy.world_x, enemy.world_y))


    # 총알 이동 및 제거
    for bullet in player_bullets[:]:
        bullet.move()
        # 플레이어 총알과 적의 충돌 체크 추가
        bullet.collision_check(enemies)
        if (bullet.position[0] < 0 or 
            bullet.position[2] > joystick.width + 100 or
            bullet.state != 'active'):
            player_bullets.remove(bullet)

    for bullet in enemy_bullets[:]:
        bullet.move()
        # 화면 범위 체크를 world 좌표로 수정
        screen_x = bullet.world_x - camera_x
        if (screen_x < -50 or screen_x > joystick.width + 50 or
            bullet.state != 'active'):
            enemy_bullets.remove(bullet)
        if bullet.check_collision_with_player(my_character):
            return True, last_shot_time  # 게임 오버
    
    return False, last_shot_time

def update_game_state(my_character, command, my_map, camera_x, FIXED_X_POSITION, joystick):
   game_over = False
   max_camera_x = (len(my_map.map_data[0]) * my_map.tile_size) - joystick.width

   if my_character.world_x <= max_camera_x + FIXED_X_POSITION:
       camera_x = int(my_character.world_x - FIXED_X_POSITION)
       my_character.position[0] = FIXED_X_POSITION
       my_character.position[2] = FIXED_X_POSITION + my_character.width
   else:
       camera_x = max_camera_x

   camera_x = max(0, min(camera_x, max_camera_x))

   # 보스의 레이저 공격 업데이트
   for enemy in my_map.enemies:
        if isinstance(enemy, Boss) and enemy.state == 'alive':
            enemy.update_laser()
            if enemy.laser_cooldown <= 0 and not enemy.laser_warning and not enemy.laser_active:
                enemy.prepare_laser_attack(my_map.map_data, camera_x)
                
            # 레이저 충돌 체크
            if enemy.laser_active:
                # 캐릭터의 충돌 박스 계산
                char_left = int(my_character.world_x)
                char_right = int(my_character.world_x + my_character.width)
                char_top = int(my_character.world_y)
                char_bottom = int(my_character.world_y + my_character.height)

                # 가로 레이저 충돌 체크
                for row in enemy.selected_rows:
                    laser_y = row * my_map.tile_size
                    if char_top <= laser_y + my_map.tile_size and char_bottom >= laser_y:
                        game_over = True
                        break

                # 세로 레이저 충돌 체크
                for col in enemy.selected_cols:
                    laser_x = col * my_map.tile_size
                    if char_left <= laser_x + my_map.tile_size and char_right >= laser_x:
                        game_over = True
                        break

   my_character.move(command, my_map)
   my_character.update_screen_position(camera_x)
   
   return game_over,camera_x

def draw_game(my_image, my_draw, background, my_map, my_character, 
            player_bullets, enemy_bullets, camera_x, joystick):
   # 배경 그리기
   my_image = background.copy()
   my_draw = ImageDraw.Draw(my_image)

   # 맵 그리기
   my_map.draw(my_draw, int(camera_x))

   # 적 그리기
   for enemy in my_map.enemies:
        if enemy.state == 'alive':
            enemy.update_position(camera_x)
            enemy_screen_x = int(enemy.position[0])
            enemy_screen_y = int(enemy.position[1])
            my_image.paste(
                enemy.image.convert('RGB'),
                (enemy_screen_x, enemy_screen_y),
                enemy.image.split()[3]
            )
            
            # 보스일 경우 체력바와 경고 메시지 표시
            if isinstance(enemy, Boss):
                boss_distance = abs(my_character.world_x - enemy.world_x)
                
                if boss_distance < joystick.width:
                    # 체력바 그리기
                    my_draw.rectangle([(10, 10), (230, 25)], fill=(128,128,128))
                    health_width = int(220 * (enemy.current_hp / enemy.max_hp))
                    my_draw.rectangle([(10, 10), (10 + health_width, 25)], fill=(255,0,0))
                    
                    # Warning 표시 로직
                    hp_percent = enemy.current_hp / enemy.max_hp
                    
                    # 처음 화면에 들어왔을 때
                    if not enemy.first_warning_shown:
                        enemy.first_warning_shown = True
                        enemy.warning_time = 60
                    
                    # HP 60% 도달했을 때
                    if not hasattr(enemy, 'hp60_warned') and hp_percent <= 0.6:
                        enemy.hp60_warned = True
                        enemy.warning_time = 60
                    
                    # HP 30% 도달했을 때    
                    if not hasattr(enemy, 'hp30_warned') and hp_percent <= 0.3:
                        enemy.hp30_warned = True
                        enemy.warning_time = 60
                    
                    # Warning 타이머 관리 및 표시
                    if hasattr(enemy, 'warning_time') and enemy.warning_time > 0:
                        enemy.warning_time -= 1
                        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 30)
                        text_width = font.getlength("WARNING!")
                        text_pos = ((joystick.width - text_width) // 2, 100)
                        my_draw.text(text_pos, "WARNING!", font=font, fill=(255,0,0))

   # 캐릭터 그리기
   y = int(my_character.position[1])
   my_image.paste(my_character.image.convert('RGB'), 
                (int(my_character.position[0]), y), 
                my_character.image.split()[3])

   # 총알 그리기
   for bullet in player_bullets:
       my_image.paste(
           bullet.image.convert('RGB'),
           (int(bullet.position[0]), int(bullet.position[1])),
           bullet.image.split()[3]
       )
      
   # 적 총알 그리기
   for bullet in enemy_bullets:
       if bullet.state == 'active':
           screen_x = int(bullet.world_x - camera_x - bullet.width/2)
           screen_y = int(bullet.position[1])
           
           if -10 <= screen_x <= joystick.width + 10:
               my_image.paste(
                   bullet.image.convert('RGB'),
                   (screen_x, screen_y),
                   bullet.image.split()[3]
               )
  
   return my_image, my_draw

def main():
   joystick = Joystick()
   
   while True:  # 전체 게임 루프
       # 시작 화면
       title_screen = draw_title_screen(joystick)
       joystick.disp.image(title_screen)
       
       # A 버튼 대기
       while joystick.button_A.value:
           pass
          
       background = Image.open("asset/background.jpeg") 
       background = background.resize((joystick.width, joystick.height))
       background = background.convert('RGB')
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
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0],
           [0,0,0,0,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6],
           [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
           [0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,0,0,0,0,0],
           [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
       ]
       
       my_map = Map(width=240, height=240, tile_size=24, map_data=map_data)

       camera_x = 0
       last_shot_time = 0
       SHOT_COOLDOWN = 10

       bullets = []
       enemy_bullets = []  
       enemies = my_map.enemies
       game_clear = False

       while True:
           command = handle_input(joystick)
           
           bullet_game_over, last_shot_time = update_bullets(bullets, enemy_bullets, 
                                                   my_character, enemies, 
                                                   last_shot_time, joystick, 
                                                   SHOT_COOLDOWN,camera_x)
           if bullet_game_over:
               break
               
           laser_game_over,camera_x = update_game_state(my_character, command, my_map, camera_x, 
                                     FIXED_X_POSITION, joystick)
           
           if laser_game_over:
               break

           for enemy in enemies:
               if isinstance(enemy, Boss) and enemy.state == 'die':
                   game_clear = True
                   break

           if game_clear:
               break

           my_image, my_draw = draw_game(my_image, my_draw, background, my_map, 
                                      my_character, bullets, enemy_bullets, camera_x, joystick)
           
           joystick.disp.image(my_image)

       # 결과 화면
       result_screen = draw_game_over_screen(joystick, game_clear)
       joystick.disp.image(result_screen)
       time.sleep(3)

       # A 버튼 대기 
       while joystick.button_A.value:
           pass
           
if __name__ == '__main__':
   main()