import math
import pygame
from degreeIterator import Degrees


class Polygon:
    def __init__(self, size):
        self.coords = [[0, size / 2], [size / 2, size / 2], [size / 2, 0], [size, 0], [size, size], [0, size]]
        self.square = [[size, 0], [size, size], [0, size], [0, 0]]
        self.angles = [[-0.1, -90], [0.0, 90], [90.0, 180.0], [-90.0, -180]]
        self.angle = math.radians(-180)

    def update(self, size, angle):
        self.angle = angle
        self.coords[0] = [size / 2 + math.cos(angle) * (size / 2), size / 2 + math.sin(angle) * (size / 2)]
        read_angle = math.degrees(angle)
        self.coords = self.coords[:3]
        for i, x in enumerate(self.angles):
            if x[0] <= read_angle <= x[1] or x[0] >= read_angle >= x[1]:
                for y in self.square[0:i + 1]:
                    self.coords.append(y)
                break

    def draw(self, surface):
        pygame.draw.polygon(surface, (255, 255, 255), self.coords)

    def update_size(self, size):
        self.coords = [[size / 2 + math.cos(self.angle) * (size / 2), size / 2 + math.sin(self.angle) * (size / 2)], [size / 2, size / 2], [size / 2, 0]]
        self.square = [[size, 0], [size, size], [0, size], [0, 0]]

class Circle:
    def __init__(self, size):
        self.size = size
        self.canvas = pygame.Surface((self.size, self.size))
        self.pointer = [0, 0]
        self.angle = 180
        self.polygon = Polygon(self.size)
        self.data = []
        self.update([math.radians(-180)])

    def update(self, data: list):
        self.data = data
        if self.canvas.get_size() != self.size:
            self.canvas = pygame.Surface((self.size, self.size))
            self.polygon.update_size(self.size)

        if len(data) == 2:
            self.angle = self.get_mouse_angle(data)
            self.snap_angle()
        elif len(data) == 1:
            self.angle = data[0]

        self.polygon.update(self.size, self.angle)

    def draw(self):
        self.canvas.fill((255, 255, 255))
        pygame.draw.circle(self.canvas, (255, 0, 50), (self.size / 2, self.size / 2), self.size / 2)
        self.polygon.draw(self.canvas)

    def update_polygon_size(self):
        self.polygon.update_size(self.size)
        self.update(self.data)

    def get_mouse_angle(self, mouse):
        dx = mouse[0] - self.size / 2
        dy = mouse[1] - self.size / 2
        rad = math.atan2(dy, dx)
        return rad

    def get_read_angle(self, angle = -1):
        if angle == -1:
            angle = self.angle
        read_angle = math.degrees(angle)

        # convert to 360
        if read_angle < 0:
            read_angle = -read_angle
        else:
            read_angle = 180 - read_angle + 180

        # turn 90 degrees
        if read_angle >= 90:
            angle = read_angle - 90
        else:
            angle = 360 - (90 - read_angle)

        return angle

    def get_usable_angle(self, angle):
        if angle <= 270:
            turned_angle = angle + 90
        else:
            turned_angle = angle - 270

        if turned_angle <= 180:
            final_angle = -turned_angle
        else:
            final_angle = 180-(turned_angle-180)

        return final_angle

    def snap_angle(self):
        angle = self.get_read_angle()
        degrees = Degrees()

        for i in degrees:
            if i[0] <= angle <= i[1]:
                d0 = angle - i[0]
                d1 = i[1] - angle
                d = abs(d0-d1)
                if d >= 15:
                    if d0 > d1:
                        final_angle = i[1]
                    elif i[0] == 0:
                        final_angle = angle
                    else:
                        final_angle = i[0]
                else:
                    final_angle = angle
                break

        usable_angle = self.get_usable_angle(final_angle)

        self.angle = math.radians(usable_angle)