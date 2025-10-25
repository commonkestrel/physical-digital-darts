import pygame
from DartboardClasses import Dartboard, Dart
from PhysicsSimClasses import DartManager
import math

class DartboardSimulator:
    FPS = 60
    def __init__(self, dartboard_pos, screen_width=800, screen_height=800):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("PHYSICAL DIGITAL DARTS")

        self.clock = pygame.time.Clock()
        
        self.dartboard = Dartboard(self.screen, dartboard_pos)
        self.dart_manager = DartManager(self.dartboard, self.screen)
        print(self.dartboard)

    def loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                self.dart_manager.throw_dart(mouse_x, mouse_y, 1, [0,100,2])

        self.screen.fill((96, 59, 42))
        self.dartboard.draw_self()
        Dart.draw_all(self.screen)
        self.dartboard.check_for_collisions(Dart.all_darts)
        self.dart_manager.update_dart_positions(self.clock.tick(self.FPS)/1000)

        pygame.display.update()
        return True
