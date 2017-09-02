import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage bullets"""

    def __init__(self, ai_settings, screen, ship):
        super(Bullet, self).__init__()
        self.screen = screen

        # create bullet rect at (0, 0) then set correct position
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.center = ship.rect.center
        self.rect.top = ship.rect.top

        # store bullet position as decimal
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_colour
        self.speed = ai_settings.bullet_speed

    def update(self):
        """Move bullet up the screen"""
        # update decimal position
        self.y -= self.speed
        # update rect position
        self.rect.y = self.y

    def draw_bullet(self):
        """Draw bullet on screen"""
        pygame.draw.rect(self.screen, self.color, self.rect)
