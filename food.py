import pygame
import random
import time

FOOD_TYPES = {
    "normal": { 
        "image": "apple.png",
        "score": 1,
        "size": 25
    },
    "golden": {
        "image": "golden_apple.png",
        "score": 5,
        "size": 30,
        "duration": 5  
    },
    "rotten": {
        "image": "rotten_apple.png",
        "score": -1,
        "size": 25,
        "duration": 7  
}
}

class Food:
    def __init__(self, play_x, play_y, play_width, play_height, block_size, snake_body):
        self.block_size = block_size
        self.spawn_time = time.time()
        
        self.type = random.choice(list(FOOD_TYPES.keys()))
        config = FOOD_TYPES[self.type]

        self.points = config["score"]
        self.food_size = config["size"]
        self.duration = config.get("duration", None)
        
        while True:
            x = random.randrange(play_x, play_x + play_width, block_size)
            y = random.randrange(play_y, play_y + play_height, block_size)
            if [x, y] not in snake_body:
                break
        self.position = [x, y]
        self.rect = pygame.Rect(self.position[0], self.position[1], block_size, block_size)
        self.image = pygame.image.load(config["image"]).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.food_size, self.food_size))

    def is_expired(self):
        if self.duration is None:
            return False
        return (time.time() - self.spawn_time) > self.duration 
        
    def draw(self, surface):
        elapsed = time.time() - self.spawn_time
        bounce_scale = 1.0
        size = self.food_size
        
        if elapsed < 0.3:
            bounce_scale = 1.2 - (elapsed * 0.6) 
            size = int(self.food_size * bounce_scale)
            
        scaled_image = pygame.transform.scale(self.image, (size, size))

        offset = (size - self.block_size) // 2
        draw_x = self.position[0] - offset
        draw_y = self.position[1] - offset

        surface.blit(scaled_image, (draw_x, draw_y))