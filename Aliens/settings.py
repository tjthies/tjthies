class Settings:
    """Store and handle all game settings for Alien Invasion"""

    def __init__(self):
        """Initialise game settings"""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_colour = (230, 230, 230)
        
        # Ship settings
        self.ship_speed = 15

        # Bullet settings
        self.bullet_speed = 5.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_colour = (60, 60, 60)
        self.bullets_allowed = 5