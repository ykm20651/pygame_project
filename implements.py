import math
import random
import time

import config

import pygame
from pygame.locals import Rect, K_LEFT, K_RIGHT


class Basic:
    def __init__(self, color: tuple, speed: int = 0, pos: tuple = (0, 0), size: tuple = (0, 0)):
        self.color = color
        self.rect = Rect(pos[0], pos[1], size[0], size[1])
        self.center = (self.rect.centerx, self.rect.centery)
        self.speed = speed
        self.start_time = time.time()
        self.dir = 270

    def move(self):
        dx = math.cos(math.radians(self.dir)) * self.speed
        dy = -math.sin(math.radians(self.dir)) * self.speed
        self.rect.move_ip(dx, dy)
        self.center = (self.rect.centerx, self.rect.centery)

class Item(Basic):
    def __init__(self, color, pos):
        super().__init__(color, 2, pos, config.item_size) 
        self.effect = None  
    
    def draw(self, surface):
        pygame.draw.ellipse(surface, self.color, self.rect)

    def move(self):
        self.rect.move_ip(0, self.speed)

class Block(Basic):
    def __init__(self, color: tuple, pos: tuple = (0,0), alive = True):
        super().__init__(color, 0, pos, config.block_size)
        self.pos = pos
        self.alive = alive

    def draw(self, surface) -> None:
        if self.alive:
            pygame.draw.rect(surface, self.color, self.rect)
    
    def collide(self):
        self.alive = False
        if random.random() < 0.2: 
            item_color = random.choice([(255, 0, 0), (0, 0, 255)])
            new_item = Item(item_color, (self.rect.centerx, self.rect.centery))
            ITEMS.append(new_item)  # 아이템 리스트에 추가


class Paddle(Basic):
    def __init__(self):
        super().__init__(config.paddle_color, 0, config.paddle_pos, config.paddle_size)
        self.start_pos = config.paddle_pos
        self.speed = config.paddle_speed
        self.cur_size = config.paddle_size

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    def move_paddle(self, event: pygame.event.Event):
        if event.key == K_LEFT and self.rect.left > 0:
            self.rect.move_ip(-self.speed, 0)
        elif event.key == K_RIGHT and self.rect.right < config.display_dimension[0]:
            self.rect.move_ip(self.speed, 0)


class Ball(Basic):
    def __init__(self, pos: tuple = config.ball_pos):
        super().__init__(config.ball_color, config.ball_speed, pos, config.ball_size)
        self.power = 1
        self.dir = 90 + random.randint(-45, 45)

    def draw(self, surface):
        pygame.draw.ellipse(surface, self.color, self.rect)

    def collide_block(self, blocks: list):
        # ============================================
        # TODO: Implement an event when the ball hits a block
        closest_block = None
        closest_distance = float('inf')  # 초기 거리 값 무한대
        prev_x, prev_y = self.rect.centerx, self.rect.centery  # 공의 이전 위치 저장

        # 가장 가까운 충돌 블록 탐색
        for block in blocks:
            if block.alive:
                # 공 이동 경로와 블록의 충돌 확인
                if block.rect.clipline((prev_x, prev_y), (self.rect.centerx, self.rect.centery)):
                    # 거리 계산
                    distance = math.hypot(
                        prev_x - block.rect.centerx,
                        prev_y - block.rect.centery
                    )
                    if distance < closest_distance:
                        closest_block = block
                        closest_distance = distance

        # 가장 가까운 블록 처리
        if closest_block:
            closest_block.collide()  # 블록 상태 업데이트

            # 반사 처리: 단순히 현재 진행 방향의 반대로 변경
            self.dir = (self.dir + 180) % 360


    def collide_paddle(self, paddle: Paddle) -> None:
        if self.rect.colliderect(paddle.rect):
            self.dir = 360 - self.dir + random.randint(-5, 5)

    def hit_wall(self):
        # ============================================
        # TODO: Implement a service that bounces off when the ball hits the wall
        # 좌우 벽 충돌
        if self.rect.left <= 0 or self.rect.right >= config.display_dimension[0]:
            self.dir = 180 - self.dir  # x축 반사
        # 상단 벽 충돌
        if self.rect.top <= 0:
            self.dir = -self.dir  # y축 반사
    
    def alive(self):
        # ============================================
        # TODO: Implement a service that returns whether the ball is alive or not
        # 공이 화면 아래로 떨어졌는지 확인
        if self.rect.top >= config.display_dimension[1]:
            return False  # 공이 사라짐
        return True  # 공이 화면 안에 있음
            
