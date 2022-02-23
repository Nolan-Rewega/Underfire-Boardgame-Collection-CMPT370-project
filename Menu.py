import pygame as pg

class Menu:
    def __init__(self, window):
        """
        Menu superclass; constructor
        :param window: A Window() Object
        """
        # set the Widow object ("MWO = Main Window Object")
        self.MWO = window

        # (dynamic) screen cords

        self.full_w, self.full_h = self.MWO.DISPLAY_W, self.MWO.DISPLAY_H
        self.half_w, self.half_h = self.MWO.DISPLAY_W / 2, self.MWO.DISPLAY_H / 2
        self.quarter_w, self.quarter_h = self.MWO.DISPLAY_W / 4, self.MWO.DISPLAY_H / 4
        self.sixteenth_w, self.sixteenth_h = self.MWO.DISPLAY_W / 16, self.MWO.DISPLAY_H / 16
        self.thirtytwo_w, self.thirtytwo_h = self.MWO.DISPLAY_W / 32, self.MWO.DISPLAY_H / 32
        self.is_displaying = True

    def save_to_db(self):
       """
       TEMP CLASS
       :return:
       """
       pass

    def load_from_db(self):
        """
        TEMP CLASS
        :return:
        """
        pass

    def blit_menu(self):
        """
        displays the drawn objects and then resets flags.
        :return: None
        """
        # (0, 0) is the top left of the screen
        self.MWO.window.blit(self.MWO.display, (0, 0))
        pg.display.update()
        self.MWO.reset_key_inputs()


    def update_screen_cords(self):
        self.full_w, self.full_h = self.MWO.DISPLAY_W, self.MWO.DISPLAY_H
        self.half_w, self.half_h = self.MWO.DISPLAY_W / 2, self.MWO.DISPLAY_H / 2
        self.quarter_w, self.quarter_h = self.MWO.DISPLAY_W / 4, self.MWO.DISPLAY_H / 4
        self.sixteenth_w, self.sixteenth_h = self.MWO.DISPLAY_W / 16, self.MWO.DISPLAY_H / 16
        self.thirtytwo_w, self.thirtytwo_h = self.MWO.DISPLAY_W / 32, self.MWO.DISPLAY_H / 32







