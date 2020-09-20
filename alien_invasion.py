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
        self.def_settings()
        self.def_screen()
        self.init_stats_of_game()
        self.create_buttons()
        self.create_scoreboard()
        self.create_surfaces()

    def def_settings(self):
        self.ai_settings = Settings()

    def def_screen(self):
        self.screen_dimensions = (self.ai_settings.screen_width, self.ai_settings.screen_height)
        self.screen = pygame.display.set_mode(self.screen_dimensions)

    def init_stats_of_game(self):
        self.stats = GameStats(self)

    def create_surfaces(self):
        self.ship = self.create_ship()
        self.aliens = self.create_aliens()
        self.super_aliens = self.create_super_aliens()
        self.bullets = self.create_bullets()
        self.create_fleet_of_aliens()

    def create_bullets(self):
        return Group()

    def create_aliens(self):
        return Group()

    def create_super_aliens(self):
        return Group()

    def create_ship(self):
        return Ship(self)

    def create_buttons(self):
        self.play_button = self.make_button('Play')
        self.pause_button = self.make_button('Pause')

    def create_scoreboard(self):
        self.sb = Scoreboard(self)
        
    def create_fleet_of_aliens(self):
        gf.create_fleet(self)

    def make_button(self, type_of_button):
        return Button(self, type_of_button)

    def assign_name_to_game(self, new_game_name):
        pygame.display.set_caption(new_game_name)

    def run(self):
        while True:
            self.check_for_key_and_mouse_events()

            if self.is_game_active():
                self.update_game()
                
    def check_for_key_and_mouse_events(self):
        gf.check_events(self)

    def is_game_active(self):
        return self.stats.game_active

    def update_game(self):
        self.update_surfaces()
        self.update_screen()

    def update_screen(self):
        gf.update_screen(self)

    def update_ship(self):
        self.ship.update()
    
    def update_aliens(self):
        gf.update_aliens(self)

    def update_bullets(self):
        gf.update_bullets(self)

    def update_surfaces(self):
        self.update_ship()
        self.update_aliens()
        self.update_bullets()

def run_game():
    pygame.init()
    game = Game()
    game.run()

# Enjoy :)
run_game()

    

    