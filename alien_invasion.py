
import sys  # Use tools in sys to exit the game when the player quits
import pygame  # Contains functionality to make a game

from settings import Settings
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


    def run_game(self):
        """Start the main loop for the game."""
        
        # Event: action that the user performs while playing the game, key, mouse press

        while True:
            # Call methods game
            self._check_events()
            self.ship.update()
            self._update_bullets()
            self._update_screen()

            # Limit the game loop to a maximum of 60 frames per second
            self.clock.tick(60)

    
    def _create_fleet(self):
        """Create the fleet of aliens."""
        # Create an alien and keep adding aliens until there's no room left.
        # Spacing between aliens is on alien width.

        # Create a single alien to get its width (used to calculate how many fit)
        alien = Alien(self)
        alien_width = alien.rect.width

        # Start the first alien at a distance of one alien width from the left
        current_x = alien_width

        # Keep adding aliens while there is enough horizontal space on the screen
        while current_x < (self.settings.screen_width - 2 * alien_width):
            # Create a new alien
            new_alien = Alien(self)

            # Set the alien's x position (float for precise movement later if needed)
            new_alien.x = current_x

            # Update the rect x position for drawing on the screen
            new_alien.rect.x = current_x

            # Add the alien to the gorup
            self.aliens.add(new_alien)

            # Move to the position for the next alien, leaving a gap equal to one alien width
            current_x += 2 * alien_width
    
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

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions
        self.bullets.update()

        # Get rid of bullets that have disappeared.
        # Loop through copy as Python expects list will stay the same length as long
        # as the loop is running.
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

    
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