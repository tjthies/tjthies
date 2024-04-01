class Settings:
    """Store and handle all game settings for Alien Invasion"""

    def __init__(self):
        """Initialise game settings"""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_colour = (230, 230, 230)
        
        # Ship settings
        self.ship_speed = 12