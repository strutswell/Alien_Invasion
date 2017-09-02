import pygame
from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self, ai_settings, screen):
        super(Ship, self).__init__()

        self.screen = screen
        self.ai_settings = ai_settings
        # load the ship image and get its rect?
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Start each new ship rect at the bottom center of the screen rect
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # store decimal value for ship position
        self.center = float(self.rect.centerx)
        self.bottom = float(self.rect.bottom)

        # moving left or right, up or down
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def center_ship(self):
        self.center = self.screen_rect.centerx
        self.bottom = self.screen_rect.bottom


    def update(self):
        """Update ship position based on moving flag"""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            # update the center, not the rect
            self.center += self.ai_settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed
        if self.moving_up and self.rect.bottom > (self.screen_rect.bottom - 50):
            self.bottom -= self.ai_settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.bottom += self.ai_settings.ship_speed

        # update rect based on the center
        self.rect.centerx = self.center
        self.rect.bottom = self.bottom



    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)
