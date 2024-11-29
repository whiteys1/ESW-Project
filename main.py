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

    # 맵 데이터 (실제 데이터는 이전과 동일 - 가독성을 위해 생략)
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
        
        # 입력 처리
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
        
        # 카메라 위치 업데이트 - 캐릭터의 월드 좌표 기준
        camera_x = int(my_character.world_x - joystick.width/2)
        max_camera_x = (len(my_map.map_data[0]) * my_map.tile_size) - joystick.width
        camera_x = max(0, min(camera_x, max_camera_x))
        
        # 총알 발사
        if not joystick.button_A.value and (last_shot_time + SHOT_COOLDOWN) <= 0:
            bullets.append(Bullet(my_character.center[0], my_character.center[1], facing_direction))
            last_shot_time = SHOT_COOLDOWN
        last_shot_time -= 1
        
        # 총알 업데이트
        for bullet in bullets[:]:
            bullet.move()
            if (bullet.position[0] < 0 or 
                bullet.position[2] > joystick.width or 
                bullet.state != 'active'):
                bullets.remove(bullet)
        
        # 캐릭터 업데이트
        my_draw.rectangle((0, 0, joystick.width, joystick.height), fill=(255, 255, 255, 100))
        my_map.draw(my_draw, int(camera_x))
        
        # 캐릭터 이동 및 그리기 업데이트
        my_character.move(command, my_map)
        my_character.update_screen_position(camera_x)
        
        # 화면에 캐릭터 그리기 (y_offset 고려)
        y = int(my_character.position[1])
        my_image.paste(my_character.image.convert('RGB'), 
                      (int(my_character.position[0]), y), 
                      my_character.image.split()[3])
        
        # 총알 그리기
        for bullet in bullets:
            my_draw.rectangle(
                (bullet.position[0], bullet.position[1] + 80,
                 bullet.position[2], bullet.position[3] + 80),
                fill='blue'
            )
        
        joystick.disp.image(my_image)

if __name__ == '__main__':
    main()