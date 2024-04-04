class GameStats:
    """Tracks game statistics for alien invasion"""

    def __init__(self, ai_game):
        """Initialise statistics"""
        self.settings = ai_game.settings
        self.reset_stats()

    def reset_stats(self):
        """Initialise statistics that can change during the game."""
        self.ships_available = self.settings.ship_limit
        self.score = 0