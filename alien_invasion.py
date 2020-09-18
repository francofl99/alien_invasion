import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
import game_function as gf

class Game:
    def __init__(self):
        self.assign_name_to_game("Alien invasion")

        self.ai_settings = Settings()
        self.screen_dimensions = (self.ai_settings.screen_width, self.ai_settings.screen_height)
        self.screen = pygame.display.set_mode(self.screen_dimensions)
        self.stats = GameStats(self)

        self.play_button = self.make_button('Play')
        self.pause_button = self.make_button('Pause')

        self.sb = Scoreboard(self)

        # Elements of the game
        self.ship = Ship(self.ai_settings, self.screen)
        self.aliens = Group()
        self.super_aliens = Group()
        self.bullets = Group()

        gf.create_fleet(self)

    def make_button(self, type_of_button):
        return Button(self.ai_settings, self.screen, type_of_button)

    def assign_name_to_game(self, new_game_name):
        pygame.display.set_caption(new_game_name)

    def run(self):
        while True:
            # Check for keyboard and mouse events
            gf.check_events(self)
            # If the game is active
            if self.stats.game_active:
            # Update on the screen the game elements
                self.update_surfaces()
                #update game
                gf.update_screen(self)

    def update_surfaces(self):
        """Update game elements"""
        # Update ship
        self.ship.update()
        # Update bullets
        gf.update_bullets(self.ai_settings, self.screen, self.stats, self.sb, self.ship, self.aliens, self.super_aliens, self.bullets)
        # Update aliens and super aliens
        gf.update_aliens(self.ai_settings, self.screen, self.stats, self.sb, self.ship, self.aliens, self.super_aliens, self.bullets)


    

def run_game():
    pygame.init()
    game = Game()
    game.run()

# Enjoy :)
run_game()

    

    