class Settings:
    """Store and handle all game settings for Alien Invasion"""

    def __init__(self):
        """Initialise game settings"""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_colour = (230, 230, 230)
        
        # Ship settings
        self.ship_speed = 5
        self.ship_limit = 3

        # Bullet settings
        self.bullet_speed = 20
        self.bullet_width = 30
        self.bullet_height = 15
        self.bullet_colour = (60, 60, 60)
        self.bullets_allowed = 5

        # Alien settings
        self.alien_speed = 5
        self.fleet_drop_speed = 50
        self.fleet_direction = 1