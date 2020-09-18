class GameStats():
    """Track statistics for Alien Invasion."""

    def __init__(self, game):
        """Initialize statistics."""
        self.ai_settings = game.ai_settings
        self.reset_stats()
        # Start Alien Invasion in an active state.
        self.game_active = False
        self.game_pause = False

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.ships_left = self.ai_settings.ship_limit
        self.high_score = self.read_high_score()
        self.score = 0
        self.level = 1

    def read_high_score(self):
        buffer = ' '
        with open('data/high_score.txt') as file_object:
            for line in file_object.readlines():
                buffer += line.rstrip()
        return int(buffer)
        
    def update_high_score(self):
        self.score_str = str(self.score)
        with open('data/high_score.txt', 'w') as file_object:
            file_object.write(self.score_str)

        