import math
import pygame.mouse
from clock import Circle
from numberIterator import Number
from stateTracker import State
from text import Text
from timeTracker import Timer


class Window:
    def __init__(self, monitor, settings):
        self.monitor = monitor
        self.width = self.monitor.width/2
        self.height = self.monitor.height/2

        self.settings = settings

        self.window = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        pygame.display.set_caption("time timer")
        self.mouse = (pygame.mouse.get_pos(), pygame.mouse.get_pressed()[0])

        self.size_divider = 2

        if self.height < self.width:
            circle_size = self.height/self.size_divider
        else:
            circle_size = self.width / self.size_divider
        self.circle = Circle(circle_size)
        self.circle_coord = [self.width/2-circle_size/2, self.height/2-circle_size/2]

        self.state = State()
        next(self.state)
        self.timer = Timer()
        self.set_time = 60*15

        numbers = Number()
        self.numbers = [Text(str(i//6), circle_size/10, [self.width/2+math.cos(math.radians(self.circle.get_usable_angle(i)))*circle_size/1.7, self.height/2+math.sin(math.radians(self.circle.get_usable_angle(i)))*circle_size/1.7]) for i in numbers]
        self.time_left = Text(f"{int(self.timer.get_time()//60)}:{int(self.timer.get_time()%60)}", circle_size/10, [self.width/2, self.height/10])

    def update(self):
        self.get_win_size()
        self.limit_win_size()
        self.get_mouse()
        self.update_circle_sizes()
        self.update_numbers()
        self.circle.update_polygon_size()
        self.time_left.update(self.circle.size / 10, [self.width / 2, self.height / 10])
        self.time_left.update_text(f"{int(self.timer.get_time()//60)}:{int(self.timer.get_time()%60)}")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    next(self.state)
                    if self.state.get_state() == "run":
                        self.get_time_from_angle()
                        self.timer.start(self.set_time)

        if self.state.get_state() == "set":
            if self.mouse[1]:
                self.circle.update([self.mouse[0][0]-self.circle_coord[0], self.mouse[0][1]-self.circle_coord[1]])
            self.get_time_from_angle()
            self.timer.start(self.set_time)
        elif self.state.get_state() == "run":
            self.circle.update([self.get_angle_from_time()])

    def draw(self):
        self.window.fill((255, 255, 255))
        self.circle.draw()
        self.time_left.draw(self.window)
        self.window.blit(self.circle.canvas, self.circle_coord)
        for i in self.numbers:
            i.draw(self.window)
        pygame.display.flip()
        pass

    def get_mouse(self):
        self.mouse = pygame.mouse.get_pos(), pygame.mouse.get_pressed()[0]

    def get_win_size(self):
        self.width, self.height = pygame.display.get_window_size()

    def limit_win_size(self):
        if self.width < 260:
            self.width = 260
            self.window = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)
        elif self.height < 420:
            self.height = 420
            self.window = pygame.display.set_mode((self.width, self.height), pygame.RESIZABLE)

    def update_circle_sizes(self):
        if self.height < self.width:
            circle_size = self.height/self.size_divider
        else:
            circle_size = self.width / self.size_divider

        self.circle.size = circle_size
        self.circle_coord = [self.width / 2 - circle_size / 2, self.height / 2 - circle_size / 2]

    def get_time_from_angle(self):
        read_angle = math.degrees(self.circle.angle)

        # convert to 360
        if read_angle < 0:
            read_angle = -read_angle
        else:
            read_angle = 180-read_angle+180

        # turn 90 degrees
        if read_angle >= 90:
            angle = read_angle - 90
        else:
            angle = 360 - (90-read_angle)

        self.set_time = angle*10

    def get_angle_from_time(self):
        angle = self.timer.get_time()/60*6

        # turn 90 degrees
        if angle <= 270:
            turned_angle = angle + 90
        else:
            turned_angle = angle - 270

        if turned_angle <= 180:
            final_angle = -turned_angle
        else:
            final_angle = 180-(turned_angle-180)

        return math.radians(final_angle)

    def update_numbers(self):
        number = Number()
        number = list(enumerate(number))
        iterations = len(list(enumerate(self.numbers)))
        for i in range(iterations):
            x_coord = self.width/2+math.cos(math.radians(self.circle.get_usable_angle(number[i][1])))*self.circle.size/1.7
            y_coord = self.height/2+math.sin(math.radians(self.circle.get_usable_angle(number[i][1])))*self.circle.size/1.7
            self.numbers[i].update(self.circle.size/10, [x_coord, y_coord])

