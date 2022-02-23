"""
GUI element to display an intermediate screen to choose the number of players
for ETF
"""
from Menu import Menu


class ChosePlayers(Menu):
    def __init__(self, window):
        Menu.__init__(self, window)
        self.window_state = "Exit"

        # number of players in the session
        self.n_play = int
        self.exit_in_chose = False

        # special box size
        self.TB_size_w = self.quarter_w
        self.SB_size_w = self.quarter_w / 4
        self.SB_size_h = self.quarter_w / 6

        # button offsets
        self.SB_offset = self.SB_size_w + 40

        # cord of utility button
        self.p1_x, self.p1_y = self.full_w / 4, self.full_h / 2
        self.p2_x, self.p2_y = self.p1_x + self.SB_offset, self.full_h / 2
        self.p3_x, self.p3_y = self.p2_x + self.SB_offset, self.full_h / 2
        self.p4_x, self.p4_y = self.p3_x + self.SB_offset, self.full_h / 2

        self.exit_x, self.exit_y = (self.full_w / 1.15), self.full_h / 1.2

        # cursor offsets
        self.cursor_offset_x = -5
        self.cursor_offset_y = -5

        # cursor initial size
        self.cursor_size_x = self.SB_size_w - (2 * self.cursor_offset_x)
        self.cursor_size_y = self.SB_size_h - (2 * self.cursor_offset_y)

        # cursor initial position
        self.cursor_pos_x = self.exit_x + self.cursor_offset_x
        self.cursor_pos_y = self.exit_y + self.cursor_offset_y

        self.choice = False

    def play(self):
        """
        main.py looks for play() to display it's screen upon selection
        """
        self.display_screen()

    def display_screen(self):
        """
        display_screen method that controls how the
        elements are displayed on the UI
        It overrides other display_screen methods,
        is the screen displayed when is_displaying== True
        """
        self.is_displaying = True
        while self.is_displaying:
            self.MWO.set_user_input()
            self.check_input()
            self.draw_background()
            self.draw_cursor()
            self.draw_buttons()
            self.blit_menu()

        return self.n_play

    def draw_background(self):
        self.MWO.display.fill((255, 140, 0))
        self.MWO.draw_image("Assets/Bubbles.jpg", self.thirtytwo_w, self.thirtytwo_h,
                            round(self.full_w - 2 * self.thirtytwo_w),
                            round(self.full_h - 2 * self.thirtytwo_h))
        self.MWO.draw_text("Select Number of players in Escape The Fire", 30,
                           self.full_w / 2, self.full_h / 16)

    def draw_buttons(self):
        """
        draw the action buttons
        """
        # draw p1, p2, p3, p4 buttons
        self.MWO.draw_rect((0, 0, 139), self.p2_x, self.p2_y, self.SB_size_w, self.SB_size_h)
        self.MWO.draw_rect((255, 255, 0), self.p3_x, self.p3_y, self.SB_size_w, self.SB_size_h)
        self.MWO.draw_rect((0, 255, 0), self.p4_x, self.p4_y, self.SB_size_w, self.SB_size_h)
        self.MWO.draw_rect((0, 50, 200), self.exit_x, self.exit_y, self.SB_size_w, self.SB_size_h)
        offset = 32
        offset_y=20
        # label buttons
        self.MWO.draw_text("Two", 30, self.p2_x + offset, self.p2_y - offset_y)
        self.MWO.draw_text("Three", 30, self.p3_x + offset, self.p3_y - offset_y)
        self.MWO.draw_text("Four", 30, self.p4_x + offset, self.p4_y - offset_y)
        self.MWO.draw_image('Assets/exit.png', self.exit_x, self.exit_y, round(self.SB_size_w), round(self.SB_size_h))
        self.MWO.draw_text("Exit", 30, self.exit_x, self.exit_y)

    def draw_cursor(self):
        """
        draws the cursor as a rectangle using Window's draw_rect
        :return: None
        """
        self.MWO.draw_rect((255, 100, 100), self.cursor_pos_x, self.cursor_pos_y, self.cursor_size_x,
                           self.cursor_size_y)

    def move_cursor(self):
        """
        It defines the cursor controlled with the arrow keys, allows UI elements
        """
        if self.MWO.LEFT_KEY:
            if self.window_state == "Exit":
                self.cursor_pos_x = self.p4_x + self.cursor_offset_x
                self.cursor_pos_y = self.p4_y + self.cursor_offset_y
                self.cursor_size_x = self.SB_size_w - (2 * self.cursor_offset_x)
                self.cursor_size_y = self.SB_size_h - (2 * self.cursor_offset_y)
                self.window_state = "p4"

            elif self.window_state == "p4":
                self.cursor_pos_x = self.p3_x + self.cursor_offset_x
                self.cursor_pos_y = self.p3_y + self.cursor_offset_y
                self.cursor_size_x = self.SB_size_w - (2 * self.cursor_offset_x)
                self.cursor_size_y = self.SB_size_h - (2 * self.cursor_offset_y)
                self.window_state = "p3"
            elif self.window_state == "p3":
                self.cursor_pos_x = self.p2_x + self.cursor_offset_x
                self.cursor_pos_y = self.p2_y + self.cursor_offset_y
                self.cursor_size_x = self.SB_size_w - (2 * self.cursor_offset_x)
                self.cursor_size_y = self.SB_size_h - (2 * self.cursor_offset_y)
                self.window_state = "p2"

        elif self.MWO.RIGHT_KEY:

            if self.window_state == "p2":
                self.cursor_pos_x = self.p3_x + self.cursor_offset_x
                self.cursor_pos_y = self.p3_y + self.cursor_offset_y
                self.cursor_size_x = self.SB_size_w - (2 * self.cursor_offset_x)
                self.cursor_size_y = self.SB_size_h - (2 * self.cursor_offset_y)
                self.window_state = "p3"
            elif self.window_state == "p3":
                self.cursor_pos_x = self.p4_x + self.cursor_offset_x
                self.cursor_pos_y = self.p4_y + self.cursor_offset_y
                self.cursor_size_x = self.SB_size_w - (2 * self.cursor_offset_x)
                self.cursor_size_y = self.SB_size_h - (2 * self.cursor_offset_y)
                self.window_state = "p4"
            elif self.window_state == "p4":
                self.cursor_pos_x = self.exit_x + self.cursor_offset_x
                self.cursor_pos_y = self.exit_y + self.cursor_offset_y
                self.cursor_size_x = self.SB_size_w - (2 * self.cursor_offset_x)
                self.cursor_size_y = self.SB_size_h - (2 * self.cursor_offset_y)
                self.window_state = "Exit"

    def check_input(self):
        self.move_cursor()

        if self.MWO.ENTER_KEY:
            if self.window_state == "Exit":
                self.MWO.playing = False
                self.n_play = 0

            elif self.window_state == "p2":
                self.n_play = 2

            elif self.window_state == "p3":
                self.n_play = 3

            elif self.window_state == "p4":
                self.n_play = 4

            self.is_displaying = False
            self.choice = True
