import pygame as pg
from Menu import Menu
from Database import Database


class Leaderboard(Menu):
    """
    Constructor for the Leaderboard page
    Menu --> a Window() object
    """
    def __init__(self, window):
        self.WIN = window
        Menu.__init__(self, window)
        self.is_displaying = False
        self.db = Database()

        # Colours
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.grey = (200, 200, 200)

        # back button to return to the profile page
        self.back = self.WIN.create_button(self.thirtytwo_w, self.thirtytwo_h, self.quarter_w / 3,
                                           self.quarter_h / 3, self.grey, self.black, text="Back")


    def display_screen(self):
        # get data from db
        c4_data = self.db.get_leaderboard("c4")
        etf_data = self.db.get_leaderboard("etf")
        self.is_displaying = True
        while self.is_displaying:
            self.WIN.set_user_input()
            self.check_input()

            # draw background
            self.WIN.draw_image('Assets/Bubbles.jpg', 0, 0, self.WIN.DISPLAY_W, self.WIN.DISPLAY_H)
            self.back.draw()

            # draw headers
            self.WIN.draw_text("Leaderboards", 45, self.WIN.DISPLAY_W * 0.5, self.WIN.DISPLAY_H / 10, self.white)
            self.WIN.draw_text("Connect Four", 30, self.WIN.DISPLAY_W * 0.25, self.WIN.DISPLAY_H / 5, self.white)
            self.WIN.draw_text("Escape the Fire", 30, self.WIN.DISPLAY_W * 0.75, self.WIN.DISPLAY_H / 5, self.white)

            # draw scores
            if c4_data is not None:
                height_mod = 0.3
                for i in range(len(c4_data)):
                    # extract name, score from current score
                    name = c4_data[i][0]
                    score = c4_data[i][1]
                    # draw current high score
                    self.WIN.draw_text(f"#{i + 1}", 27, self.WIN.DISPLAY_W * 0.15, self.WIN.DISPLAY_H * height_mod, self.white)
                    self.WIN.draw_text(f"{name}", 27, self.WIN.DISPLAY_W * 0.25, self.WIN.DISPLAY_H * height_mod, self.white)
                    self.WIN.draw_text(f"{score}", 27, self.WIN.DISPLAY_W * 0.35, self.WIN.DISPLAY_H * height_mod, self.white)
                    height_mod += 0.05

            if etf_data is not None:
                height_mod = 0.3
                for i in range(len(etf_data)):
                    name = etf_data[i][0]
                    score = etf_data[i][1]
                    self.WIN.draw_text(f"#{i + 1}", 27, self.WIN.DISPLAY_W * 0.65, self.WIN.DISPLAY_H * height_mod, self.white)
                    self.WIN.draw_text(f"{name}", 27, self.WIN.DISPLAY_W * 0.75, self.WIN.DISPLAY_H * height_mod, self.white)
                    self.WIN.draw_text(f"{score}", 27, self.WIN.DISPLAY_W * 0.85, self.WIN.DISPLAY_H * height_mod, self.white)
                    height_mod += 0.05

            self.blit_menu()


    def check_input(self):
        if self.WIN.BACKSPACE_KEY or self.back.clickCheck():
            # close database connection and switch to profile screen
            #self.db.close_connection()
            self.WIN.current_screen = self.WIN.profile
            self.is_displaying = False
