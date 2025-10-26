import pygame
from DartboardClasses import Dartboard, Dart
from PhysicsSimClasses import DartManager
import math

class DartboardSimulator:
    FPS = 60
    PREVIEW_RADIUS = Dart.MIN_RADIUS + Dart.RADIUS
    def __init__(self, dartboard_pos, screen_width=800, screen_height=800):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("PHYSICAL DIGITAL DARTS")

        self.clock = pygame.time.Clock()
        
        self.dartboard = Dartboard(self.screen, dartboard_pos)
        self.dart_manager = DartManager(self.dartboard, self.screen)
        self.mouse_pos = (0,0)
        #print(self.dartboard)

    def loop(self, should_throw_debug=False, should_preview_debug=False):
        self.screen.fill((96, 59, 42))
        
        self.dartboard.draw_self()
        Dart.draw_all(self.screen)
        self.dartboard.check_for_collisions(Dart.all_darts)
        self.dart_manager.update_dart_positions(self.clock.tick(self.FPS)/1000)

        if should_throw_debug or should_preview_debug:
            self.mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            
            if should_throw_debug:
                self.debug_mouse_throw(event)

        if should_preview_debug:
            self.debug_mouse_preview()

        pygame.display.update()
        return True
    
    def draw_dart_pos_preview(self, x, y):
        pygame.draw.circle(self.screen, Dart.COLOR, (x,y), self.PREVIEW_RADIUS)

    def debug_mouse_throw(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.dart_manager.throw_dart(self.mouse_pos[0], self.mouse_pos[1], 1, [0,100,2])

    def debug_mouse_preview(self):
        self.draw_dart_pos_preview(self.mouse_pos[0], self.mouse_pos[1])
