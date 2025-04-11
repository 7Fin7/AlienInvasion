
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

        # Load the ship image and get its rect
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # Start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom

    def blitme(self):
        """Draw the ship at its current location."""
        self.screen.blit(self.image, self.rect)