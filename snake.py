import pygame

class Snake:
    def __init__(self, block_size, play_x, play_y, snake_head_img):
        self.block_size = block_size
        start_x = play_x + 5 * block_size
        start_y = play_y + 5 * block_size
        self.body = [
            [start_x, start_y],
            [start_x - block_size, start_y],
            [start_x - 2 * block_size, start_y]
        ]
        self.direction = 'RIGHT'
        self.change_to = 'RIGHT'  
        self.snake_head_img = snake_head_img

    def change_dir(self, dir):
        opposite_directions = {'UP': 'DOWN', 'DOWN': 'UP', 'LEFT': 'RIGHT', 'RIGHT': 'LEFT'}
        if dir != opposite_directions.get(self.direction):
            self.change_to = dir

    def move(self, grow_flag=False):
        self.direction = self.change_to
        head_x, head_y = self.body[0]

        if self.direction == "UP":
            head_y -= self.block_size
        elif self.direction == "DOWN":
            head_y += self.block_size
        elif self.direction == "LEFT":
            head_x -= self.block_size
        elif self.direction == "RIGHT":
            head_x += self.block_size

        new_head = [head_x, head_y]
        self.body.insert(0, new_head)

        if not grow_flag:
            self.body.pop()

    def draw(self, surface, color):
        for i, segment in enumerate(self.body):
            x, y = segment
            if i == 0:
                if self.direction == "UP":
                    rotated = pygame.transform.rotate(self.snake_head_img, 0)
                elif self.direction == "RIGHT":
                    rotated = pygame.transform.rotate(self.snake_head_img, -90)
                elif self.direction == "DOWN":
                    rotated = pygame.transform.rotate(self.snake_head_img, 180)
                elif self.direction == "LEFT":
                    rotated = pygame.transform.rotate(self.snake_head_img, 90)
                surface.blit(rotated, (x, y))
            else:
                rect = pygame.Rect(x, y, self.block_size, self.block_size)
                pygame.draw.rect(surface, color, rect)