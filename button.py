import pygame.font  # Lets Pygame render text to the screen

class Button:
    """A class to build buttons for the game."""

    def __init__(self, ai_game, msg):
        """Initialise button attributes."""

        # Get access to the game screen and its rectangle
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()

        # Button appearance and size settings
        self.width, self.height = 200, 50
        self.button_colour = (0, 135, 0)
        self.text_colour = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)

        # Create a rectangular area for the button and position it at the screen centre
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # Render the button text once (no need to do it every frame)
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """
        Render the text message as an image and center it on the button.

        - Converts the text (msg) into a graphical image that can be drawn to the screen.
        - Centers the text image inside the button rectangle.
        """
        # Create a rendered image of the text with anti-aliasing (True)
        # The background of the text matches the button colour
        self.msg_image = self.font.render(msg, True, self.text_colour, self.button_colour)

        # Get the rectangle of the rendered text image
        self.msg_image_rect = self.msg_image.get_rect()

        # Center the text image within the button
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """Draw blank button and then draw message."""
        # Draw the rectangular area (the button background) on the screen.
        # screen.fill() fills a specific area of the screen (defined by self.rect)
        # with a solid colour. It’s used for drawing basic shapes like rectangles.
        self.screen.fill(self.button_colour, self.rect)

        # Draw the text image (the rendered message) on top of the button.
        # screen.blit() places an image or surface onto another surface at a given position.
        # Here it’s used to "blit" (copy) the pre-rendered text image onto the button area.
        self.screen.blit(self.msg_image, self.msg_image_rect)
