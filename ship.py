
import pygame

class Ship:
    """A class to manage the ship."""

    # Takes in a reference to the current instance of the AlienInvasion class.
    # This will give the ship access to the game resources.
    def __init__(self, ai_game):
        """Initalise the ship and set its starting position."""

        # Access the screen's rect attribute using the get_rect() method.
        # Doing so allows you to place the ship in the correct location.
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        # Access game settings
        self.settings = ai_game.settings

        # Load the ship image and get its rect
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

        # Store a float for the ship's exact horizontal position
        self.x = float(self.rect.x)

        # Movement flag; start with a ship that's not moving
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Update the ship's position based on the movement flag."""
        # Update the ship's x value and check for boundaries.
        # self.rect.right returns the x-coordinate of the right edge of the ship’s rect
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed

        # Update the rect object from self.x
        self.rect.x = self.x

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)