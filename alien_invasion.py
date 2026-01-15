# Test

import sys  # Use tools in sys to exit the game when the player quits
from time import sleep

import pygame  # Contains functionality to make a game

from settings import Settings
from game_stats import GameStats
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien

class AlienInvasion:
    """Overall class to manage game assets and behaviour."""
    
    def __init__(self):
        """Initialise the game, and create game resources."""

        # Initialise the imported pygame modules
        pygame.init()

        # Set the title of the game window
        pygame.display.set_caption("Alien Invasion")

        # Create a Clock object to manage how fast the screen updates (frame rate)
        self.clock = pygame.time.Clock()

        self.settings = Settings()

        # Create an instance to store game statistics
        self.stats = GameStats(self)

        # Set the dimensions of the game window and create the display surface
        # Surface: part of the screen where a game element can be displayed
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))

        # Create an instance of ship
        # One parameter: instance of AlienInvasion
        # self argument refers to current instance of AlienInvasion
        self.ship = Ship(self)

        # Create the group that holds the bullets
        self.bullets = pygame.sprite.Group()

        # Create the group that holds the aliens
        self.aliens = pygame.sprite.Group()

        # Create the initial fleet of aliens
        self._create_fleet()

        # Start Alien Invasion in an inactive state
        self.game_active = False

        # Make the Play button.
        self.play_button = Button(self, "Play")


    def run_game(self):
        """Start the main loop for the game."""
        
        # Event: action that the user performs while playing the game, key, mouse press

        while True:
            # Call methods game
            self._check_events()

            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
        
            self._update_screen()
            # Limit the game loop to a maximum of 60 frames per second
            self.clock.tick(60)

    
    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and keep adding aliens until there's no room left.
        # Spacing between aliens is one alien width and one alien height

        # Create a single alien to get its width and height (used to calculate how many fit)
        # A rect's size is a tuple of (width, height)
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size

        # Initial x- and y-values: one alien width in from the left and one alien height 
        # down from the top
        current_x, current_y = alien_width, alien_height

        # Keep adding aliens while there is enough vertical space on the screen
        while current_y < (self.settings.screen_height - 3 * alien_height):

            # Keep adding aliens while there is enough horizontal space on the screen
            while current_x < (self.settings.screen_width - 2 * alien_width):
                # Call method to create alien at give x position
                self._create_alien(current_x, current_y)

                # Move to the position for the next alien, leaving a gap equal to one alien width
                current_x += 2 * alien_width

            # Finished a row; reset x value and increment y value
            current_x = alien_width
            current_y += 2 * alien_height


    def _create_alien(self, x_position, y_position):
        """Create an alien and place it in the row."""
        # Create a new alien
        new_alien = Alien(self)

        # Set the alien's x position (float for precise movement later if needed)
        new_alien.x = x_position

        # Update the rect x position for drawing on the screen
        new_alien.rect.x = x_position

        # Update the rect y position for drawing on the screen
        new_alien.rect.y = y_position

        # Add the alien to the gorup
        self.aliens.add(new_alien)


    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        # Loop through all aliens in the fleet
        for alien in self.aliens.sprites():
            # If any alien is at the screen edge...
            if alien.check_edges():
                # Change the direction of the entire fleet
                self._change_fleet_direction()
                # Exit the loop — only one alien needs to trigger the change
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        # Move every alien in the fleet down by a certain amount
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed

        # Reverse the fleet's horizontal movement direction
        # If the fleet was moving right (1), it now moves left (-1), and vice versa
        self.settings.fleet_direction *= -1
    

    def _check_events(self):
        """Respond to keypresses and mouse event; event loop."""
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Exit the game if the window is closed
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    self._check_play_button(mouse_pos)


    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        # collidepoint() returns True if the given point (x, y) lies within the button’s rect.
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.game_active:
            # Reset the game statistics
            self.stats.reset_stats()
            self.game_active = True

            # Get rid of any remaining bullets and aliens
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and centre the ship
            self._create_fleet()
            self.ship.center_ship()

            # Hide the mouse cursor
            pygame.mouse.set_visible(False)


    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions
        self.bullets.update()

        # Get rid of bullets that have disappeared
        # Loop through copy as Python expects list will stay the same length as long
        # as the loop is running
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()


    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        # Check for any bullets that have hit aliens
        # If so, get rid of the bullet and the alien
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, False, True
        )

        # Check if fleet is destroyed and if so create new one
        if not self.aliens:
            # Destroy existing bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()


    def _update_aliens(self):
        """Check if the fleet is at an edge, then update positions."""
        self._check_fleet_edges()
        self.aliens.update()

        # Check if the ship has collided with any alien in the group
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            # If a collision is detected, print a message to the console
            self._ship_hit()

        # Look for aliens hitting the bottom of the screen
        self._check_aliens_bottom()

    def _ship_hit(self):
        """Respond to the ship being hit by an alien."""
        if self.stats.ship_left > 0:
            # Decrement ships_left.
            self.stats.ship_left -= 1

            # Get rid of any remaining bullets and aliens
            self.bullets.empty()
            self.aliens.empty()

            # Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            # Pause.
            sleep(0.5)
        else:
            self.game_active = False
            pygame.mouse.set_visible(True)
        
    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen."""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Treat this the same as if the ship got hit
                self._ship_hit()
                break

    def _update_screen(self):
        """Updates images on the screen, and flip to the new screen."""
        # Updates the background colour
        self.screen.fill(self.settings.bg_colour)

        # Draw bullets on the screen
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        
        # Draw the ship on the screen
        self.ship.blitme()

        # Draw the aliens
        self.aliens.draw(self.screen)

        # Draw the play button if the is inactive
        if not self.game_active:
            self.play_button.draw_button()

        # Update the screen with the latest drawings and changes
        pygame.display.flip()


    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        # Set movement flag to true
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        # Press q to quit the game
        elif event.key == pygame.K_q:
            sys.exit()
        # Fire bullet
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()


    def _check_keyup_events(self, event):
        # Set movement flag to false
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)


# Only run the game if this file is executed directly (not imported)
if __name__ == '__main__':
    # Create an instance of the game and start the main loop
    ai =  AlienInvasion()
    ai.run_game()