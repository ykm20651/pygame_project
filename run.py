import sys
from implements import BasicObject, BlockObject, PaddleObject, BallObject, ItemObject, create_item, item_list
import config

import pygame
from pygame.locals import QUIT, Rect, K_ESCAPE, K_SPACE
import random

pygame.init()
pygame.key.set_repeat(3, 3)
surface = pygame.display.set_mode(config.display_dimension)

fps_clock = pygame.time.Clock()

paddle = PaddleObject()
ball1 = BallObject()
blocks = []
items = []
balls = [ball1]
life = config.life
start = False

def create_blocks():
    for i in range(config.num_blocks[0]):
        for j in range(config.num_blocks[1]):
            x = config.margin[0] + i * (config.block_size[0] + config.spacing[0])
            y = (
                config.margin[1]
                + config.scoreboard_height
                + j * (config.block_size[1] + config.spacing[1])
            )
            color_index = j % len(config.colors)
            color = config.colors[color_index]
            block = BlockObject(color, (x, y))
            blocks.append(block)

def tick():
    global life
    global blocks
    global items
    global balls
    global paddle
    global ball1
    global start
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == K_ESCAPE:  # ESC 키가 눌렸을 때
                pygame.quit()
                sys.exit()
            if event.key == K_SPACE:  # space키가 눌리면 start 변수가 True로 바뀌며 게임 시작
                start = True
            paddle.move_paddle(event)

    for ball in balls:
        if start:
            ball.move()
        else:
            ball.rect.centerx = paddle.rect.centerx
            ball.rect.bottom = paddle.rect.top

        ball.collide_block(blocks)
        ball.collide_paddle(paddle)
        ball.hit_wall()
        if not ball.alive():
            balls.remove(ball)

    # 아이템 업데이트
    for item in item_list:  # item_list에서 아이템 업데이트
        item.move()
        if not item.alive():
            item_list.remove(item)

def main():
    global life
    global blocks
    global items
    global balls
    global paddle
    global ball1
    global start
    my_font = pygame.font.SysFont(None, 50)
    mess_clear = my_font.render("Cleared!", True, config.colors[2])
    mess_over = my_font.render("Game Over!", True, config.colors[2])
    create_blocks()

    while True:
        tick()
        surface.fill((0, 0, 0))
        paddle.draw(surface)

        for block in blocks:
            block.draw(surface)

        cur_score = config.num_blocks[0] * config.num_blocks[1] - len(blocks)

        score_txt = my_font.render(f"Score : {cur_score * 10}", True, config.colors[2])
        life_font = my_font.render(f"Life: {life}", True, config.colors[0])

        surface.blit(score_txt, config.score_pos)
        surface.blit(life_font, config.life_pos)

        if len(balls) == 0:
            if life > 1:
                life -= 1
                ball1 = BallObject()
                balls = [ball1]
                start = False
            else:
                surface.blit(mess_over, (200, 300))
        elif all(block.alive == False for block in blocks):
            surface.blit(mess_clear, (200, 400))
        else:
            for ball in balls:
                if start:
                    ball.move()
                ball.draw(surface)
            for block in blocks:
                block.draw(surface)

        # 아이템 그리기
        for item in item_list:  # item_list에서 아이템 그리기
            item.draw(surface)

        pygame.display.update()
        fps_clock.tick(config.fps)

if __name__ == "__main__":
    main()
