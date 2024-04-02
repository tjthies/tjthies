import sys # tools needed to exit game
import pygame 

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion():
    """Master class to manage game assets and behaviour"""

    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        # Not full screen mode
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))

        # Full screen mode
        # self.screen = pygame.display.set_mode((0, 0),pygame.FULLSCREEN)
        # self.settings.screen_width = self.screen.get_rect().width
        # self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Alien Invasion")

        # Load instance of ship
        self.ship = Ship(self)

        # Load group of bullets
        self.bullets = pygame.sprite.Group()

        # Load fleet of aliens
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        # Set background colour
        self.bg_colour = self.settings.bg_colour

    def run_game(self):
        """Start main loop for game"""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_screen()
            self.clock.tick(60)

    def _check_events(self):
        """Respond to key presses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            # Move ship to the left & right
            elif event.type == pygame.KEYDOWN:
                self._check_key_down_events(event)
            elif event.type == pygame.KEYUP:
                self._check_key_up_events(event)
    
    def _check_key_down_events(self, event):
        """Respond to key presses"""
        if event.key == pygame.K_RIGHT:      
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:      
            self.ship.moving_left = True 
        elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _check_key_up_events(self, event):
        """Respond to key releases"""
        if event.key == pygame.K_RIGHT:      
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:      
            self.ship.moving_left = False 

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet) 

    def _update_bullets(self):
        """Update bullet position and delete bullets after they leave screen."""
        # Update bullet position
        self.bullets.update()

        # Remove bullets that have left top of screen
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    def _create_fleet(self):
        """Create fleet of aliens"""
        # Make alien and keep adding aliens until no room left.
        # Spacing between aliens is one alien width.
        alien = Alien(self)
        alien_width = alien.rect.width

        current_x = alien_width
        while current_x < (self.settings.screen_width - 2 * alien_width):
            new_alien = Alien(self)
            new_alien.x = current_x
            new_alien.rect.x = current_x
            self.aliens.add(new_alien)
            current_x += 2 * alien_width

    def _update_screen(self):
        """Make the most recently drawn screen visible."""
        # Redraw screen during each pass through the loop.
        self.screen.fill(self.bg_colour)
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        # Draw ship to screen
        self.ship.blitme()
        # Draw aliens to screen
        self.aliens.draw(self.screen)
        pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()