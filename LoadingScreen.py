import time as t
import pygame as pg

class LoadingScreen:
    # set the Widow object ("MWO = Main Window Object")
    def __init__(self, window):
        self.MWO = window
        self.is_displaying = False

        # time objects
        self.time = 0
        self.timelim = 3

        self.half_w, self.half_h = self.MWO.DISPLAY_W / 2, self.MWO.DISPLAY_H / 2
        self.bar_offset_y = + 25

        # sizes
        self.box_size_w, self.box_size_h = self.half_w, self.half_h
        self.bar_size_w, self.bar_size_h = self.half_w, self.half_h/10

        # positions
        self.box_x, self.box_y = self.half_w/2, self.half_h/2
        self.bar_x, self.bar_y = self.half_w/2, self.half_h + self.bar_offset_y

    def display_screen(self):
        start = t.time()
        self.is_displaying = True
        # start music on loading time
        self.MWO.play_music()
        while self.is_displaying:
            # update elasped time and progress
            self.time = t.time() - start + 0.1
            progress = self.time/self.timelim

            self.MWO.set_user_input()
            self.check_input()

            self.MWO.draw_rect((0,0,0), self.box_x, self.box_y, self.box_size_w, self.box_size_h)
            self.MWO.draw_text("Loading....", 20, self.half_w, self.half_h)
            self.MWO.draw_rect((255,255,255), self.bar_x, self.bar_y, self.bar_size_w, self.bar_size_h)
            self.MWO.draw_rect((100, 255, 100), self.bar_x, self.bar_y, self.bar_size_w * progress, self.bar_size_h)

            self.blit_LoadingScreen()

    def check_input(self):
        """
        Profile's state machine; checks input and acts accordingly
        :return: None
        """
        # check for enter key
        if self.MWO.BACKSPACE_KEY or self.time > self.timelim :
            self.MWO.current_screen = self.MWO.main_menu
            self.is_displaying = False

    def blit_LoadingScreen(self):
        """
        displays the drawn objects and then resets flags.
        :return: None
        """
        self.MWO.window.blit(self.MWO.display, (0, 0))
        pg.display.update()
        self.MWO.reset_key_inputs()

