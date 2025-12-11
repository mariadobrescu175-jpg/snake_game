import pygame, sys, os, time, math
from snake import Snake
from food import Food, FOOD_TYPES

pygame.init()

icon = pygame.image.load("snake_lg.png")
pygame.display.set_icon(icon)

width = 600
height = 400
block_size = 20

play_width = 300
play_height = 300
play_x = ((width - play_width) // 2) // block_size * block_size
play_y = ((height - play_height) // 2) // block_size * block_size

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

apple_images = {}
for name, data in FOOD_TYPES.items():
    img = pygame.image.load(data["image"]).convert_alpha()
    img = pygame.transform.scale(img, (20, 20)) 
    apple_images[name] = img

BLACK = (0, 0, 0)
PINK = (255, 20, 147)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
PASTEL_PINK = (255, 228, 225)
LIGHT_GRAY = (240, 240, 240)
DARK_GRAY = (51, 51, 51)
DARK_PINK = (219, 112, 147)

clock = pygame.time.Clock()
fps = 6
font = pygame.font.SysFont("Times New Roman", 25)
title_font = pygame.font.SysFont("Times New Roman", 60, bold=True)

HS_FILE = os.path.join(os.path.dirname(__file__), "highscore.txt" )
snake_head_img = pygame.image.load("snake_head.png").convert_alpha()
snake_head_img = pygame.transform.scale(snake_head_img, (block_size, block_size))

FOOD_SPAWN_INTERVAL = 0.5
MAX_FOOD_ON_SCREEN = 7

paused = False
pause_button = pygame.Rect(width - 100, 50, 80, 30)

def draw_pause_button(paused):
    pygame.draw.rect(screen, DARK_PINK, pause_button, border_radius=5)
    label = "RESUME" if paused else "PAUSE"
    text = font.render(label, True, WHITE)
    screen.blit(text, (pause_button.x + (pause_button.width - text.get_width()) // 2, pause_button.y + (pause_button.height - text.get_height()) // 2))



def load_high_score():
    try:
        with open(HS_FILE, "r") as f:
            return int(f.read())
    except:
        return 0

def save_high_score(score):
    with open(HS_FILE, "w") as f:
        f.write(str(score))

high_score = load_high_score()

def draw_background():
    screen.fill(PASTEL_PINK)
    for row in range(play_height // block_size):
        for col in range(play_width // block_size):
            color = WHITE if(row + col) % 2 == 0 else LIGHT_GRAY
            x = play_x + col * block_size
            y = play_y + row *  block_size
            pygame.draw.rect(screen, color, (x,y, block_size, block_size))


def draw_header(score, high_score):
    title = font.render("SNAKE GAME", True, DARK_GRAY)
    hs_text = font.render(f"HS: {high_score}", True, DARK_GRAY)
    score_text = font.render(f"SCORE: {score}", True, DARK_GRAY)

    screen.blit(hs_text, (20, 12))
    screen.blit(title, ((width - title.get_width()) // 2, 12))
    screen.blit(score_text, (width - score_text.get_width() - 20, 12))

def draw_apple_list():
    x = 20
    y = height - 100
    for name, data in FOOD_TYPES.items():
        screen.blit(apple_images[name], (x, y))
        score_text = font.render(str(data["score"]), True, DARK_GRAY)
        screen.blit(score_text, (x + 30, y + 2))
        y += 30


def game_over_screen(score):
    text = font.render(f"Game Over!", True, (255, 255, 255))
    restart_text = font.render("Press R to Restart or Q to Quit", True, (255, 255, 255))

    screen.fill(PASTEL_PINK)
    screen.blit(text, ((width - text.get_width()) // 2, height // 2 - 50))
    screen.blit(restart_text, ((width - restart_text.get_width()) // 2, height // 2 +10))
    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_high_score(high_score)
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    save_high_score(score)
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_r:
                    return
                

def opening_screen(high_score):
    snake_preview = [(width//2 - i*block_size, height//2 + 100) for i in range(10)]

    menu_running = True
    while menu_running:
        screen.fill(PASTEL_PINK)
        title_text = "SNAKE GAME"
        pulse = (math.sin(pygame.time.get_ticks() * 0.003) + 1) / 2
        color = (int (255 * pulse), 20, 147)
        offset = int(5 * math.sin(pygame.time.get_ticks() * 0.005))
        for dx, dy in [(-2,0),(2,0),(0,-2),(0,2)]:
            outline = title_font.render(title_text, True, BLACK)
            screen.blit(outline, ((width - outline.get_width()) // 2 + dx, 80 + dy))
        title = title_font.render(title_text, True, DARK_PINK)
        screen.blit(title, ((width - title.get_width()) // 2, 80))


        play_text = font.render("PLAY", True, WHITE)
        play_rect = play_text.get_rect(center=(width // 2, height //2 + 20))
        pygame.draw.rect(screen, DARK_PINK, play_rect.inflate(40, 20))
        screen.blit(play_text, play_rect)

        mouse_x, mouse_y = pygame.mouse.get_pos()

        head_x, head_y = snake_preview[-1]
        dx = mouse_x - head_x
        dy = mouse_y - head_y

        if abs(dx) > block_size or abs(dy) > block_size:
            if abs(dx) > abs(dy):
                head_x += block_size if dx > 0 else -block_size
            else:
                head_y += block_size if dy > 0 else -block_size

            snake_preview.append((head_x, head_y))
            snake_preview.pop(0)

        for i, (x, y) in enumerate(snake_preview):
            if i == len(snake_preview) - 1:
                px, py = snake_preview[i - 1]
                dx = x - px
                dy = y - py
                if dx > 0:
                    angle = -90
                elif dx < 0:
                    angle = 90
                elif dy > 0:
                    angle = 180
                elif dy < 0:
                    angle = 0
                else:
                    angle = 0

                rotated_head = pygame.transform.rotate(snake_head_img, angle)
                screen.blit(rotated_head, (x, y))
            else:
                pygame.draw.rect(screen, PINK, (x, y, block_size, block_size))

        pygame.display.update()
        clock.tick(10)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    menu_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    menu_running = False


opening_screen(high_score)

while  True:
    snake = Snake(block_size, play_x, play_y, snake_head_img)
    foods = []
    foods.append(Food(play_x, play_y, play_width, play_height, block_size, snake.body))
    last_food_spawn_time = time.time()
    score = 0
    running = True
    paused = False
    
    while running:
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    save_high_score(high_score)
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        snake.change_dir('UP')
                    elif event.key == pygame.K_DOWN:
                        snake.change_dir('DOWN')
                    elif event.key == pygame.K_LEFT:
                        snake.change_dir('LEFT')
                    elif event.key == pygame.K_RIGHT:
                         snake.change_dir('RIGHT')
                    elif event.key == pygame.K_p:
                        paused = not paused
                    elif paused and event.key in (pygame.K_RETURN, pygame.K_SPACE):
                        paused = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pause_button.collidepoint(event.pos):
                        paused = not paused
        grow = False
        if not paused:
            current_time = time.time()
            if current_time - last_food_spawn_time > FOOD_SPAWN_INTERVAL:
                if len(foods) <MAX_FOOD_ON_SCREEN:
                    new_food = Food(play_x, play_y, play_width, play_height, block_size, snake.body)
                    foods.append(new_food)
                last_food_spawn_time = current_time
                
            head_rect = pygame.Rect(snake.body[0][0], snake.body[0][1], block_size, block_size)
            foods_to_keep = []

            for food in foods:
                if food.is_expired():
                    food = Food(play_x, play_y, play_width, play_height, block_size, snake.body)

                if head_rect.colliderect(food.rect):
                    points_gained = food.points
                    score += points_gained
                    high_score = max(high_score, score)
                    if points_gained > 0:
                        grow = True 
                    elif points_gained < 0 and len(snake.body) > 1:
                        snake.body.pop()
                    continue
                
                foods_to_keep.append(food)
            foods = foods_to_keep

            snake.move(grow)

            x, y = snake.body[0]
            if (x < play_x or x >= play_x + play_width or y < play_y or y >= play_y + play_height or snake.body[0] in snake.body[1:]):
                if score > high_score:
                    high_score = score
                save_high_score(high_score)
                game_over_screen(score)
                break

            if score < 0:
                save_high_score(high_score)
                game_over_screen(score)
                break
            
            draw_background()
            draw_header(score, high_score)
            snake.draw(screen, PINK)
            for food in foods:
                food.draw(screen)
            
            draw_apple_list()
            draw_pause_button(paused)
            if paused:
                draw_pause_overlay()

            pygame.display.update()
            clock.tick(fps)
            

       
pygame.quit()
sys.exit()