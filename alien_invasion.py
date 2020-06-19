import pygame
from pygame.sprite import Group

from settings import Settings
from ship import Ship
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard
import game_function as gf

def run_game():
    # Gettin settings
    ai_settings = Settings()
    #inizialite game and create a screen object
    pygame.init()
    # Create screen
    screen_dimensions = (ai_settings.screen_width, ai_settings.screen_height)
    screen = pygame.display.set_mode(screen_dimensions)
    # Game name
    pygame.display.set_caption("Alien invasion")
    # Make the Play button.
    play_button = Button(ai_settings, screen, 'Play')
    # Make the pause button
    pause_button = Button(ai_settings, screen, 'Pause')
    # Create an instance to store game statistics
    stats = GameStats(ai_settings)
    # Create scoreboard
    sb = Scoreboard(ai_settings, screen, stats)
    # Make a ship, a group of bullets, group of aliens and super aliens
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    super_aliens = Group()
    # Create the fleet of aliens.
    gf.create_fleet(ai_settings, screen, ship, aliens, super_aliens)
    # Run game
    while True:
        run(ai_settings, screen, stats, sb, ship, aliens, super_aliens, bullets, play_button, pause_button)

def update_surfaces(ai_settings, screen, stats, sb, ship, aliens, super_aliens, bullets):
        """Update game elements"""
        # Update ship
        ship.update()
        # Update bullets
        gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens, super_aliens, bullets)
        # Update aliens and super aliens
        gf.update_aliens(ai_settings, screen, stats, sb, ship, aliens, super_aliens, bullets)

def run(ai_settings, screen, stats, sb, ship, aliens, super_aliens, bullets, play_button, pause_button):
    """Run game and update surfaces"""
    # Check for keyboard and mouse events
    gf.check_events(ai_settings, screen, stats, sb, play_button, pause_button, ship, aliens, super_aliens, bullets)
    # If the game is active
    if stats.game_active:
        # Update on the screen the game elements
        update_surfaces(ai_settings, screen, stats, sb, ship, aliens, super_aliens, bullets)
    # update game
    gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, super_aliens,bullets, play_button, pause_button)

# Enjoy :)
run_game()

    

    