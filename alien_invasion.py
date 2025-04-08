
import sys  # Use tools in sys to exit the game when the player quits
import pygame  # Contains functionality to make a game

class AlienInvasion:
    """Overall class to manage game assets and behaviour."""
    
    def __init__(self):
        """Initialise the game, and create game resources."""

        # Initialise the imported pygame modules
        pygame.init()

        # Set the dimensions of the game window and create the display surface
        # Surface: part of the screen where a game element can be displayed
        self.screen = pygame.display.set_mode((1000, 600))

        # Set the title of the game window
        pygame.display.set_caption("Alien Invasion")

    def run_game(self):
        """Start the main loop for the game."""
        
        # Event: action that the user performs while playing the game, key, mouse press

        while True:
            # Handle events like key presses and mouse clicks - event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Exit the game if the window is closed
                    sys.exit()

            # Update the screen with the latest drawings and changes
            pygame.display.flip()


# Only run the game if this file is executed directly (not imported)
if __name__ == '__main__':
    # Create an instance of the game and start the main loop
    ai =  AlienInvasion()
    ai.run_game()