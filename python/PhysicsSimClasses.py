from DartboardClasses import Dartboard, Dart

class DartManager:
    DART_GRAVITY = 9.8
    VELOCITY_SCALARS = (1,1,1)

    def __init__(self, screen):
        self.screen = screen

    def update(self):
        for dart in Dart.all_darts:
            dart.velocity[1] -= self.DART_GRAVITY
            dart.position[0] += dart.velocity[0] * self.VELOCITY_SCALARS[0]
            dart.position[1] += dart.velocity[1] * self.VELOCITY_SCALARS[1]
            dart.position[2] += dart.velocity[2] * self.VELOCITY_SCALARS[2]

    def throw_dart(self, x, y, z, exit_velocity):
        Dart(x, y, z, exit_velocity, self.screen)