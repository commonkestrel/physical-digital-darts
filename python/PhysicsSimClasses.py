from DartboardClasses import Dartboard, Dart
import pygame

class DartManager:
    DART_GRAVITY = -.98
    VELOCITY_SCALARS = (1,1,1)

    def __init__(self, dartboard, screen):
        self.screen = screen
        self.dartboard = dartboard

    def update_dart_positions(self, deltaTime):
        for dart in Dart.all_darts:
            if not dart.should_decay:
                dart.velocity[1] -= self.DART_GRAVITY
                dart.position[0] += dart.velocity[0] * self.VELOCITY_SCALARS[0] * deltaTime
                dart.position[1] += dart.velocity[1] * self.VELOCITY_SCALARS[1] * deltaTime
                dart.position[2] += dart.velocity[2] * self.VELOCITY_SCALARS[2] * deltaTime
                #print(dart)

    def throw_dart(self, exit_velocity):
        Dart(self.screen.get_width()//2, self.screen.get_height()//2, 1, exit_velocity, self.screen, self.dartboard)

    def throw_dart_using_mouse(self, x, y, z, exit_velocity):
        Dart(x, y, z, exit_velocity, self.screen, self.dartboard)
