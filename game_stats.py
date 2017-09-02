class GameStats():
    """Track stats for the game"""

    def __init__(self, ai_settings):
        """Init the stats"""
        self.ai_settings = ai_settings
        self.reset_stats()
        self.game_active = False
        self.high_score = 0

    def reset_stats(self):
        """Init stats that can change during the game"""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1


