import sys # tools needed to exit game
import pygame 
from time import sleep

from settings import Settings
from game_stats import GameStats
from ship import Ship
from bullet import Bullet
from alien import Alien
from button import Button
from scoreboard import Scoreboard

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

        # Create instance of game stats
        self.stats = GameStats(self)
        self.scoreboard = Scoreboard(self)

        # Load instance of ship
        self.ship = Ship(self)

        # Load group of bullets
        self.bullets = pygame.sprite.Group()

        # Load fleet of aliens
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        # Set background colour
        self.bg_colour = self.settings.bg_colour

        # Start AI in an inactive state.
        self.game_active = False

        # Make a play button.
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Start main loop for game"""
        while True:
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()

            self._update_screen()
            self.clock.tick(120)

    def _check_events(self):
        """Respond to key presses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.stats.save_high_score()
                sys.exit()
            # Move ship to the left & right
            elif event.type == pygame.KEYDOWN:
                self._check_key_down_events(event)
            elif event.type == pygame.KEYUP:
                self._check_key_up_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _play_game(self):
        """Start playing the game after user input."""
        # Reset game statistics.
        self.stats.reset_stats()
        self.scoreboard.prep_score()
        self.scoreboard.prep_level()
        self.scoreboard.prep_ships()
        self.game_active = True

        # Remove remaining aliens and bullets.
        self.bullets.empty()
        self.aliens.empty()

        # Create a new fleet and center the ship.
        self._create_fleet()
        self.ship.centre_ship()

        # Hide mouse cursor
        pygame.mouse.set_visible(False)  
             
    def _check_play_button(self, mouse_pos):
        """Start new game when player clicks Play button."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            # Reset game settings
            self.settings.initialise_dynamic_settings() 
            self._play_game()
    
    def _check_key_down_events(self, event):
        """Respond to key presses"""
        if event.key == pygame.K_RIGHT:      
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:      
            self.ship.moving_left = True 
        elif event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
            self.stats.save_high_score()
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_p:
            self._play_game()

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

        # Remove bullets and aliens that have collided
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Check if bullets have hit aliens"""
        # If yes, remove bullet and alien
        collisions = pygame.sprite.groupcollide(
                self.bullets, self.aliens, True, True)
        
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.scoreboard.prep_score()
            self.scoreboard.check_high_score()

        # Destroy existing bullets and create new fleet.
        if not self.aliens:
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level
            self.stats.level += 1
            self.scoreboard.prep_level()

    def _create_fleet(self):
        """Create fleet of aliens"""
        # Make alien and keep adding aliens until no room left.
        # Spacing between aliens is one alien width and one alien height.
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        current_x,  current_y = alien_width, alien_height
        while current_y < (self.settings.screen_height - 3 * alien_height):
            while current_x < (self.settings.screen_width - 2 * alien_width):
                self._create_alien(current_x,current_y)
                current_x += 2 * alien_width

            # Row finished; reset x value and increment y value.
            current_x = alien_width
            current_y += 2* alien_height

    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the fleet"""
        new_alien = Alien(self)
        new_alien.x, new_alien.y = x_position, y_position
        new_alien.rect.x, new_alien.rect.y = x_position, y_position
        self.aliens.add(new_alien)

    def _update_aliens(self):
        """Update the position of all aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update()

        # Detect alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            print("Ship hit!!!")
            self._ship_hit()

        # Check for aliens hitting the bottom of the screen
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        """Respond if any aliens reach a screen edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """Drop the alien fleet and change its direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

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

        # Show score
        self.scoreboard.show_score()

        # Draw play button if the game is inactive.
        if not self.game_active:
            self.play_button.draw_button()

        pygame.display.flip()

    def _ship_hit(self):
        """Respond to a ship being hit"""
        # Decrement ships available
        if self.stats.ships_available > 0:
            self.stats.ships_available -= 1
            self.scoreboard.prep_ships()

            # Remove any remaining bullets and aliens.
            self.bullets.empty()
            self.aliens.empty()

            # Create new alien fleet and centre ship.
            self._create_fleet()
            self.ship.centre_ship()

            # Pause
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)

    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Treat this the same as a ship being hit.
                self._ship_hit()
                break 

if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = AlienInvasion()
    ai.run_game()