from Menu import Menu

class DecisionScreen(Menu):
    def __init__(self, window, picked_game_obj):
        Menu.__init__(self, window)

        # state
        self.state = "LeftBox"
        self.decision_state = "AI"
        self.selected_game = picked_game_obj

        # text size
        self.text_size = round(self.full_w // 50)

        # offsets
        self.outline_offset = 15
        self.cursor_offset_x = -5
        self.cursor_offset_y = -5

        # decision box size
        self.DB_size_w, self.DB_size_h, = self.half_w, self.full_h / 1.5
        self.LB_size_w, self.LB_size_h, = self.quarter_w / 4, self.quarter_h / 2

        # cords of AI and load game screen
        self.decision_x, self.decision_y = self.quarter_w, self.sixteenth_h
        self.load_x, self.load_y = self.decision_x + (self.DB_size_w*(1/8)), self.half_h
        self.new_game_x, self.new_game_y = self.decision_x + (self.DB_size_w*(3/4)), self.half_h

        self.cursor_pos_x = self.load_x + self.cursor_offset_x
        self.cursor_pos_y = self.load_y + self.cursor_offset_y
        self.cursor_size_x = self.LB_size_w - (2 * self.cursor_offset_x)
        self.cursor_size_y = self.LB_size_h - (2 * self.cursor_offset_y)

    def draw_decision_screen(self):
        """
        Draws the load and save screens
        :return: None
        """
        self.MWO.draw_rect((225, 129, 38),
                           self.decision_x - self.outline_offset,
                           self.decision_y - self.outline_offset,
                           self.DB_size_w + (self.outline_offset * 2),
                           self.DB_size_h + (self.outline_offset * 2))

        self.MWO.draw_rect((0, 0, 0), self.decision_x, self.decision_y, self.DB_size_w, self.DB_size_h)

        self.MWO.draw_text("Press Escape to go back", self.text_size, self.half_w,
                           self.decision_y + (self.DB_size_h * (1/8)), (40, 40, 40))
        # draw the cursor
        self.draw_cursor()

        if self.decision_state == "Load":
            self.MWO.draw_text("Do you want to load last saved game?", self.text_size, self.half_w, self.quarter_h, (100, 200, 40))
            self.MWO.draw_rect((0, 0, 100), self.load_x, self.load_y, self.LB_size_w, self.LB_size_h)
            self.MWO.draw_text("Load", self.text_size, self.load_x + self.LB_size_w/2, self.load_y - self.text_size, (100, 200, 40))
            self.MWO.draw_rect((0, 0, 100), self.new_game_x, self.new_game_y, self.LB_size_w, self.LB_size_h)
            self.MWO.draw_text("New", self.text_size, self.new_game_x + self.LB_size_w/2, self.new_game_y - self.text_size, (100, 200, 40))

        elif self.decision_state == "AI":
            self.MWO.draw_text("Do you want to play against AI?", self.text_size, self.half_w, self.quarter_h, (100, 200, 40))
            self.MWO.draw_rect((0, 100, 100), self.load_x, self.load_y, self.LB_size_w, self.LB_size_h)
            self.MWO.draw_text("Yes", self.text_size, self.load_x + self.LB_size_w/2, self.load_y - self.text_size, (100, 200, 40))
            self.MWO.draw_rect((0, 100, 100), self.new_game_x, self.new_game_y , self.LB_size_w, self.LB_size_h)
            self.MWO.draw_text("No", self.text_size, self.new_game_x + self.LB_size_w/2, self.new_game_y - self.text_size, (100, 200, 40))

    def draw_cursor(self):
        """
        draws the cursor on screen
        """
        self.MWO.draw_rect((255, 100, 100), self.cursor_pos_x, self.cursor_pos_y, self.cursor_size_x,
                           self.cursor_size_y)

    def display_screen(self):
        """
        Main Display loop for DecisionScreen
        """
        self.is_displaying = True

        while self.is_displaying:
            # check for user inputs
            self.MWO.set_user_input()
            self.check_input()

            # draw the background
            self.draw_decision_screen()

            self.blit_menu()


    def move_cursor(self):
        """
        change where the cursor is draw based on the current windows state
        :return: None
        """

        if self.MWO.RIGHT_KEY or \
                (self.new_game_x < self.MWO.mx < self.new_game_x + self.LB_size_w
                 and self.new_game_y < self.MWO.my < self.new_game_y + self.LB_size_h):
            if self.state == "LeftBox":
                self.cursor_pos_x = self.new_game_x + self.cursor_offset_x
                self.cursor_pos_y = self.new_game_y + self.cursor_offset_y
                self.cursor_size_x = self.LB_size_w - (2 * self.cursor_offset_x)
                self.cursor_size_y = self.LB_size_h - (2 * self.cursor_offset_y)
                self.state = "RightBox"

        elif self.MWO.LEFT_KEY or \
                (self.load_x < self.MWO.mx < self.load_x + self.LB_size_w
                 and self.load_y < self.MWO.my < self.load_y + self.LB_size_h):
            if self.state == "RightBox":
                self.cursor_pos_x = self.load_x + self.cursor_offset_x
                self.cursor_pos_y = self.load_y + self.cursor_offset_y
                self.cursor_size_x = self.LB_size_w - (2 * self.cursor_offset_x)
                self.cursor_size_y = self.LB_size_h - (2 * self.cursor_offset_y)
                self.state = "LeftBox"

    def check_input(self):
        """
        checks the user input and apply a action from the current state
        :return: None
        """
        # change cursor position
        self.move_cursor()

        if self.MWO.ENTER_KEY:
            if self.state == "LeftBox":
                # get game from DB
                if self.decision_state == "Load":
                    self.is_displaying = False
                    self.MWO.playing = True
                    self.selected_game.load_from_db()
                    self.MWO.current_screen = self.selected_game
                # set AI flag
                elif self.decision_state == "AI":
                    self.decision_state = "Load"
                    self.selected_game.change_ai(True)

            elif self.state == "RightBox":
                # new game
                if self.decision_state == "Load":
                    self.is_displaying = False
                    self.MWO.playing = True
                    self.MWO.current_screen = self.selected_game
                # no AI
                elif self.decision_state == "AI":
                    self.decision_state = "Load"
                    self.selected_game.change_ai(False)
        elif self.MWO.LEFT_CLICK:
            if (self.load_x < self.MWO.mx < self.load_x + self.LB_size_w
                 and self.load_y < self.MWO.my < self.load_y + self.LB_size_h):
                # get game from DB
                if self.decision_state == "Load":
                    self.is_displaying = False
                    self.MWO.playing = True
                    self.selected_game.load_from_db()
                    self.MWO.current_screen = self.selected_game
                # set AI flag
                elif self.decision_state == "AI":
                    self.decision_state = "Load"
                    self.selected_game.change_ai(True)

            elif (self.new_game_x < self.MWO.mx < self.new_game_x + self.LB_size_w
                 and self.new_game_y < self.MWO.my < self.new_game_y + self.LB_size_h):
                # new game
                if self.decision_state == "Load":
                    self.is_displaying = False
                    self.MWO.playing = True
                    self.MWO.current_screen = self.selected_game
                # no AI
                elif self.decision_state == "AI":
                    self.decision_state = "Load"
                    self.selected_game.change_ai(False)

        # check backspace
        elif self.MWO.BACKSPACE_KEY:
            if self.decision_state == "Load":
                self.decision_state = "AI"

        # check escape
        elif self.MWO.ESCAPE_KEY:
            self.is_displaying = False
            self.MWO.current_screen = self.MWO.main_menu

