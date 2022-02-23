import pygame as pg
from Menu import Menu
from Database import Database


class OptionMenu(Menu):
    def __init__(self, window):
        """
        constructor for OptionMenu
        :param window: a Window() object
        """
        # initialize the superclass
        Menu.__init__(self, window)

        # make variable for database calls
        self.db = Database()

        # Get settings from database as a dictionary
        self.settings_dic = self.db.get_settings()

        # Load in background image
        self.bgImg = pg.image.load('Assets/Bubbles.jpg').convert_alpha()

        # initial state set on volume
        # might not need we will see later
        self.state = "Volume"

        # where each "text option" is displayed
        self.vol_x, self.vol_y = self.half_w, self.half_h + 20
        self.res_x, self.res_y = self.half_w, self.half_h + 60
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)

        # Make graphics string
        graphics = str(self.settings_dic["res_height"]) + "p"

        # create buttons and sliders and dropBoxes
        self.backButton = self.MWO.create_button(self.thirtytwo_w, self.thirtytwo_h, self.quarter_w / 3,
                                            self.quarter_h / 3, (200, 200, 200), self.black, text='Back')

        self.soundSlider = self.MWO.create_slider(self.quarter_w, self.quarter_h / 2, self.half_w, self.quarter_h / 2,
                                                  self.settings_dic["sound"])

        self.musicSlider = self.MWO.create_slider(self.quarter_w, self.quarter_h + self.sixteenth_h, self.half_w,
                                                  self.quarter_h / 2, self.settings_dic["music"])

        self.graphicsDropBox = self.MWO.create_dropbox(self.quarter_w - self.sixteenth_w,
                                                       self.half_h + self.sixteenth_h, self.quarter_w,
                                                       self.quarter_h / 3, ['480p', '720p', '792p'],
                                                       initialText=graphics)

        self.difficultyDropBox = self.MWO.create_dropbox(self.half_w + self.sixteenth_w, self.half_h + self.sixteenth_h,
                                                         self.quarter_w, self.quarter_h / 3, ['Easy', 'Normal', 'Hard'],
                                                         initialText=self.settings_dic["difficulty"])

    def display_screen(self):
        """
        the display loop that draws all required objects on screen.
        This happens every frame.
        :return: None
        """
        # making sure OptionMenu's is_display is true
        self.is_displaying = True

        while self.is_displaying:

            # check for user input
            self.MWO.set_user_input()
            self.check_input()

            # draw objects on the screen (**in provided order**)
            self.MWO.draw_image('Assets/Bubbles.jpg', 0, 0, self.MWO.DISPLAY_W, self.MWO.DISPLAY_H)
            # self.MWO.display.fill((0,100,100))
            self.MWO.draw_text("Options Menu", 40, self.half_w, self.MWO.DISPLAY_H / 20, self.white)
            self.MWO.draw_text("Changes will be updated when returned to the main menu", 20, self.half_w,
                               self.MWO.DISPLAY_H * 0.90, self.white)

            # draw button
            self.backButton.draw()

            # draw sliders
            self.soundSlider.draw()
            self.MWO.draw_text("Sounds", 30, self.quarter_w - self.sixteenth_w, self.quarter_h * 3 / 4, self.white)
            self.MWO.draw_text(str(self.soundSlider.getPercentage()), 30, self.half_w + self.quarter_w + self.sixteenth_w,
                               self.quarter_h * 3 / 4, self.white)

            self.musicSlider.draw()
            self.MWO.draw_text("Music", 30, self.quarter_w - self.sixteenth_w,
                               self.quarter_h + self.sixteenth_h + (self.quarter_h / 4), self.white)
            self.MWO.draw_text(str(self.musicSlider.getPercentage()), 30, self.half_w + self.quarter_w + self.sixteenth_w,
                               self.quarter_h + self.sixteenth_h + (self.quarter_h / 4), self.white)

            # draw dropBoxes
            self.graphicsDropBox.draw()
            self.MWO.draw_text("Graphics", 30, self.quarter_w + self.sixteenth_w, self.half_h, self.white)

            self.difficultyDropBox.draw()
            self.MWO.draw_text("Difficulty", 30, self.half_w + self.quarter_h + self.sixteenth_h, self.half_h, self.white)

            # "update" the screen
            self.blit_menu()

    def check_input(self):
        """
        OptionMenu's state machine; checks input and acts accordingly
        :return: None
        """
        # check for Backspace or back button click to go back to MainMenu
        if self.MWO.BACKSPACE_KEY or self.backButton.clickCheck():
            self.update_database_settings(self.graphicsDropBox.getValue(), self.difficultyDropBox.getValue(),
                                          self.soundSlider.getPercentage(), self.musicSlider.getPercentage())
            self.update_MWO_settings()
            self.MWO.current_screen = self.MWO.main_menu
            self.is_displaying = False


    def update_database_settings(self, resolution=None, difficulty=None, sound=None, music=None):
        height = None
        width = None
        if resolution == "480p":
            height = 480
            width = 858
        elif resolution == "720p":
            height = 720
            width = 1280
        elif resolution == "792p":
            height = 792
            width = 1408
        self.db.update_settings(height, width, str(difficulty), sound, music)


    def update_MWO_settings(self):
        dic = self.db.get_settings()
        if dic["music"] != self.MWO.music_vol:
            self.MWO.music_vol = dic["music"] / 100
            self.MWO.change_music_vol()

        if dic["sound"] != self.MWO.SFX_vol:
            self.MWO.SFX_vol = dic["sound"] / 100

        if dic["res_height"] != self.MWO.DISPLAY_H:
            self.MWO.DISPLAY_H = dic["res_height"]
            self.MWO.DISPLAY_W = dic["res_width"]
            self.update_screen_cords()
            self.MWO.update_menu_resolution()

        if dic["difficulty"] != self.MWO.difficulty:
            self.MWO.difficulty = dic["difficulty"]
