import sys
import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    """Response to keypresses and mouse events"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            # this is the window's close button
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)
        if event.type == pygame.KEYUP:
            check_keyup(event, ship)
        if event.type == pygame.KEYDOWN:
            check_keydown(event, ai_settings, screen, ship, bullets)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    """ start a new game """
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        ai_settings.initialize_dynamic_settings()
        stats.reset_stats()
        stats.game_active = True
        pygame.mouse.set_visible(False)

        # empty the list of aliens and bullets
        aliens.empty()
        bullets.empty()

        # reset scoreboard
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # create a new fleet and center the ship
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

def check_keydown(event, ai_settings, screen, ship, bullets):
    # this is a key press
    if event.key == pygame.K_RIGHT:
        # move the ship right
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        # move the ship left
        ship.moving_left = True
    elif event.key == pygame.K_UP:
        # move up
        ship.moving_up = True
    elif event.key == pygame.K_DOWN:
        # move down
        ship.moving_down = True

    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()


def fire_bullet(ai_settings, screen, ship, bullets):
    """Fire a bullet if limit is not reached"""
    # create new bullet and add to group if we havent reached max yet
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)



def check_keyup(event, ship):
    # this is a key release
    if event.key == pygame.K_RIGHT:
        # stop moving right
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        # stop moving left
        ship.moving_left = False
    elif event.key == pygame.K_UP:
        # stop moving up
        ship.moving_up = False
    elif event.key == pygame.K_DOWN:
        # stop moving down
        ship.moving_down = False


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
        """Update images on the screen and flip to the new screen"""
        # redraw screen during each pass through the loop
        screen.fill(ai_settings.bg_colour)

        # redraw all bullets behind the ship and aliens
        for bullet in bullets.sprites():
            bullet.draw_bullet()
        ship.blitme()
        aliens.draw(screen)

        # draw score info
        sb.show_score()

        # draw play button if game is inactive
        if not stats.game_active:
            play_button.draw_button()

        # Make the most recently drawn screen visible
        pygame.display.flip()

def update_bullets(bullets):
    """Updates position of all bullets on screen, get rid of old bullets"""
    # update bullet position
    bullets.update()

    # get rid of old bullets that are off-screen
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)


def check_collisions_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Check for any bullets that have collided with aliens"""
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    # 3rd argument is True to clear the bullet after 1 collision, can set to False for super-bullet!
    # 4th argument is True to clear the alien off the screen

    if len(aliens) == 0:
        # destroy existing bullets and create new fleet of aliens
        bullets.empty()
        ai_settings.increase_speed()
        stats.level += 1
        sb.prep_level()
        create_fleet(ai_settings, screen, ship, aliens)
        sleep(1)


def check_collisions_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets):
    """Check for any aliens that have collided with the ship"""
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)



def get_number_aliens_x(ai_settings, alien_width):
    """Determine number of aliens that fit the space"""
    available_space_x = ai_settings.screen_width - (2 * alien_width)
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    """Create an alien"""
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    """ Create full fleet of aliens. """
    # create an alien and find the number of aliens in a row
    # space between each alien is 1 width of an alien rect
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    # create the fleet of aliens
    for row_number in range(number_rows):
        # create first row of aliens
        for alien_number in range(number_aliens_x):
            # create an alien and place it in the row
            create_alien(ai_settings, screen, aliens, alien_number, row_number)


def get_number_rows(ai_settings, ship_height, alien_height):
    """Determine number of rows that fit"""
    available_space_y = ai_settings.screen_height - (3 * alien_height) - ship_height
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def update_aliens(ai_settings, aliens):
    """check if fleet is at edge, then update position of all aliens"""
    check_fleet_edges(ai_settings, aliens)
    aliens.update()


def check_fleet_edges(ai_settings, aliens):
    """Respond appropriately if any aliens have reached the edge"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """Drop the entire fleet and change direction"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Respond to ship being hit by alien"""
    if stats.ships_left >= 1:
        stats.ships_left -= 1
        sb.prep_ships()
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        sleep(1)
    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)


def check_location_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # same if ship got hit
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break

def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
