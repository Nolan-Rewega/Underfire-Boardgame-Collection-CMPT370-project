from Menu import Menu
from Database import Database


class HiscoreScreen(Menu):
    def __init__(self, window, score, game_name):
        """
        HighScores's constructor
        """
        # init a Menu class object
        Menu.__init__(self, window)

        # open database
        self.db = Database()
        self.game_name = game_name
        self.score_list = self.db.get_leaderboard(self.game_name)
        # text size
        self.text_size = round(self.full_w // 60)

        # init alphabet
        self.alphabet = ["A","B","C","D","E","F","G","H","I",
                         "J","K","L","M","N","O","P","Q","R",
                         "S","T","U","V","W","X","Y","Z","1",
                         "2","3","4","5","6","7","8","9","0",
                         "!","?","@","$","%","^",'&',"*","#" ]
        self.alphabet_ptr = 0

        # initial state is empty
        self.user_name = ["_","_","_","_"]
        self.char_indicator = 0

        self.player_score = score
        # char constants
        self.CHAR_BLANK = "_"

        # text offsets
        self.scores_offset_y = round(self.full_h // 20)
        self.outline_offset = 10
        # buttons sizes (GB = game menu buttons) (SB = setting buttons)
        self.panel_w, self.panel_h = self.full_w * (2/4), self.full_h * (3/4)

        # cords of game buttons
        self.center_box_x, self.center_box_y = self.quarter_w, self.quarter_h / 2

        # cords of text
        self.enter_box_x, self.enter_box_y = self.half_w, self.quarter_h
        self.text_x = self.half_w

        # cords of "setting" buttons (position is relative to EXIT button's position)

    def display_screen(self):
        """
        Main display loop for HiscoreScreen.py
        """
        self.is_displaying = True

        while self.is_displaying:
            # checks for user input.
            self.MWO.set_user_input()
            self.check_input()

            # draw the main screen panel
            self.draw_panel()
            # draw text
            self.draw_text()
            # draw the score indicator
            self.draw_user_initials()
            # draw leaderboards
            self.draw_leaderboards()

            # blit the menu
            self.blit_menu()

    def draw_panel(self):
        """
        draws the background panel on screen
        """
        self.MWO.draw_rect((225, 129, 38),
                           self.center_box_x - self.outline_offset,
                           self.center_box_y - self.outline_offset,
                           self.panel_w + (self.outline_offset * 2),
                           self.panel_h + (self.outline_offset * 2))

        self.MWO.draw_rect((0, 0, 0), self.center_box_x, self.center_box_y, self.panel_w, self.panel_h*(1/2))
        self.MWO.draw_rect((15, 15, 15), self.center_box_x,
                           self.center_box_y + self.panel_h*(1/2), self.panel_w, self.panel_h*(1/2))

    def draw_text(self):
        """
        draws all text objects on screen
        """
        self.MWO.draw_text("Enter your name using the arrow keys...", self.text_size, self.text_x,
                           self.center_box_y + (self.panel_h * (1 / 10)), (200, 0, 0))
        self.MWO.draw_text("Hit Enter to confirm or Backspace to undo", self.text_size, self.text_x,
                           self.center_box_y + (self.panel_h * (1 / 6)), (200, 0, 0))
        self.MWO.draw_text("Hit Escape to quit without saving", self.text_size, self.text_x,
                           self.center_box_y + (self.panel_h * (8 / 9)), (200, 0, 0))

    def draw_leaderboards(self):
        """
        draws the top 5 scores from the database on screen
        """
        self.MWO.draw_text("TOP 5 SCORES", self.text_size, self.text_x, self.center_box_y + (self.panel_h * (1 / 3.1)), (0, 210, 0))
        if self.score_list is None:
            pass
        else:
            place = 1
            color = (0,0,0)
            pos = ""
            size = 5
            if len(self.score_list) < 5:
                size = len(self.score_list)
            for idx in range(0, size):
                score = self.score_list[idx]
                # reformat place into a position string
                if place == 1: pos, color = "1st   ", (255,255,50)
                if place == 2: pos, color = "2nd   ", (160,160,160)
                if place == 3: pos, color = "3rd   ", (150,70,0)
                if place == 4: pos, color = "4th   ", (255,205,220)
                if place == 5: pos, color = "5th   ", (255,205,220)

                score_str = pos + str(score[1]) + "   " + str(score[0])
                self.MWO.draw_text(score_str, self.text_size, self.text_x,
                                   self.center_box_y + (self.panel_h * (1 / 3) + (self.scores_offset_y * place)), color)
                # increment
                place += 1


    def draw_user_initials(self):
        """
        Draws the user's selected chars on the screen
        """
        usr_initials_str = ""
        # build the user string
        for letter in self.user_name:
            usr_initials_str += letter + " "

        self.MWO.draw_text(usr_initials_str + "  Score: " + str(self.player_score), self.text_size, self.text_x,
                           self.center_box_y + (self.panel_h*(1/4)))

    def check_input(self):
        """
        checks the user input and apply a action from the current state
        """
        # Enter
        if self.MWO.ENTER_KEY:
            if self.char_indicator <= 3:
                self.user_name[self.char_indicator] = self.alphabet[self.alphabet_ptr]
                if self.char_indicator == 3:
                    name = ""
                    for char in self.user_name:
                        name += char
                    # update the database
                    self.db.update_leaderboard(self.game_name, name, self.player_score)
                    self.is_displaying = False
                    self.db.close_connection()
                    self.MWO.current_screen = self.MWO.main_menu
                else:
                    self.user_name[self.char_indicator + 1] = self.alphabet[self.alphabet_ptr]
                    self.char_indicator += 1
        # escape key
        elif self.MWO.ESCAPE_KEY:
            self.is_displaying = False
            self.db.close_connection()
            self.MWO.current_screen = self.MWO.main_menu

        # back space
        elif self.MWO.BACKSPACE_KEY:
            if self.char_indicator >= 0:
                self.user_name[self.char_indicator] = self.CHAR_BLANK
                if self.char_indicator != 0:
                    self.char_indicator -= 1

        # up arrow or down arrow
        elif self.MWO.UP_KEY or self.MWO.DOWN_KEY:
            if self.MWO.UP_KEY:
                # can get infinite negative prt number
                self.alphabet_ptr = (self.alphabet_ptr + 1) % len(self.alphabet)
            else:
                # can get infinite negative prt number
                self.alphabet_ptr = (self.alphabet_ptr - 1) % len(self.alphabet)
            # update the text
            self.user_name[self.char_indicator] = self.alphabet[self.alphabet_ptr]





















