import pygame

# Initialize Pygame
pygame.init()

# Screen dimensions and setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("My Pygame Game")

# Clock for controlling frame rate
clock = pygame.time.Clock()
FPS = 60 # Frames per second

# Game loop flag
running = True

# Game loop
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0, 0, 0))
    quad_points = [(100, 100), (300, 150), (250, 300), (50, 250)]
    pygame.draw.polygon(screen, (255,255,255), quad_points)

    


    # Update the display
    pygame.display.update()

    # Control frame rate
    clock.tick(FPS)

# Quit Pygame
pygame.quit()