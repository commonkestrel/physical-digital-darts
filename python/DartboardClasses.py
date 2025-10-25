import math
import pygame

class Dart:
    RADIUS = 40
    MIN_RADIUS = 10
    COLOR = (100,100,255)
    LIFETIME = 100
    all_darts = []
    def __init__(self, x, y, z, exit_velocity, screen, dartboard):
        Dart.all_darts.append(self)
        self.dartboard = dartboard
        self.should_decay = False
        self.velocity = exit_velocity
        self.velocity[1] = -self.velocity[1]
        self.lifetime = Dart.LIFETIME
        self.screen = screen
        self.starting_distance_from_dartboard = z #CURRENTLY DOESN'T ACTUALLY REPRESENT DISTANCE FROM DARTBOARD ON LAUNCH
        self.position = [x, y, z]

    def draw_self(self):
        if self.has_reached_dartboard_depth():
            self.should_decay = True

        if self.should_decay and self.lifetime > 0:
            self.lifetime -= 1

        if self.should_decay and self.lifetime <= 0:
            Dart.all_darts.remove(self)
        
        percent_of_distance_traveled = (self.position[2]-self.starting_distance_from_dartboard)/(self.dartboard.position[2]-self.starting_distance_from_dartboard)
        pygame.draw.circle(self.screen, self.COLOR, self.position[:2], self.MIN_RADIUS+self.RADIUS*(1-percent_of_distance_traveled))

    def has_reached_dartboard_depth(self):
        at_or_past_dartboard = self.position[2] >= self.dartboard.position[2]
        return at_or_past_dartboard
       
    def __repr__(self):
        return "Dart Coordinates: " + str(self.position)
    
    @staticmethod
    def draw_all(screen):
        for dart in Dart.all_darts:
            dart.draw_self()

class Polar_Rectangle:
    HIT_COLOR = (0,0,255)
    def __init__(self, radius1, radius2, theta1, theta2, color, dartboard, screen):
        self.screen = screen
        self.dartboard = dartboard
        self.non_hit_color = color
        self.color = self.non_hit_color
        self.xy_corners = []
        self.xy_corners.append((radius1*math.cos(theta1), radius1*math.sin(theta1)))
        self.xy_corners.append((radius1*math.cos(theta2), radius1*math.sin(theta2)))
        self.xy_corners.append((radius2*math.cos(theta2), radius2*math.sin(theta2)))
        self.xy_corners.append((radius2*math.cos(theta1), radius2*math.sin(theta1)))
        self.xy_corners = Dartboard.cartesian_coordinates_to_pygame_coordinates(self.xy_corners, screen)

    def draw_self(self):
        pygame.draw.polygon(self.screen, self.color, self.xy_corners, 0)

    def check_for_collision(self, darts):
        has_collided = False
        for dart in darts:
            has_collided = self.point_in_polygon(dart.position, self.xy_corners)
            if has_collided:
                self.when_projected_collide()
                if dart.has_reached_dartboard_depth():
                    self.when_collide(dart)
                    #return True #Collided including the depth
                return True #Collided only in x-y projection
        self.color = self.non_hit_color
        return False
    
    def when_collide(self, dart):
        #print(f'Collided with: {dart}')
        pass

    def when_projected_collide(self):
        self.color = self.HIT_COLOR
    
    def point_in_polygon(self, point, polygon):
        num_vertices = len(polygon)
        x, y = point[0], point[1]
        inside = False

        # Store the first point in the polygon and initialize the second point
        p1 = polygon[0]

        # Loop through each edge in the polygon
        for i in range(1, num_vertices + 1):
            # Get the next point in the polygon
            p2 = polygon[i % num_vertices]

            # Check if the point is above the minimum y coordinate of the edge
            if y > min(p1[1], p2[1]):
                # Check if the point is below the maximum y coordinate of the edge
                if y <= max(p1[1], p2[1]):
                    # Check if the point is to the left of the maximum x coordinate of the edge
                    if x <= max(p1[0], p2[0]):
                        # Calculate the x-intersection of the line connecting the point to the edge
                        x_intersection = (y - p1[1]) * (p2[0] - p1[0]) / (p2[1] - p1[1]) + p1[0]

                        # Check if the point is on the same line as the edge or to the left of the x-intersection
                        if p1[0] == p2[0] or x <= x_intersection:
                            # Flip the inside flag
                            inside = not inside

            # Store the current point as the first point for the next iteration
            p1 = p2

        # Return the value of the inside flag
        return inside


    def __repr__(self):
        return "Polar Rectangle Corners: " + str(self.xy_corners)
    
class Polar_Circle:
    def __init__(self, list_of_polar_rectangles, dartboard, screen):
        self.screen = screen
        self.dartboard = dartboard
        self.list_of_polar_rectangles = list_of_polar_rectangles

    def draw_self(self):
        for polar_rectangle in self.list_of_polar_rectangles:
            polar_rectangle.draw_self()

    def check_for_collision(self, darts):
        any_collisions = any([polar_rectangle.check_for_collision(darts) for polar_rectangle in self.list_of_polar_rectangles])
        if any_collisions:
            for polar_rectangle in self.list_of_polar_rectangles:
                polar_rectangle.when_projected_collide()
                
    def __repr__(self):
        return "Polar Circle: " + str(self.list_of_polar_rectangles)

class Dartboard:
    GREEN = (0,255,0)
    RED = (255,0,0)
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    THICK_RING_THICKNESS = 100
    THIN_RING_THICKNESS = 75
    BULLSEYE_THICKNESS = 25
    PER_REGION_DELTA_THETA = math.pi/10
    THETA_OFFSET = math.pi/20
    #DARTBOARD_SIZE - THIN_RING_THICKNESS*2 - THICK_RING_THICKNESS*2 should = BULLSEYE THICKNESS

    def __init__(self, screen, position) -> None:
        self.DARTBOARD_SIZE = self.THIN_RING_THICKNESS*2 + self.THICK_RING_THICKNESS*2 + self.BULLSEYE_THICKNESS*2
        self.screen = screen
        self.position = position
        self.all_rings = []
        self.all_rings.append(self.create_circle_of_polar_rectangles(self.DARTBOARD_SIZE-self.THIN_RING_THICKNESS,self.DARTBOARD_SIZE,self.PER_REGION_DELTA_THETA,(Dartboard.RED, Dartboard.GREEN)))
        self.all_rings.append(self.create_circle_of_polar_rectangles(self.DARTBOARD_SIZE-self.THIN_RING_THICKNESS-self.THICK_RING_THICKNESS,self.DARTBOARD_SIZE-self.THIN_RING_THICKNESS,self.PER_REGION_DELTA_THETA,(Dartboard.BLACK, Dartboard.WHITE)))
        self.all_rings.append(self.create_circle_of_polar_rectangles(self.DARTBOARD_SIZE-self.THIN_RING_THICKNESS-self.THICK_RING_THICKNESS-self.THIN_RING_THICKNESS,self.DARTBOARD_SIZE-self.THIN_RING_THICKNESS-self.THICK_RING_THICKNESS,self.PER_REGION_DELTA_THETA,(Dartboard.RED, Dartboard.GREEN)))
        self.all_rings.append(self.create_circle_of_polar_rectangles(self.DARTBOARD_SIZE-self.THIN_RING_THICKNESS-self.THICK_RING_THICKNESS-self.THIN_RING_THICKNESS-self.THICK_RING_THICKNESS,self.DARTBOARD_SIZE-self.THIN_RING_THICKNESS-self.THICK_RING_THICKNESS-self.THIN_RING_THICKNESS,self.PER_REGION_DELTA_THETA,(Dartboard.BLACK, Dartboard.WHITE)))
        self.all_rings.append([Polar_Circle(self.create_circle_of_polar_rectangles(self.DARTBOARD_SIZE-self.THIN_RING_THICKNESS-self.THICK_RING_THICKNESS-self.THIN_RING_THICKNESS-self.THICK_RING_THICKNESS-self.BULLSEYE_THICKNESS,self.DARTBOARD_SIZE-self.THIN_RING_THICKNESS-self.THICK_RING_THICKNESS-self.THIN_RING_THICKNESS-self.THICK_RING_THICKNESS,self.PER_REGION_DELTA_THETA,(Dartboard.GREEN, Dartboard.GREEN)),self,self.screen)])
        self.all_rings.append([Polar_Circle(self.create_circle_of_polar_rectangles(0,self.DARTBOARD_SIZE-self.THIN_RING_THICKNESS-self.THICK_RING_THICKNESS-self.THIN_RING_THICKNESS-self.THICK_RING_THICKNESS-self.BULLSEYE_THICKNESS,self.PER_REGION_DELTA_THETA,(Dartboard.RED, Dartboard.RED)),self, self.screen)])

    def check_for_collisions(self, darts):
        for ring in self.all_rings:
            for polar_rectangle in ring:
                polar_rectangle.check_for_collision(darts)

    def draw_self(self):
        for ring in self.all_rings:
            for polar_rectangle in ring:
                polar_rectangle.draw_self()
    
    def create_circle_of_polar_rectangles(self, radius1, radius2, delta_theta, colors_to_alternate_between):
        polar_rectangles = [] 
        for i in range(int(2*math.pi/delta_theta)):
            polar_rectangles.append(Polar_Rectangle(radius1, radius2, delta_theta*i+self.THETA_OFFSET, delta_theta*(i+1)+self.THETA_OFFSET, colors_to_alternate_between[i%2], self, self.screen))
        return polar_rectangles
    
    @staticmethod
    def cartesian_coordinates_to_pygame_coordinates(coordinates, screen):
        return [(screen.get_width()//2+c[0], screen.get_height()//2-c[1]) for c in coordinates]
    
    def __repr__(self):
        return "All Rings: " + str(self.all_rings)