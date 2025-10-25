import pygame
from DartboardClasses import Dartboard, Polar_Rectangle, Dart
from PhysicsSimClasses import DartManager
import math

# Initialize Pygame
pygame.init()

# Screen dimensions and setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("PHYSICAL DIGITAL DARTS")

# Clock for controlling frame rate
clock = pygame.time.Clock()
FPS = 60 # Frames per second
dartboard = Dartboard(screen, (0,3,10))
dart_manager = DartManager(dartboard, screen)
print(dartboard)


# Game loop flag
running = True

# Game loop
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Get the mouse position at the time of the click
            mouse_x, mouse_y = event.pos
            dart_manager.throw_dart(mouse_x, mouse_y, 1, [0,100,2])

    screen.fill((0, 0, 0))
    dartboard.draw_self()
    Dart.draw_all(screen)
    dartboard.check_for_collisions(Dart.all_darts)
    dart_manager.update_dart_positions(clock.tick(FPS)/1000)

    # Update the display
    pygame.display.update()

    # Control frame rate
    

# Quit Pygame
pygame.quit()