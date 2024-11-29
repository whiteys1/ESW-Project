import numpy as np

class Bullet:
    def __init__(self, position, direction):
        self.appearance = 'rectangle'
        self.speed = 10
        self.damage = 10
        self.position = np.array([position[0]-3, position[1]-3, position[0]+3, position[1]+3])
        self.direction = direction  # 'right' 또는 'left'
        self.state = 'active'
        self.outline = "#0000FF"

    def move(self):
        if self.state == 'active':
            if self.direction == 'right':
                self.position[0] += self.speed
                self.position[2] += self.speed
            else:  # direction == 'left'
                self.position[0] -= self.speed
                self.position[2] -= self.speed

    def collision_check(self, enemys):
        if self.state != 'active':
            return
            
        for enemy in enemys:
            if enemy.state == 'alive' and self.overlap(self.position, enemy.position):
                enemy.state = 'die'
                self.state = 'hit'
                break

    def overlap(self, ego_position, other_position):
        return not (ego_position[2] < other_position[0] or
                   ego_position[0] > other_position[2] or
                   ego_position[3] < other_position[1] or
                   ego_position[1] > other_position[3])