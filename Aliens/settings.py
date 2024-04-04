class Settings:
    """Store and handle all game settings for Alien Invasion"""

    def __init__(self):
        """Initialise game settings"""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_colour = (230, 230, 230)
        
        # Ship settings
        self.ship_limit = 3

        # Bullet settings
        self.bullet_width = 5
        self.bullet_height = 15
        self.bullet_colour = (60, 60, 60)
        self.bullets_allowed = 8

        # Alien settings
        self.fleet_drop_speed = 10
        self.fleet_direction = 1

        # Set how quickly the game speeds up
        self.speed_increase = 1.1

        # Set how quickly alient point values increase
        self.score_scale = 1.5
        self.initialise_dynamic_settings()

    def initialise_dynamic_settings(self):
        """Initialise settings that change for each level."""
        self.ship_speed = 7
        self.bullet_speed = 3
        self.alien_speed = 1
        self.fleet_direction = 1
        self.alien_points = 5

    def increase_speed(self):
        """Increase game speed."""
        self.ship_speed *= self.speed_increase
        self.bullet_speed *= self.speed_increase
        self.alien_speed *= self.speed_increase
        self.fleet_direction *= self.speed_increase 

        self.alien_points = int(self.alien_points * self.score_scale)    