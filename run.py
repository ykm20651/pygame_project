import sys
from implements import BasicObject, BlockObject, PaddleObject, BallObject, ItemObject, create_item, item_list
import config
import pygame
from pygame.locals import QUIT, Rect, K_ESCAPE, K_SPACE
import random

pygame.init()
pygame.key.set_repeat(3, 3)
surface = pygame.display.set_mode(config.screen_dimensions)

fps_clock = pygame.time.Clock()

paddle = PaddleObject()
ball1 = BallObject()
blocks = []
items = []
balls = [ball1]
life = config.total_lives
start = False

def create_blocks():
    for i in range(config.block_count[0]):
        for j in range(config.block_count[1]):
            x = config.margin_size[0] + i * (config.block_dimensions[0] + config.block_spacing[0])
            y = (
                config.margin_size[1]
                + config.scoreboard_height
                + j * (config.block_dimensions[1] + config.block_spacing[1])
            )
            color_index = j % len(config.item_colors)
            color = config.item_colors[color_index]
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

        # 패들과 아이템 충돌 체크
        if paddle.collide_item(item):
            if item.color == config.red_item_color:
                # 빨간색 아이템을 먹었을 때 추가 공 생성
                new_ball = BallObject((paddle.rect.centerx, paddle.rect.top - 20))  # 패들 위에서 발사
                balls.append(new_ball)  # 추가 공을 balls 리스트에 추가
            item_list.remove(item)  # 아이템 제거

def main():
    global life
    global blocks
    global items
    global balls
    global paddle
    global ball1
    global start
    my_font = pygame.font.SysFont(None, 50)
    mess_clear = my_font.render("Cleared!", True, config.item_colors[2])
    mess_over = my_font.render("Game Over!", True, config.item_colors[2])
    create_blocks()

    while True:
        tick()
        surface.fill((0, 0, 0))
        paddle.draw(surface)

        for block in blocks:
            block.draw(surface)

        cur_score = config.block_count[0] * config.block_count[1] - len(blocks)

        score_txt = my_font.render(f"Score : {cur_score * 10}", True, config.item_colors[2])
        life_font = my_font.render(f"Life: {life}", True, config.item_colors[0])

        surface.blit(score_txt, config.score_position)
        surface.blit(life_font, config.life_position)

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
        fps_clock.tick(config.frames_per_second)

if __name__ == "__main__":
    main()
