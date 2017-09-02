
# TODO: save high score to file before running sys.exit
# TODO: add shields, bullets from aliens, shields get destroyed from both sides
# TODO: add music and sound effects with pygame.mixer

import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
from game_stats import GameStats
from button import Button
from scoreboard import ScoreBoard

import game_functions as gf

def run_game():
    # Init pygame, settings and create screen object
    pygame.init();

    # loading self referenced settings variables from imported class
    ai_settings = Settings()

    # the screen object is called a surface which displays a game element
    # this surface will be redrawn every pass through the loop for animation
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion!")

    # make the play button
    play_button = Button(ai_settings, screen, "Play")

    # create instance to store game stats
    stats = GameStats(ai_settings)
    sb = ScoreBoard(ai_settings, screen, stats)

    # Make ship, reference the screen we created for coordinate matching
    ship = Ship(ai_settings, screen)

    # make a group to store bullets
    bullets = Group()

    # make a group to store aliens
    aliens = Group()

    # create fleet of aliens
    gf.create_fleet(ai_settings, screen, ship, aliens)


    # Start the main loop for the game.
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(bullets)
            gf.check_collisions_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets)
            gf.update_aliens(ai_settings, aliens)
            gf.check_collisions_aliens(ai_settings, stats, screen, sb, ship, aliens, bullets)
            gf.check_location_aliens(ai_settings, stats, sb, screen, ship, aliens, bullets)

        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button)

# kick off the run_game() function
run_game()