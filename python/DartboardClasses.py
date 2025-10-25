import math

class Polar_Rectangle:
    def __init__(self, radius1, radius2, theta1, theta2):
        self.xy_corners = []
        for radius in [radius1, radius2]:
            for theta in [theta1, theta2]:
                self.xy_corners.append((radius*math.cos(theta)))


class Dartboard:
    def __init__(self) -> None:
        self.screen
        self.all_rings = []
        self.all_rings.append(create_circle_of_polar_rectangles(100,200,0,math.pi/4))

    def draw_self(self, screen,size=1):
        for ring in all_rings:
            for polar_rectangle in ring:
                pygame.draw.polygon(screen, polygon_color, polygon_points, 0)

    def create_circle_of_polar_rectangles(self, radius1, radius2, theta1, theta2):
        polar_rectangles = [] 
        for i in range(1,(theta2-theta1)/2*math.pi):
            polar_rectangles.append(Polar_Rectangle(radius1, radius2, theta1*i,theta2*i))
        return polar_rectangles