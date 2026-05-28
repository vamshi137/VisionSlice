import pygame # type:ignore
import random

# Initialize pygame
pygame.init()

# Screen settings
SCREEN_WIDTH  = 1280
SCREEN_HEIGHT = 720
FPS           = 60

# Colors
WHITE  = (255, 255, 255)
BLACK  = (0,   0,   0)
RED    = (255, 50,  50)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN  = (0,   200, 0)
PINK   = (255, 100, 150)

# Fruit data
FRUITS = [
    {"name": "apple",      "color": RED,    "radius": 40},
    {"name": "orange",     "color": ORANGE, "radius": 45},
    {"name": "watermelon", "color": GREEN,  "radius": 55},
    {"name": "banana",     "color": YELLOW, "radius": 35},
    {"name": "kiwi",       "color": PINK,   "radius": 30},
]

# Fruit class
class Fruit:

    def __init__(self):
        self.reset()

    def reset(self):
        fruit_data   = random.choice(FRUITS)
        self.name    = fruit_data["name"]
        self.color   = fruit_data["color"]
        self.radius  = fruit_data["radius"]
        self.x       = random.randint(100, SCREEN_WIDTH - 100)
        self.y       = -self.radius
        self.speed_x = random.uniform(-2, 2)
        self.speed_y = random.uniform(3, 7)
        self.gravity = 0.2
        self.sliced  = False

    def update(self):
        self.speed_y += self.gravity
        self.x       += self.speed_x
        self.y       += self.speed_y

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(screen, WHITE,      (int(self.x), int(self.y)), self.radius, 3)

    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT + self.radius + 50


# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("VisionSlice - Fruit System")
clock  = pygame.time.Clock()
font   = pygame.font.SysFont("Arial", 30)

# Fruit list and spawn timer
fruits      = []
spawn_timer = 0
SPAWN_DELAY = 90

# Game loop
running = True

while running:

    # 1 - Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False

    # 2 - Spawn fruits
    spawn_timer += 1
    if spawn_timer >= SPAWN_DELAY:
        fruits.append(Fruit())
        spawn_timer = 0

    # 3 - Update fruits
    for fruit in fruits:
        fruit.update()

    # 4 - Remove off screen fruits
    fruits = [f for f in fruits if not f.is_off_screen()]

    # 5 - Draw background
    screen.fill(BLACK)

    # 6 - Draw fruits
    for fruit in fruits:
        fruit.draw(screen)

    # 7 - Draw fruit count
    count_text = font.render(f"Fruits on screen: {len(fruits)}", True, WHITE)
    screen.blit(count_text, (20, 20))

    # 8 - Update display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()