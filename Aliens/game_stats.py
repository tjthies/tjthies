from pathlib import Path

class GameStats:
    """Tracks game statistics for alien invasion"""

    def __init__(self, ai_game):
        """Initialise statistics"""
        self.settings = ai_game.settings
        self.reset_stats()
        
        # Load high score saved from file
        self.high_score_path = Path('high_score.txt')
        self._read_high_score()
        

    def reset_stats(self):
        """Initialise statistics that can change during the game."""
        self.ships_available = self.settings.ship_limit
        self.score = 0
        self.level = 1

    def _read_high_score(self):
        """Load in a previous high score if file is saved."""
        try:
            prev_high_score = int(self.high_score_path.read_text())
            self.high_score = prev_high_score
        except:
            self.high_score = 0

    def save_high_score(self):
        """Save high score when game is ended."""
        self.high_score_path.write_text(str(round(self.high_score, -1)))
        
