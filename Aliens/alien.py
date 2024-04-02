import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Class to represent a single alien in the fleet"""

    def __init__(self, ai_game):
        """Initialise alien and set starting position"""
        super().__init__()
        self.screen = ai_game.screen

        # Load the alien image and set its rect attribute
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        # Initialise each new alien at the top of the screen
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Store aliens exact horizontal position
        self.x = float(self.rect.x)