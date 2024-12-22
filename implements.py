import math
import random
import time
import config
import pygame
from pygame.locals import Rect, K_LEFT, K_RIGHT

# 아이템 리스트 초기화
item_list = []

class BasicObject:
    def __init__(self, color: tuple, speed: int = 0, position: tuple = (0, 0), size: tuple = (0, 0)):
        self.color = color
        self.rect = Rect(position[0], position[1], size[0], size[1])
        self.center = (self.rect.centerx, self.rect.centery)
        self.speed = speed
        self.start_time = time.time()
        self.direction = 270

    def move(self):
        dx = math.cos(math.radians(self.direction)) * self.speed
        dy = -math.sin(math.radians(self.direction)) * self.speed
        self.rect.move_ip(dx, dy)
        self.center = (self.rect.centerx, self.rect.centery)

class BlockObject(BasicObject):
    def __init__(self, color: tuple, position: tuple = (0, 0), alive=True):
        super().__init__(color, 0, position, config.block_dimensions)
        self.position = position
        self.alive = alive

    def draw(self, surface) -> None:
        pygame.draw.rect(surface, self.color, self.rect)
    
    def collide(self):
        self.alive = False

class PaddleObject(BasicObject):
    def __init__(self):
        super().__init__(config.paddle_color, 0, config.paddle_position, config.paddle_dimensions)
        self.start_pos = config.paddle_position
        self.speed = config.paddle_movement_speed
        self.cur_size = config.paddle_dimensions

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def move_paddle(self, event: pygame.event.Event):
        if event.key == K_LEFT and self.rect.left > 0:
            self.rect.move_ip(-self.speed, 0)
        elif event.key == K_RIGHT and self.rect.right < config.screen_dimensions[0]:
            self.rect.move_ip(self.speed, 0)

    def collide_item(self, item):
        if self.rect.colliderect(item.rect):
            if item.color == config.red_item_color:  # 빨간색 아이템일 때
                return True
        return False

class BallObject(BasicObject):
    def __init__(self, position: tuple = config.ball_position):
        super().__init__(config.ball_color, config.ball_movement_speed, position, config.ball_dimensions)
        self.power = 1
        self.direction = 90 + random.randint(-45, 45)

    def draw(self, surface):
        pygame.draw.ellipse(surface, self.color, self.rect)

    def collide_block(self, blocks: list):
        for block in blocks:
            if block.alive and self.rect.colliderect(block.rect):
                block.collide()  
                create_item(block.rect.center)  # 아이템 생성 호출
                self.direction = -self.direction
                blocks.remove(block)
                break

    def collide_paddle(self, paddle: PaddleObject) -> None:
        if self.rect.colliderect(paddle.rect):
            self.direction = 360 - self.direction + random.randint(-5, 5)

    def hit_wall(self):
        if self.rect.left <= 0 or self.rect.right >= config.screen_dimensions[0]:
            self.direction = 180 - self.direction
        
        if self.rect.top <= 0:
            self.direction = -self.direction
    
    def alive(self):
        return self.rect.top < config.screen_dimensions[1]

class ItemObject(BasicObject):
    def __init__(self, color: tuple, position: tuple = (0, 0)):
        super().__init__(color, config.item_movement_speed, position, config.item_dimensions)
        self.alive_status = True  # 상태를 나타내는 속성으로 변경

    def move(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top > config.screen_dimensions[1]:
            self.alive_status = False

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.rect.center, self.rect.width // 2)

    def alive(self):
        return self.alive_status  # alive_status 반환

def create_item(position):
    if random.random() < 0.2:  # 20% 확률
        item_color = random.choice([config.red_item_color, config.blue_item_color])
        item = ItemObject(item_color, position)
        item_list.append(item)  # 아이템 리스트에 추가
