
class GameStats:
    """Track statistics for Alien Invasion."""

    def __init__(self, ai_game):
        """Initialise statistics."""
        self.settings = ai_game.settings
        self.reset_stats()

    # We’ll call this method from __init__() so the statistics are set properly when 
    # he GameStats instance is first created 1. But we’ll also be able to call 
    # reset_stats() anytime the player starts a new game.
    def reset_stats(self):
        """Initialise statistics that can change during the game."""
        self.ships_left = self.settings.ship_limit