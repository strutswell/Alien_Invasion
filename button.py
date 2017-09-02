import pygame.ftfont


class Button():
    def __init__(self, ai_settings, screen, msg):
        """ Init the button """
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # set dimensions and properties
        self.width, self.height = 200, 50
        self.button_colour = (0, 255, 0)
        self.text_colour = (255, 255, 200)
        self.font = pygame.font.SysFont(None, 48)

        # build the rect and center it
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center

        # the button message
        self.prep_msg(msg)


    def prep_msg(self, msg):
        """ turn msg into rendered image and center text on button """
        self.msg_image = self.font.render(msg, True, self.text_colour, self.button_colour)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center


    def draw_button(self):
        # draw button and message
        self.screen.fill(self.button_colour, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

