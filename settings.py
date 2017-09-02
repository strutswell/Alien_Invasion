class Settings():
    """A class to store all settings for Alien Invasion!"""

    def __init__(self):
        """Init the game's static settings"""
        # Screen settings
        self.screen_width = 800
        self.screen_height = 600
        self.bg_colour = (230, 230, 230)
        self.ship_limit = 3
        self.fleet_drop_speed = 15

        # bullet settings
        self.bullet_width = 6
        self.bullet_height = 12
        self.bullet_colour = (65, 50, 30)
        self.bullets_allowed = 6

        self.speedup_scale = 1.1
        self.score_scale = 1.2

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        # speed settings
        self.ship_speed = 0.8

        self.bullet_speed = 0.7
        self.alien_speed = 0.6
        # fleet direction of 1 is right, -1 is left
        self.fleet_direction = 1

        self.alien_points = 25


    def increase_speed(self):
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
