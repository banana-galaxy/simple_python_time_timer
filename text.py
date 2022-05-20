import pygame.font


class Text:
    def __init__(self, text, size, coords: list, font = "Arial"):
        self.font_text = font
        self.font = pygame.font.SysFont(font, int(size))
        self.text = text
        self.rendered = self.font.render(text, True, (0, 0, 0))
        self.coords = coords

    def update(self, size, coords: list):
        self.font = pygame.font.SysFont(self.font_text, int(size))
        self.rendered = self.font.render(self.text, True, (0, 0, 0))
        self.coords = coords

    def draw(self, surface):
        x, y = self.rendered.get_size()
        surface.blit(self.rendered, (self.coords[0]-x/2, self.coords[1]-y/2))
