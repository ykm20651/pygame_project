# Setting for Blocks
# Number of blocks
block_count = (5, 3)
# Size of margin
margin_size = (60, 40)
# Size of block
block_dimensions = (80, 30)
# Spacing between blocks
block_spacing = (20, 20)
score_position = (10, 10)
life_position = (450, 10)

# Display setting
frames_per_second = 30
wall_thickness = 10
scoreboard_height = 50
gameboard_height_ratio = 3

screen_dimensions = (600, 800)

center_x = screen_dimensions[0] / 2
center_y = screen_dimensions[1] / 2

# Setting for paddle
paddle_color = (242, 242, 0)
paddle_position = (center_x, screen_dimensions[1] - 100)
paddle_dimensions = (100, 30)
paddle_movement_speed = 5

# Setting for ball
ball_color = (242, 242, 0)
ball_movement_speed = screen_dimensions[1] / 80
ball_position = (center_x, paddle_position[1] - paddle_dimensions[1])
ball_fever_color = (255, 50, 0)
ball_dimensions = (20, 20)

# Setting for items
item_dimensions = (20, 20)
item_movement_speed = 5  # 아이템 이동 속도 추가
extra_item_probability = 0.3
fever_item_probability = 0.1
score_item_probability = 0.1
paddle_extension_probability = 0.1

fever_duration = 5

score_increment = 100
score_increment_color = (0, 255, 0)

paddle_extension_ratio = 2
paddle_extension_duration = 5
paddle_extension_color = (0, 126, 255)

# 아이템 색상 추가
red_item_color = (255, 0, 0)  # 빨간색 아이템
blue_item_color = (0, 0, 255)  # 파란색 아이템

item_colors = [(255, 0, 0), (255, 165, 0), (255, 255, 0)]
collision_threshold = len(item_colors) - 1

# Total number of life.
total_lives = 3
