import pygame
from DartboardClasses import Dartboard, Dart
from PhysicsSimClasses import DartManager
import math

class DartboardSimulator:
    FPS = 60
    PREVIEW_RADIUS = Dart.MIN_RADIUS + Dart.RADIUS
    def __init__(self, dartboard_depth, screen_width=800, screen_height=800):
        pygame.init()
        #self.screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
        self.screen = pygame.display.set_mode((screen_width, screen_height))

        pygame.display.set_caption("PHYSICAL DIGITAL DARTS")

        self.clock = pygame.time.Clock()
        
        self.dartboard = Dartboard(self.screen, [0, 0, dartboard_depth]) # x and y are obselete
        self.dart_manager = DartManager(self.dartboard, self.screen)
        self.mouse_pos = (0,0)
        #font = pygame.font.SysFont('Arial', 40)
        #self.text_to_blit = font.render(f'x:0, y:0, z:0', True, (0, 0, 255))

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
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pitch = 90
                    yaw = 0
                    speed = 100
                    #With x as depth/default to yaw=0
                    #left_and_right_movement = 1 * math.cos(math.radians(yaw)) * math.sin(math.radians(pitch))
                    left_and_right_movement = speed * math.sin(math.radians(yaw)) * math.sin(math.radians(pitch))
                    up_and_down_movement = speed * math.cos(math.radians(pitch))

                    print(left_and_right_movement, up_and_down_movement)
                    
                    self.throw_dart([left_and_right_movement, up_and_down_movement, 1])
                else:
                    Dart.all_darts = []
            
            if should_throw_debug:
                self.debug_mouse_throw(event)

        if should_preview_debug:
            self.debug_mouse_preview()

        #if self.text_to_blit:
            #self.screen.blit(self.text_to_blit, (0, 0))

        pygame.display.update()
        return True
    
    def draw_dart_pos_preview(self, x, y):
        pygame.draw.circle(self.screen, Dart.COLOR, (x,y), self.PREVIEW_RADIUS)

    def debug_mouse_throw(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.dart_manager.throw_dart_using_mouse(self.mouse_pos[0], self.mouse_pos[1], 1, [0,100,2])

    def debug_mouse_preview(self):
        self.draw_dart_pos_preview(self.mouse_pos[0], self.mouse_pos[1])

    def throw_dart(self, exit_velocity):
        #font = pygame.font.SysFont('Arial', 40)
        #if self.magnitude_of_vector3(exit_velocity):
            #self.text_to_blit = font.render(f'l/r:{round(exit_velocity[0]/self.magnitude_of_vector3(exit_velocity),2)}, u/d:{round(exit_velocity[1]/self.magnitude_of_vector3(exit_velocity),2)}, depth:{round(exit_velocity[2]/self.magnitude_of_vector3(exit_velocity),2)}', True, (0, 0, 255))

        self.dart_manager.throw_dart([exit_velocity[0], exit_velocity[1], exit_velocity[2]])

    def magnitude_of_vector3(self, vector3):
        return math.sqrt(vector3[0]**2+vector3[1]**2+vector3[2]**2)

