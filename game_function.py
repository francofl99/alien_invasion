import sys
from time import sleep
import pygame

from pygame.sprite import Group

from alien import Alien, SuperAlien
from bullet import Bullet

# Events
def check_events(game):
    """
    Rspond to keypress and mouse events.
    """
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                check_keydown_events(event, game)

            elif event.type == pygame.KEYUP:
                check_keyup_events(event, game.ship)
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                mouse = (mouse_x, mouse_y)
                check_button(game, mouse)

def check_keydown_events(event, game):
    """
    Respond to keypresses
    """
    if event.key == pygame.K_RIGHT:
        game.ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        game.ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(game)
    elif event.key == pygame.K_p:
        pause_game(game)
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event, ship):
    """
    Response to key releases
    """
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_button(game, mouse):
    """Check if either play or pause button were clicked"""
    button_clicked = game.play_button.rect.collidepoint(mouse[0], mouse[1])
    if not game.stats.game_active and game.stats.game_pause:
        # If the game is on pause then reanude
        reanude_game(game)
    else:
        # If the game is inactive then reset
        reset_game(game)

# Aliens and Super Aliens
def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that fit in a row."""
    avaible_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(avaible_space_x / (2 * alien_width)) - 3
    return number_aliens_x

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien and place it in the row."""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    alien.rect.x = alien.x
    aliens.add(alien)

def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine the number of rows of aliens that fit on the screen."""
    available_space_y = (ai_settings.screen_height - (3 * alien_height ) - ship_height )
    number_rows = int(available_space_y / (2 * alien_height))
    
    return number_rows
    
def update_aliens(ai_settings, screen, stats, sb, ship, aliens, super_aliens,bullets):
    """
    Check if the fleet is at an edge,
    and then update the postions of all aliens in the fleet.
    """
    check_fleet_edges(ai_settings, aliens, super_aliens)
    aliens.update()
    super_aliens.update()
    # Look for alien-ship collisions or aliens hitting the bottom of the screen.
    check_aliens_ship_collisions(game)

def check_fleet_edges(ai_settings, aliens, super_aliens):
    """Respond appropriately if any aliens have reached an edge."""
    # join aliens on the game like a only information list 
    total_aliens = join_aliens(aliens, super_aliens)
    # Check of any alien match with screen edge
    for alien in total_aliens:
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens, super_aliens)
            break

def change_fleet_direction(ai_settings, aliens, super_aliens):
    """Drop the entire fleet and change the fleet's direction."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    for super_alien in super_aliens.sprites():
        super_alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def join_aliens(aliens, super_aliens):
    """Join the totally of game aliens"""
    total_aliens = Group()
    for alien in aliens:
        total_aliens.add(alien)
    for super_alien in super_aliens:
        total_aliens.add(super_alien)

    return total_aliens

def create_fleet(game):
    """Create a full fleet of aliens."""
    # Spacing between each alien is equal to one alien width.
    alien = Alien(game.ai_settings, game.screen)
    # Get the number of columns (width) for aliens
    number_aliens_x = get_number_aliens_x(game.ai_settings, alien.rect.width)
    # Get the number of rows (deep) for aliens
    number_rows = get_number_rows(game.ai_settings, game.ship.rect.height, alien.rect.height) - 2
    # Create the fleet of aliens
    create_alien_fleet(game.ai_settings, game.screen, game.aliens, number_rows, number_aliens_x)
    # Create the fleet of super aliens
    create_super_fleet(game.ai_settings, game.screen, game.super_aliens, number_rows, number_aliens_x)

def create_super_fleet(ai_settings, screen, super_aliens, number_rows, number_aliens_x):
    """Creat a fleet of super aliens"""
    row_number = number_rows 
    for alien_number in range(number_aliens_x):
        create_super_alien(ai_settings, screen, super_aliens, alien_number, row_number)

def create_super_alien(ai_settings, screen, super_aliens, alien_number, row_number):
    """Create a super alien"""
    alien = SuperAlien(ai_settings, screen)
    alien.x = alien.rect.width + 2 * alien.rect.width * alien_number
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    alien.rect.x = alien.x
    super_aliens.add(alien)

def create_alien_fleet(ai_settings, screen, aliens, number_rows, number_aliens_x):
    """Create a fleet of aliens"""
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            # Create an alien and place it in the row.
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

# Collisions
def check_aliens_ship_collisions(game):
    """Check for collisions between aliens and ship or if some alien reach the bottom sceen
    """
    ship_alien_collision = pygame.sprite.spritecollideany(game.ship, game.aliens)
    alien_on_the_bottom = alien_on_bottom(game)
    if ship_alien_collision or alien_on_the_bottom:
        ship_hit(game)

def check_bullet_alien_collisions(ai_settings,screen, stats, sb, ship, aliens, super_aliens, bullets):
    """Respond to bullet-alien collisions."""

    # Check if any bullet collision with any alien
    bullet_alien_collision(ai_settings,screen, stats, sb, ship, aliens, bullets)

    # Check if any bullet collision with any super alien
    bullet_super_alien_collisions(ai_settings,screen, stats, sb, ship, super_aliens, bullets)
        
    # Check if totally fleet are down
    check_fleet_down(game)

def bullet_alien_collision(ai_settings,screen, stats, sb, ship, aliens, 
bullets):
    # Remove any bullets and aliens that have collided.
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            # Assign points
            assign_points(ai_settings, stats, sb, aliens=aliens)
        
        # Update high score
        check_high_score(stats, sb)

def check_fleet_down(game):
    """Check if the total aliens are down"""
    # If not exist any alien or super alien
    if not len(game.aliens) and not len(game.super_aliens):
        # Reorder surfaces without reorder ship
        reorder_surfaces(game)
        # Increment challenger of game
        increase_level(game.ai_settings, game.stats, game.sb)

def bullet_super_alien_collisions(ai_settings,screen, stats, sb, ship, super_aliens, bullets):
    """Check if any bullet shoot to any super alien"""
    collisions = pygame.sprite.groupcollide(bullets, super_aliens, True, False)

    if collisions:
        for super_aliens_list in collisions.values():
            for super_alien in super_aliens_list:
                # If the super alien have two shoot
                if super_alien.scratch:
                    # Delete super alien
                    super_aliens.remove(super_alien)
                    # Assign points
                    assign_points(ai_settings, stats, sb, super_aliens=super_aliens_list)
                    # Update high score
                    check_high_score(stats, sb)
                else:
                    # The super alien have one shoot
                    super_alien.scratch = 1

def ship_hit(game):
    """Respond to ship being hit by alien."""
    if game.stats.ships_left > 0:
        # Decrement ships_left.
        game.stats.ships_left -= 1
        # Reorder surfaces
        reorder_surfaces(game, True)
        # Update scoreboard.
        game.sb.prep_ships()
        # Pause
        sleep(0.75)
    else:
        # Game Over
        game.stats.game_active = False

# Bullets
def update_bullets(ai_settings, screen, stats, sb, ship, aliens, super_aliens, bullets):
    """Update position of bullets and get rid of old bullets."""
    # Update bullet positions
    bullets.update()
    # Get rid of bullets that have disappeared.
    remove_old_bullets(bullets)
    # Check for any bullets that have hit aliens and if so, get rid of the bullet and the alien
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, super_aliens, bullets)

def remove_old_bullets(bullets):
    """Remove bullets such it was reached the top screen"""
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

def fire_bullet(game):
    """Fire a bullet if limit not reached yet."""
    # Create a new bullet and add it to the bullets group.
    if len(game.bullets) < game.ai_settings.bullets_allowed:
            new_bullet = Bullet(game)
            game.bullets.add(new_bullet)

# Points
def assign_points(ai_settings, stats, sb, aliens=None, super_aliens=None):
    if aliens:
        # Assign the totally points of aliens shotdown
        stats.score += ai_settings.alien_points * len(aliens)
    if super_aliens:
        # Assign the points of super alien down
        stats.score += ai_settings.super_alien_points
    # Update score
    sb.prep_score()

def increase_level(ai_settings, stats, sb):
    """Increment challenger of game"""
    # Increment speed
    ai_settings.increase_speed()
    # Increase level.
    stats.level += 1
    # Update level
    sb.prep_level()

def check_high_score(stats, sb):
    """Check to see if there's a new high score."""
    if stats.score > stats.high_score:
        stats.update_high_score()
        sb.prep_high_score()

# Game update and screen
def show_surfaces(screen, ship, aliens, super_aliens, bullets):
    """Draw the elements on the game"""
    # Show bullets
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    # Show ship
    ship.blitme()
    # Show aliens
    aliens.draw(screen)
    super_aliens.draw(screen)

def update_screen(game):
    """Update images on the screen and flip to the new screen."""
    #Redraw the screen during each pass through the loop.
    game.screen.fill(game.ai_settings.bg_color)
    # show elements of the game on screen
    show_surfaces(game.screen, game.ship, game.aliens, game.super_aliens, game.bullets)
    # Draw the score information
    game.sb.show_score()
    # Draw the play button if the game is inactive.
    check_state_game(game.stats, game.play_button, game.pause_button)
    #make the most recently draw screen visible
    pygame.display.flip()

def check_state_game(stats, play_button, pause_button):
    """Check the state of the game, if it's either pause or inactive"""
    if stats.game_pause:
        pause_button.draw_button()
        pygame.mouse.set_visible(True)
    elif not stats.game_active:
        play_button.draw_button()
        pygame.mouse.set_visible(True)

def reorder_surfaces(game, center_ship=False):
    """Set the surfaces at the correct position when the game is reset"""
    # Empty the list of bullets
    game.bullets.empty()
    # Empty the lost of aliens
    game.aliens.empty()
    game.super_aliens.empty()
    # Create a new fleet
    create_fleet(game)
    # center ship
    if center_ship:
        game.ship.center_ship()
    
def alien_on_bottom(game):
    """Check if any aliens have reached the bottom of the screen."""
    screen_rect = game.screen.get_rect()
    for alien in game.aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            return True

    return False

def reset_game(game):
    """Reset totally game"""
    # Hide the mouse cursor.
    pygame.mouse.set_visible(False)
    # Reset the game settings.
    game.ai_settings.initialize_dynamic_settings()
    # Reset the game statistics
    game.stats.reset_stats()
    # Reset the scoreboard images.
    game.sb.reset_sb()
    # Reorder elements of the game
    reorder_surfaces(game, True)
    # Activate game
    game.stats.game_active = True
        
def pause_game(game):
    game.stats.game_pause = True
    game.stats.game_active = False
    
def reanude_game(game):
    game.stats.game_active = True
    game.stats.game_pause = False


