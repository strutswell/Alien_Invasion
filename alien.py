import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien ship."""

    def __init__(self, ai_settings, screen):
        """Initialize the alien and set it's starting position"""
        super(Alien, self).__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # load the alien image
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # start each new alien near top of screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # store the alien's exact position
        self.x = float(self.rect.x)

    def blitme(self):
        """Draw the alien at its current location"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Move the alien right or left"""
        self.x += (self.ai_settings.alien_speed * self.ai_settings.fleet_direction)
        self.rect.x = self.x

    def check_edges(self):
        """Return true if alien is at edge of screen"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True
