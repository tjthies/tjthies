import sys # tools needed to exit game
import pygame 

from settings import Settings
from ship import Ship

class AlienInvasion():
    """Master class to manage game assets and behaviour"""

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Alien Invasion")

        # Load instance of ship
        self.ship = Ship(self)

        # Set background colour
        self.bg_colour = self.settings.bg_colour

    def run_game(self):
        """Start main loop for game"""
        while True:
            self._check_events()
            self.ship.update()
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        """Respond to key presses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # Move ship to the left & right
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:      
                    self.ship.moving_right = True
                if event.key == pygame.K_LEFT:      
                    self.ship.moving_left = True

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:      
                    self.ship.moving_right = False
                if event.key == pygame.K_LEFT:      
                    self.ship.moving_left = False                    

    def _update_screen(self):
        """Make the most recently drawn screen visible."""
        pygame.display.flip()
        # Redraw screen during each pass through the loop.
        self.screen.fill(self.bg_colour)
        self.ship.blitme()

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()