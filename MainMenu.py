import pygame as pg
from Menu import Menu
from ConnectFour import ConnectFour
from EscapeTheFire import EscapeTheFire
from DecisionScreen import DecisionScreen

class MainMenu(Menu):
    def __init__(self, window):
        """
        MainMenu's constructor
        :param window: A Window() Object
        """
        # init a Menu class object
        Menu.__init__(self, window)

        # initial state set on Game 1 (Connect Four)
        self.state = "CF"

        # text size
        self.text_size = round(self.full_w // 60)

        # button offsets
        self.GB_offset = 100
        self.SB_offset = 50

        # buttons sizes (GB = game menu buttons) (SB = setting buttons)
        self.GB_size_w = self.half_w / 1.5
        self.GB_size_h = self.half_h / 1.5
        self.SB_size_w = self.quarter_w / 4
        self.SB_size_h = self.quarter_w / 4


        # cords of game buttons
        self.connectfour_x, self.connectfour_y = self.quarter_w/2, self.quarter_h
        self.escapefire_x, self.escapefire_y = (self.full_w - self.connectfour_x - self.GB_size_w), self.quarter_h

        # cords of "setting" buttons (position is relative to EXIT button's position)
        self.profile_x, self.profile_y = (self.full_w / 1.15), self.full_h / 1.2
        self.options_x, self.options_y = (self.profile_x - self.SB_size_w - self.SB_offset), self.full_h / 1.2
        self.exit_x, self.exit_y = (self.options_x - self.SB_size_w - self.SB_offset), self.full_h / 1.2

        # cursor offsets
        self.cursor_offset_x = -5
        self.cursor_offset_y = -5

        # cursor initial size
        self.cursor_size_x = self.GB_size_w - (2*self.cursor_offset_x)
        self.cursor_size_y = self.GB_size_h - (2*self.cursor_offset_y)

        # cursor initial position
        self.cursor_pos_x = self.connectfour_x + self.cursor_offset_x
        self.cursor_pos_y = self.connectfour_y + self.cursor_offset_y

    def draw_cursor(self):
        """
        draws the cursor as a rectangle using Window's draw_rect
        :return: None
        """
        self.MWO.draw_rect((255, 100, 100),self.cursor_pos_x, self.cursor_pos_y, self.cursor_size_x, self.cursor_size_y)


    def draw_mainmenu(self):
        """
        Draws the main menu
        :return:
        """
        # draw background
        self.MWO.display.fill((225, 129, 38))
        #self.MWO.draw_rect(self.MWO.BLACK, self.thirtytwo_w, self.thirtytwo_h, self.full_w - 2 * self.thirtytwo_w, self.full_h - 2 * self.thirtytwo_h)
        self.MWO.draw_image("Assets/Bubbles.jpg", self.thirtytwo_w, self.thirtytwo_h,
                            round(self.full_w - 2 * self.thirtytwo_w),
                            round(self.full_h - 2 * self.thirtytwo_h))
        self.MWO.draw_text("UnderFire's collection", self.text_size + 10, self.full_w / 2, self.full_h / 10)

        # draw cursor
        self.draw_cursor()

        # draws game button squares and text
        self.MWO.draw_image("Assets/CF_preview.PNG", self.connectfour_x, self.connectfour_y, round(self.GB_size_w), round(self.GB_size_h))
        self.MWO.draw_image("Assets/ETF_board.png", self.escapefire_x, self.escapefire_y, round(self.GB_size_w), round(self.GB_size_h))

        self.MWO.draw_text("Connect Four", self.text_size, self.connectfour_x + self.GB_size_w/2, self.connectfour_y - 15)
        self.MWO.draw_text("Escape the Fire", self.text_size, self.escapefire_x + self.GB_size_w/2, self.escapefire_y - 15)

        # draws setting options squares and text
        # self.MWO.draw_rect((0, 100, 200), self.exit_x, self.exit_y, self.SB_size_w, self.SB_size_h)
        # self.MWO.draw_rect((150, 50, 200), self.options_x, self.options_y, self.SB_size_w, self.SB_size_h)
        # self.MWO.draw_rect((250, 0, 50), self.profile_x, self.profile_y, self.SB_size_w, self.SB_size_h)

        self.MWO.draw_text("Exit", self.text_size, self.exit_x + self.SB_size_h/2, self.exit_y-15)
        self.MWO.draw_text("Settings", self.text_size, self.options_x + self.SB_size_h/2, self.options_y-15)
        self.MWO.draw_text("Profile", self.text_size, self.profile_x + self.SB_size_h/2, self.profile_y-15)

    def draw_textures(self):
        """
        Draws images on the board
        :return: None
        """
        self.MWO.draw_image("Assets/exit.png", self.exit_x, self.exit_y, round(self.SB_size_w), round(self.SB_size_h))
        self.MWO.draw_image("Assets/cog.png", self.options_x, self.options_y, round(self.SB_size_w), round(self.SB_size_h))
        self.MWO.draw_image("Assets/profile.png", self.profile_x, self.profile_y, round(self.SB_size_w), round(self.SB_size_h))

    def display_screen(self):
        """
        the display loop that draws all required objects on screen.
        This happens every frame.
        :return: None
        """
        # making sure Main menu is_display is true
        self.is_displaying = True

        # Main menu's display loop (** displays in provided order**)
        while self.is_displaying:
            # checks for user input.
            self.MWO.set_user_input()
            self.check_input()

            # draw the main menu
            self.draw_mainmenu()
            # draw the textures
            self.draw_textures()
            # "update" the screen
            self.blit_menu()

    def move_cursor(self):
        """
        moves the cursor in the required direction, then sets the new state.
        :return: None
        """
        # changes state and cursor location

        # right key
        if self.MWO.RIGHT_KEY:
            if self.state == "CF":
                self.cursor_pos_x = self.escapefire_x + self.cursor_offset_x
                self.cursor_pos_y = self.escapefire_y + self.cursor_offset_y
                self.cursor_size_x = self.GB_size_w - (2 * self.cursor_offset_x)
                self.cursor_size_y = self.GB_size_h - (2 * self.cursor_offset_y)
                self.state = "ETF"

            elif self.state == "Exit":
                self.cursor_pos_x = self.options_x + self.cursor_offset_x
                self.cursor_pos_y = self.options_y + self.cursor_offset_y
                self.cursor_size_x = self.SB_size_w - (2 * self.cursor_offset_x)
                self.cursor_size_y = self.SB_size_h - (2 * self.cursor_offset_y)
                self.state = "Options"

            elif self.state == "Options":
                self.cursor_pos_x = self.profile_x + self.cursor_offset_x
                self.cursor_pos_y = self.profile_y + self.cursor_offset_y
                self.cursor_size_x = self.SB_size_w - (2 * self.cursor_offset_x)
                self.cursor_size_y = self.SB_size_h - (2 * self.cursor_offset_y)
                self.state = "Profile"
        # left key
        elif self.MWO.LEFT_KEY:
            if self.state == "ETF":
                self.cursor_pos_x = self.connectfour_x + self.cursor_offset_x
                self.cursor_pos_y = self.connectfour_y + self.cursor_offset_y
                self.cursor_size_x = self.GB_size_w - (2 * self.cursor_offset_x)
                self.cursor_size_y = self.GB_size_h - (2 * self.cursor_offset_y)
                self.state = "CF"

            elif self.state == "Options":
                self.cursor_pos_x = self.exit_x + self.cursor_offset_x
                self.cursor_pos_y = self.exit_y + self.cursor_offset_y
                self.cursor_size_x = self.SB_size_w - (2 * self.cursor_offset_x)
                self.cursor_size_y = self.SB_size_h - (2 * self.cursor_offset_y)
                self.state = "Exit"

            elif self.state == "Profile":
                self.cursor_pos_x = self.options_x + self.cursor_offset_x
                self.cursor_pos_y = self.options_y + self.cursor_offset_y
                self.cursor_size_x = self.SB_size_w - (2 * self.cursor_offset_x)
                self.cursor_size_y = self.SB_size_h - (2 * self.cursor_offset_y)
                self.state = "Options"
        # down key
        elif self.MWO.DOWN_KEY:
            if self.state == "CF" or self.state == "ETF":
                self.cursor_pos_x = self.exit_x + self.cursor_offset_x
                self.cursor_pos_y = self.exit_y + self.cursor_offset_y
                self.cursor_size_x = self.SB_size_w - (2 * self.cursor_offset_x)
                self.cursor_size_y = self.SB_size_h - (2 * self.cursor_offset_y)
                self.state = "Exit"
        # up key
        elif self.MWO.UP_KEY:
            if self.state != "CF" or self.state != "ETF":
                self.cursor_pos_x = self.escapefire_x + self.cursor_offset_x
                self.cursor_pos_y = self.escapefire_y + self.cursor_offset_y
                self.cursor_size_x = self.GB_size_w - (2 * self.cursor_offset_x)
                self.cursor_size_y = self.GB_size_h - (2 * self.cursor_offset_y)
                self.state = "ETF"

        # mouse positions
        # over CF
        elif self.connectfour_x < self.MWO.mx < self.connectfour_x + self.GB_size_w and self.connectfour_y < self.MWO.my < self.connectfour_y + self.GB_size_h:
            self.cursor_pos_x = self.connectfour_x + self.cursor_offset_x
            self.cursor_pos_y = self.connectfour_y + self.cursor_offset_y
            self.cursor_size_x = self.GB_size_w - (2 * self.cursor_offset_x)
            self.cursor_size_y = self.GB_size_h - (2 * self.cursor_offset_y)
            self.state = "CF"

        # over ETF
        elif self.escapefire_x < self.MWO.mx < self.escapefire_x + self.GB_size_w and self.escapefire_y < self.MWO.my < self.escapefire_y + self.GB_size_h:
            self.cursor_pos_x = self.escapefire_x + self.cursor_offset_x
            self.cursor_pos_y = self.escapefire_y + self.cursor_offset_y
            self.cursor_size_x = self.GB_size_w - (2 * self.cursor_offset_x)
            self.cursor_size_y = self.GB_size_h - (2 * self.cursor_offset_y)
            self.state = "ETF"

        elif self.options_x < self.MWO.mx < self.options_x + self.SB_size_w and self.options_y < self.MWO.my < self.options_y + self.SB_size_h:
            self.cursor_pos_x = self.options_x + self.cursor_offset_x
            self.cursor_pos_y = self.options_y + self.cursor_offset_y
            self.cursor_size_x = self.SB_size_w - (2 * self.cursor_offset_x)
            self.cursor_size_y = self.SB_size_h - (2 * self.cursor_offset_y)
            self.state = "Options"

        elif self.profile_x < self.MWO.mx < self.profile_x + self.SB_size_w and self.profile_y < self.MWO.my < self.profile_y + self.SB_size_h:
            self.cursor_pos_x = self.profile_x + self.cursor_offset_x
            self.cursor_pos_y = self.profile_y + self.cursor_offset_y
            self.cursor_size_x = self.SB_size_w - (2 * self.cursor_offset_x)
            self.cursor_size_y = self.SB_size_h - (2 * self.cursor_offset_y)
            self.state = "Profile"

        elif self.exit_x < self.MWO.mx < self.exit_x + self.SB_size_w and self.exit_y < self.MWO.my < self.exit_y + self.SB_size_h:
            self.cursor_pos_x = self.exit_x + self.cursor_offset_x
            self.cursor_pos_y = self.exit_y + self.cursor_offset_y
            self.cursor_size_x = self.SB_size_w - (2 * self.cursor_offset_x)
            self.cursor_size_y = self.SB_size_h - (2 * self.cursor_offset_y)
            self.state = "Exit"



    def check_input(self):
        """
        MainMenu's state machine; checks which state its currently in
        an sets the screen and cursor position accordingly.
        :return: None
        """
        # move the cursor
        self.move_cursor()

        # Enter will swap the screen
        if self.MWO.ENTER_KEY:
            if self.state == "CF":
                # create a new CF and pass it into DecisionScreen
                new_game = ConnectFour(self.MWO)
                self.MWO.current_screen = DecisionScreen(self.MWO, new_game)

            elif self.state == "ETF":
                # create a new ETF and pass it into DecisionScreen
                new_game = EscapeTheFire(self.MWO)
                self.MWO.current_screen = DecisionScreen(self.MWO, new_game)

            elif self.state == "Options":
                self.MWO.current_screen = self.MWO.options_menu

            elif self.state == "Profile":
                self.MWO.current_screen = self.MWO.profile

            elif self.state == "Exit":
                self.MWO.running = False
                self.MWO.playing = False
            # set Main Menu's is_displaying to false
            self.is_displaying = False

        # mouse inputs, duplicate and messy code:(
        elif self.MWO.LEFT_CLICK:
            # check if mouse is "inside" each button
            if self.connectfour_x < self.MWO.mx < self.connectfour_x + self.GB_size_w and self.connectfour_y < self.MWO.my < self.connectfour_y + self.GB_size_h:
                new_game = ConnectFour(self.MWO)
                self.MWO.current_screen = DecisionScreen(self.MWO, new_game)

            elif self.escapefire_x < self.MWO.mx < self.escapefire_x + self.GB_size_w and self.escapefire_y < self.MWO.my < self.escapefire_y + self.GB_size_h:
                new_game = EscapeTheFire(self.MWO)
                self.MWO.current_screen = DecisionScreen(self.MWO, new_game)

            elif self.options_x < self.MWO.mx < self.options_x + self.SB_size_w and self.options_y < self.MWO.my < self.options_y + self.SB_size_h:
                self.MWO.current_screen = self.MWO.options_menu

            elif self.profile_x < self.MWO.mx < self.profile_x + self.SB_size_w and self.profile_y < self.MWO.my < self.profile_y + self.SB_size_h:
                self.MWO.current_screen = self.MWO.profile

            elif self.exit_x < self.MWO.mx < self.exit_x + self.SB_size_w and self.exit_y < self.MWO.my < self.exit_y + self.SB_size_h:
                self.MWO.running = False
                self.MWO.playing = False
            # set Main Menu's is_displaying to false
            self.is_displaying = False