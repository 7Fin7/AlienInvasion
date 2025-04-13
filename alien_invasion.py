
import sys  # Use tools in sys to exit the game when the player quits
import pygame  # Contains functionality to make a game

from settings import Settings
from ship import Ship

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


    def run_game(self):
        """Start the main loop for the game."""
        
        # Event: action that the user performs while playing the game, key, mouse press

        while True:

            # Call methods for event loop, right movement and updating screen
            self._check_events()
            self.ship.update()
            self._update_screen()

            # Limit the game loop to a maximum of 60 frames per second
            self.clock.tick(60)

    
    def _check_events(self):
        """Respond to keypresses and mouse event; event loop."""
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Exit the game if the window is closed
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        # Set right movement flag to true
                        self.ship.moving_right = True
                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        # Set right movement flag to false
                        self.ship.moving_right = False

    def _update_screen(self):
        """Updates images on the screen, and flip to the new screen."""
        
        # Updates the background colour
        self.screen.fill(self.settings.bg_colour)

        # Draw the ship on the screen
        self.ship.blitme()

        # Update the screen with the latest drawings and changes
        pygame.display.flip()


# Only run the game if this file is executed directly (not imported)
if __name__ == '__main__':
    # Create an instance of the game and start the main loop
    ai =  AlienInvasion()
    ai.run_game()