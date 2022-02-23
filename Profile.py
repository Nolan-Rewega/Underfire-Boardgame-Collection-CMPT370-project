import pygame as pg
from Menu import Menu
from Database import Database

class Profile(Menu):
    def __init__(self, window):
        """
        Profile's construction
        :param window: A Window() object
        """

        # initialize the superclass
        Menu.__init__(self, window)

        # Make database variable
        self.db = Database()

        # set the Widow object ("MWO = Main Window Object")
        self.MWO = window

        # text colours
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.grey = (200, 200, 200)

        # Make new length amounts
        self.three_quarter_w = self.quarter_w * 3
        self.three_quarter_h = self.quarter_h * 3
        self.eighth_w = self.quarter_w // 2
        self.eighth_h = self.quarter_h // 2

        # create buttons
        self.backButton = self.MWO.create_button(self.thirtytwo_w, self.thirtytwo_h, self.quarter_w / 3,
                                                 self.quarter_h / 3, self.grey, self.black, text='Back')
        self.leaderButton = self.MWO.create_button(self.MWO.DISPLAY_W - self.quarter_w / 2 - self.thirtytwo_w, self.thirtytwo_h, self.quarter_w / 2,
                                                  self.quarter_h / 3, self.grey, self.black, text='Leaderboards')

        # screen cords and sizes
        self.mid_w, self.mid_h = self.MWO.DISPLAY_W / 2, self.MWO.DISPLAY_H / 2
        self.forth_w, self.forth_h = self.MWO.DISPLAY_W / 4, self.MWO.DISPLAY_H / 4
        self.achieveWidth = int(self.sixteenth_w)
        self.halfAchieveWidth = (self.achieveWidth // 2)
        self.achieveHeight = self.MWO.DISPLAY_H // 1.5
        self.textAchieveSize = int(self.achieveWidth // 1.1)
        self.statsTextSize = int(20 * (self.MWO.DISPLAY_W/1280))
        self.is_displaying = False

    def display_screen(self):
        """
        draws all required objects on screen. This happens every frame.
        :return: None
        """

        # Get game stats dictionary
        stats = self.db.get_stats()

        # making sure OptionMenu's is_display is true
        self.is_displaying = True

        while self.is_displaying:

            # check for user input
            self.MWO.set_user_input()
            self.check_input()

            # draw background
            self.MWO.draw_image('Assets/Bubbles.jpg', 0, 0, self.MWO.DISPLAY_W, self.MWO.DISPLAY_H)


            # draw buttons
            self.backButton.draw()
            self.leaderButton.draw()

            # Draw Stats
            self.MWO.draw_text("Stats", 45, self.MWO.DISPLAY_W * 0.5, self.MWO.DISPLAY_H / 10, color=self.white)

            # Stats on left side
            self.MWO.draw_text("Total Games Played: " + str(stats["games_played"]), self.statsTextSize, self.half_w//3,
                               self.eighth_h + self.thirtytwo_h + self.sixteenth_h, color=self.white)

            self.MWO.draw_text("Total Games Won: " + str(stats["games_won"]), self.statsTextSize, self.half_w//3,
                               self.eighth_h + self.thirtytwo_h + (self.sixteenth_h * 2), color=self.white)

            self.MWO.draw_text("Total Win Percentage: " + str("{:.2f}".format(stats["win_percentage"])), self.statsTextSize, self.half_w//3,
                               self.eighth_h + self.thirtytwo_h + (self.sixteenth_h * 3), color=self.white)

            self.MWO.draw_text("Total Score: " + str(stats["total_score"]), self.statsTextSize, self.half_w//3,
                               self.eighth_h + self.thirtytwo_h + (self.sixteenth_h * 4), color=self.white)

            # Stats in middle
            self.MWO.draw_text("Escape The Fire Games Played: " + str(stats["etf_games"]), self.statsTextSize, self.half_w,
                               self.eighth_h + self.thirtytwo_h + self.sixteenth_h, color=self.white)

            self.MWO.draw_text("Escape The Fire Games Won: " + str(stats["etf_wins"]), self.statsTextSize, self.half_w,
                               self.eighth_h + self.thirtytwo_h + (self.sixteenth_h * 2), color=self.white)

            self.MWO.draw_text("Escape The Fire Win Percentage: " + str("{:.2f}".format(stats["etf_percentage"])), self.statsTextSize,
                               self.half_w, self.eighth_h + self.thirtytwo_h + (self.sixteenth_h * 3), color=self.white)

            self.MWO.draw_text("Escape The Fire Fire Paths Taken: " + str(stats["etf_fire_paths"]), self.statsTextSize, self.half_w,
                               self.eighth_h + self.thirtytwo_h + (self.sixteenth_h * 4), color=self.white)

            self.MWO.draw_text("Escape The Fire Water Paths Taken: " + str(stats["etf_water_paths"]), self.statsTextSize, self.half_w,
                               self.eighth_h + self.thirtytwo_h + (self.sixteenth_h * 5), color=self.white)

            # Stats on right side
            self.MWO.draw_text("Connect 4 Games Played: " + str(stats["c4_games"]), self.statsTextSize, self.half_w*1.65,
                               self.eighth_h + self.thirtytwo_h + self.sixteenth_h, color=self.white)

            self.MWO.draw_text("Connect 4 Games Won: " + str(stats["c4_wins"]), self.statsTextSize, self.half_w*1.65,
                               self.eighth_h + self.thirtytwo_h + (self.sixteenth_h * 2), color=self.white)

            self.MWO.draw_text("Connect 4 Win Percentage: " + str("{:.2f}".format(stats["c4_percentage"])), self.statsTextSize,
                               self.half_w*1.65, self.eighth_h + self.thirtytwo_h + (self.sixteenth_h * 3), color=self.white)

            self.MWO.draw_text("Connect 4 Pieces Placed: " + str(stats["c4_pieces_placed"]), self.statsTextSize, self.half_w*1.65,
                               self.eighth_h + self.thirtytwo_h + (self.sixteenth_h * 4), color=self.white)

            self.MWO.draw_text("Connect 4 Almost Wins: " + str(stats["c4_almost_wins"]), self.statsTextSize, self.half_w*1.65,
                               self.eighth_h + self.thirtytwo_h + (self.sixteenth_h * 5), color=self.white)

            # Draw Achievements
            self.MWO.draw_text("Achievements", 45, self.MWO.DISPLAY_W * 0.5, self.MWO.DISPLAY_H // 1.7, color=self.white)

            # Achievement distance dividers
            d = (self.MWO.DISPLAY_W // 6)
            constantD = (self.MWO.DISPLAY_W // 8)

            # Escape The Fire Achievements
            self.MWO.draw_image("Assets/Fire.png",d-constantD, self.achieveHeight,
                                self.achieveWidth, self.achieveWidth)
            self.MWO.draw_text("1", self.textAchieveSize,d-constantD + self.halfAchieveWidth,
                               self.achieveHeight + self.halfAchieveWidth)
            if stats["etf_wins"] < 1:
                self.MWO.draw_image("Assets/Lock.png",d-constantD, self.achieveHeight,
                                    self.achieveWidth, self.achieveWidth)
            self.MWO.draw_text("1 ETF Game Won", self.textAchieveSize // 4,
                              d-constantD + self.halfAchieveWidth,
                               self.achieveHeight + self.halfAchieveWidth * 3)

            self.MWO.draw_image("Assets/Fire.png",d*2-constantD, self.achieveHeight,
                                self.achieveWidth, self.achieveWidth)
            self.MWO.draw_text("10", self.textAchieveSize,d*2-constantD + self.halfAchieveWidth,
                               self.achieveHeight + self.halfAchieveWidth)
            if stats["etf_wins"] < 10:
                self.MWO.draw_image("Assets/Lock.png",d*2-constantD, self.achieveHeight,
                                    self.achieveWidth, self.achieveWidth)
            self.MWO.draw_text("10 ETF Games Won", self.textAchieveSize // 4,
                              d*2-constantD + self.halfAchieveWidth,
                               self.achieveHeight + self.halfAchieveWidth * 3)

            self.MWO.draw_image("Assets/WaterPath.png",d*3-constantD, self.achieveHeight,
                                self.achieveWidth, self.achieveWidth)
            self.MWO.draw_text("100", self.textAchieveSize//2,d*3-constantD + self.halfAchieveWidth,
                               self.achieveHeight + self.halfAchieveWidth)
            if stats["etf_water_paths"] < 100:
                self.MWO.draw_image("Assets/Lock.png",d*3-constantD, self.achieveHeight,
                                    self.achieveWidth, self.achieveWidth)
            self.MWO.draw_text("100 Water Paths Taken", self.textAchieveSize // 4,
                              d*3-constantD + self.halfAchieveWidth,
                               self.achieveHeight + self.halfAchieveWidth * 3)

            # Connect 4 achievements
            self.MWO.draw_image("Assets/C4A.png",d*4-constantD, self.achieveHeight,
                                self.achieveWidth, self.achieveWidth)
            self.MWO.draw_text("1", self.textAchieveSize,d*4-constantD + self.halfAchieveWidth,
                               self.achieveHeight + self.halfAchieveWidth)
            if stats["c4_wins"] < 1:
                self.MWO.draw_image("Assets/Lock.png",d*4-constantD, self.achieveHeight,
                                    self.achieveWidth, self.achieveWidth)
            self.MWO.draw_text("1 C4 Game Won", self.textAchieveSize // 4,
                              d*4-constantD + self.halfAchieveWidth,
                               self.achieveHeight + self.halfAchieveWidth * 3)

            self.MWO.draw_image("Assets/C4A.png",d*5-constantD, self.achieveHeight,
                                self.achieveWidth, self.achieveWidth)
            self.MWO.draw_text("10", self.textAchieveSize,d*5-constantD + self.halfAchieveWidth,
                               self.achieveHeight + self.halfAchieveWidth)
            if stats["c4_wins"] < 10:
                self.MWO.draw_image("Assets/Lock.png",d*5-constantD, self.achieveHeight,
                                    self.achieveWidth, self.achieveWidth)
            self.MWO.draw_text("10 C4 Games Won", self.textAchieveSize // 4,
                              d*5-constantD + self.halfAchieveWidth,
                               self.achieveHeight + self.halfAchieveWidth * 3)

            self.MWO.draw_image("Assets/C4P.png",d*6-constantD, self.achieveHeight,
                                self.achieveWidth, self.achieveWidth)
            self.MWO.draw_text("100", self.textAchieveSize//2,d*6-constantD + self.halfAchieveWidth,
                               self.achieveHeight + self.halfAchieveWidth)
            if stats["c4_pieces_placed"] < 100:
                self.MWO.draw_image("Assets/Lock.png",d*6-constantD, self.achieveHeight,
                                    self.achieveWidth, self.achieveWidth)
            self.MWO.draw_text("100 C4 Pieces Placed", self.textAchieveSize // 4,
                              d*6-constantD + self.halfAchieveWidth,
                               self.achieveHeight + self.halfAchieveWidth * 3)


            # "update" the screen
            self.blit_profile()

    def check_input(self):
        """
        Profile's state machine; checks input and acts accordingly
        :return: None
        """
        # check for Backspace or back button click to go back to MainMenu
        if self.MWO.BACKSPACE_KEY or self.backButton.clickCheck():
            self.MWO.current_screen = self.MWO.main_menu
            self.is_displaying = False

        # Draw leaderboards if leaderboard button is clicked
        if self.leaderButton.clickCheck():
            self.MWO.current_screen = self.MWO.Leaderboard
            self.is_displaying = False

    def blit_profile(self):
        """
        displays the drawn objects and then resets flags.
        :return: None
        """
        self.MWO.window.blit(self.MWO.display, (0, 0))
        pg.display.update()
        self.MWO.reset_key_inputs()