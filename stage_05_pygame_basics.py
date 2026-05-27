import pygame # type:ignore

# Initialize pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Colors (R, G, B)
WHITE  = (255, 255, 255)
BLACK  = (0,   0,   0)
RED    = (255, 0,   0)
GREEN  = (0,   255, 0)
BLUE   = (0,   0,   255)
YELLOW = (255, 255, 0)

# Create game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("VisionSlice - Pygame Basics")

# Clock for FPS control
clock = pygame.time.Clock()

# Font for text
font_large = pygame.font.SysFont("Arial", 60)
font_small = pygame.font.SysFont("Arial", 30)

# Game loop
running = True

while running:

    # 1 - Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False

    # 2 - Draw background
    screen.fill(BLACK)

    # 3 - Draw shapes
    pygame.draw.circle(screen, RED,    (200, 360), 60)
    pygame.draw.circle(screen, GREEN,  (500, 360), 60)
    pygame.draw.circle(screen, YELLOW, (800, 360), 60)
    pygame.draw.rect(screen,   BLUE,   (1000, 300, 120, 120))

    # 4 - Draw text
    title = font_large.render("VisionSlice AI", True, WHITE)
    subtitle = font_small.render("Press Q to quit", True, WHITE)
    screen.blit(title,    (440, 100))
    screen.blit(subtitle, (540, 200))

    # 5 - Draw FPS counter
    fps_text = font_small.render(f"FPS: {int(clock.get_fps())}", True, WHITE)
    screen.blit(fps_text, (20, 20))

    # 6 - Update display
    pygame.display.flip()

    # 7 - Control FPS
    clock.tick(FPS)

# Cleanup
pygame.quit()