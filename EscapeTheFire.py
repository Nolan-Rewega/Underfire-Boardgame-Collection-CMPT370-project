from State import State
import Dice as dice
import time
from Game import Game
from ChosePlayers import ChosePlayers
import pygame as pg
from Database import Database
from HiscoreScreen import HiscoreScreen


class EscapeTheFire(Game):

    def __init__(self, window):
        Game.__init__(self, window)

        # the number of players in the game
        # zero means exit
        self.nPlayers = 0
        self.roll_die = 1

        # controls the Elements
        self.game_State = State()

        # created data base:
        self.db = Database()

        # new game flag
        self.new_game = True

        # score variable
        self.score = 0
        self.winner = 0

        # GUI ELEMENTS
        self.N_ROWS = 10
        self.N_COLS = 10

        # initial state set on Game 2 (Escape te fire)
        self.window_state = "Exit"

        # button offsets
        self.SB_offset = 50
        self.GB_offset = 50

        self.Die_offset = 15
        self.small_x_offset = 100

        # text size
        self.text_size = round(self.full_w // 60)

        ## Game box, special box(utilities) (Text box)
        self.GB_size_w = self.full_w * (3 / 5)
        self.TB_size_w = self.quarter_w
        self.GB_size_h = self.full_h * (2 / 3)
        self.SB_size_w = self.quarter_w / 4
        self.SB_size_h = self.SB_size_w

        # cords of game rect's
        self.board_x, self.board_y = self.sixteenth_w, self.quarter_h / 2
        self.text_box_x, self.text_box_y = (self.board_x + self.GB_size_w + self.GB_offset), self.quarter_h / 2
        # dice position
        self.die_x = self.full_w/12

        # cords of utility buttons
        self.exit_x, self.exit_y = (self.full_w / 1.15), self.full_h / 1.2
        self.undo_x, self.undo_y = (self.exit_x - self.SB_size_w - self.SB_offset), self.full_h / 1.2
        self.next_x, self.next_y = (self.board_x + (self.GB_size_w * (2 / 3))), self.full_h / 1.2

        self.roll_x, self.roll_y = (self.next_x + self.small_x_offset * 2), self.next_y

        self.details_x, self.details_y = (self.board_x + self.GB_size_w * 0.5), self.board_y + self.GB_size_h * 1.1
        # cursor offsets
        self.cursor_offset_x = -5
        self.cursor_offset_y = -5

        # cursor initial size
        self.cursor_size_x = self.SB_size_w - (2 * self.cursor_offset_x)
        self.cursor_size_y = self.SB_size_h - (2 * self.cursor_offset_y)

        # cursor initial position
        self.cursor_pos_x = self.exit_x + self.cursor_offset_x
        self.cursor_pos_y = self.exit_y + self.cursor_offset_y

        self.curr = 0
        self.dest = 0

    def save_to_db(self):
        """
        Saves a given 2D array into the data base.
        :return:None
        """
        # add score or other things here, just append to save.
        current_player = self.game_State.get_current_player().get_identifier()
        save = [self.game_State._gameState, self.score, self.nPlayers, current_player]
        self.db.save_game_state('etf', save)

    def load_from_db(self):
        """
        load save state from Database, and reconstruct it into a 2D array
        :return: None
        """
        # fetch that data
        read_data = self.db.get_game_state("etf")
        self.new_game = False

        if read_data is not None:
            # get the list
            self.game_State._gameState = read_data[0]
            self.score = read_data[1]
            # set the number of players
            self.nPlayers = read_data[2]
            # set the current player
            self.game_State._players.set_current_player(read_data[3])

    def save_stats(self):
        """
        Saves the user Stats to the database
        :return: None
        """
        stats = self.db.get_stats()

        stat_list = self.game_State.get_stats()
        print(stat_list)

        stats["fire_paths"] = stat_list[0]
        stats["water_paths"] = stat_list[1]
        stats["score"] = self.score

        outcome = 0
        if self.winner == -1:
            outcome = 1
        self.db.update_stats('etf', outcome, stats)

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
        # display the player choice screen first
        self.is_displaying = True

        if self.new_game:
            # new game then choose the number of players
            self.nPlayers = ChosePlayers(self.MWO).display_screen()

        # check if player exited in choose player screen
        if self.nPlayers == 0:
            self.is_displaying = False
            self.MWO.playing = False
            self.save_stats()
            self.MWO.current_screen = self.MWO.main_menu
        else:
            # refer to documentation for EFT_Init() in states.py
            self.game_State.n_players = self.nPlayers
            self.game_State.ETF_Init(self.new_game)

        # loop until some end condition or EXIT is chosen
        while self.is_displaying:
            self.MWO.set_user_input()
            self.check_input()
            # BACKGROUND #######
            self.draw_background()
            # draw the cursor that will be used to select elements on the UI
            self.draw_cursor()
            # draw buttons that will be used to carry out actions on the UI
            self.draw_buttons()
            # draw the game pieces that represent the players on the board
            self.draw_pieces()
            # draw the grid lines on the game board
            self.draw_grid(self.N_ROWS, self.N_COLS, self.GB_size_w / self.N_COLS, self.GB_size_h / self.N_ROWS,
                           self.GB_size_w, self.GB_size_h, self.board_x, self.board_y)
            self.display_info()
            self.draw_instructions()
            self.draw_die(self.roll_die)

            self.blit_game()

            # time.sleep(0.1)  # stall simulation for visual understanding ## DEBUG
        self.game_State.clear_state()

    def display_info(self):
        """
        draws the current players move details, such as start and end points
        if a event is triggered ...etc
        :return: None
        """
        details = ""
        if self.nPlayers == 1 or self.nPlayers == 2:
            if self.game_State._players.get_current_player_int() == -1:
                details = self.game_State.player_console_descrip(self.curr, self.dest, -2)
            else:
                details = self.game_State.player_console_descrip(self.curr, self.dest, -1)
        elif self.nPlayers == 3:
            if self.game_State._players.get_current_player_int() == -1:
                details = self.game_State.player_console_descrip(self.curr, self.dest, -3)
            elif self.game_State._players.get_current_player_int() == -2:
                details = self.game_State.player_console_descrip(self.curr, self.dest, -1)
            elif self.game_State._players.get_current_player_int() == -3:
                details = self.game_State.player_console_descrip(self.curr, self.dest, -2)
        elif self.nPlayers == 4:
            if self.game_State._players.get_current_player_int() == -1:
                details = self.game_State.player_console_descrip(self.curr, self.dest, -4)
            elif self.game_State._players.get_current_player_int() == -2:
                details = self.game_State.player_console_descrip(self.curr, self.dest, -1)
            elif self.game_State._players.get_current_player_int() == -3:
                details = self.game_State.player_console_descrip(self.curr, self.dest, -2)
            elif self.game_State._players.get_current_player_int() == -4:
                details = self.game_State.player_console_descrip(self.curr, self.dest, -3)
        self.MWO.draw_text(details, self.text_size, self.details_x, self.details_y - 30)

    def draw_background(self):
        """
        Draws all the background Objects
        :return: None
        """
        # BACKGROUND #######
        self.MWO.display.fill((110,69,19))
        self.MWO.draw_image("Assets/Bubbles.jpg", self.thirtytwo_w, self.thirtytwo_h,
                            round(self.full_w - 2 * self.thirtytwo_w),
                            round(self.full_h - 2 * self.thirtytwo_h))
        self.MWO.draw_image('Assets/ETF_board.png', self.board_x, self.board_y, round(self.GB_size_w),
                            round(self.GB_size_h))

        self.MWO.draw_text("Escape The Fire", self.text_size, self.full_w / 2, self.full_h / 16)
        self.MWO.draw_text("Score: " + str(self.score), self.text_size, self.board_x + (self.GB_size_w * (1 / 6)),
                           self.board_y - 20, (110, 40, 110))

    def draw_cursor(self):
        """
        draws the cursor as a rectangle using Window's draw_rect
        :return: None
        """
        self.MWO.draw_rect((255, 100, 100), self.cursor_pos_x, self.cursor_pos_y, self.cursor_size_x,
                           self.cursor_size_y)

    def draw_buttons(self):
        """
        draw the action buttons
        """
        # draw rectangles and text box
        self.MWO.draw_rect((240,230,140), self.text_box_x, self.text_box_y, self.TB_size_w, self.GB_size_h)
        self.MWO.draw_text("Instructions", self.text_size, self.text_box_x + self.TB_size_w / 2, self.text_box_y-25)

        # draw utility box's
        self.MWO.draw_image('Assets/exit.png', self.exit_x, self.exit_y, round(self.SB_size_w), round(self.SB_size_h))
        self.MWO.draw_text("Exit", self.text_size, self.exit_x, self.exit_y)

        # NEW ROLL button
        self.MWO.draw_rect((0, 124, 100), self.roll_x, self.roll_y, self.SB_size_w, self.SB_size_h)
        self.MWO.draw_image('Assets/die.png', self.roll_x, self.roll_y, round(self.SB_size_w), round(self.SB_size_h))
        self.MWO.draw_text("ROLL", 30, self.roll_x, self.roll_y)

    def draw_grid(self, num_lines_x, num_lines_y, offset_x, offset_y, len_x, len_y, start_x, start_y):
        """
        Draws a grid given a starting point
        :param num_lines_x:
        :param num_lines_y:
        :param offset_x: spacing between each col
        :param offset_y: spacing between each row
        :param len_x: the length of x lines
        :param len_y:
        :param start_x:
        :param start_y:
        :return:
        """
        for i in range(1, num_lines_x):
            pg.draw.line(self.MWO.display, (200, 200, 200),
                         (start_x, start_y + offset_y * i),
                         (len_x + start_x, start_y + offset_y * i), 2)

        for j in range(1, num_lines_y):
            pg.draw.line(self.MWO.display, (200, 200, 200),
                         (offset_x * j + start_x, start_y),
                         (offset_x * j + start_x, len_y + start_y), 2)

    def draw_pieces(self):
        """
        Draws the every piece on the board
        :return:
        """
        # draw player pieces on the board

        # 1 square size
        size_x = self.GB_size_w / self.N_COLS
        size_y = self.GB_size_h / self.N_ROWS

        n_items = 100

        blah = size_x * 0.25
        for i in range(1, n_items + 1):
            # token can be a list, -1, -2, -3, -4 or 0
            token = self.game_State.get_gamestate_position(i)
            if token != 0:
                for item in token:
                    j = i - 1
                    if item == -1:
                        self.MWO.draw_rect((255, 0, 0),
                                           self.board_x + (size_x * (j % self.N_COLS)),
                                           self.board_y + (size_y * (j // self.N_ROWS)), blah, size_y)
                    if item == -2:
                        self.MWO.draw_rect((0, 0, 139),
                                           self.board_x + (size_x * (j % self.N_COLS)) + size_x * 0.25,
                                           self.board_y + (size_y * (j // self.N_ROWS)), blah, size_y)
                    if item == -3:
                        self.MWO.draw_rect((255, 255, 0),
                                           self.board_x + (size_x * (j % self.N_COLS)) + size_x * 0.50,
                                           self.board_y + (size_y * (j // self.N_ROWS)), blah, size_y)
                    if item == -4:
                        self.MWO.draw_rect((0, 255, 0),
                                           self.board_x + (size_x * (j % self.N_COLS)) + size_x * 0.75,
                                           self.board_y + (size_y * (j // self.N_ROWS)), blah, size_y)

    def draw_die(self, roll):
        """
        Draws the preview dice in the bottom left corner
        :param roll: A Integer representing the number rolled
        :return: None
        """
        n = roll
        spot_size = 9
        midpoint = int(self.die_x / 2)
        left = top = int(self.die_x / 4)
        right = bottom = self.die_x - left
        spot_col = (0, 127, 127)
        self.MWO.draw_rect((255, 255, 127), self.board_x, self.full_h * 0.8, self.die_x, self.die_x)
        if n % 2 == 1:  # draw the centre dot
            pg.draw.circle(self.MWO.display, spot_col, (midpoint + self.board_x, midpoint + self.full_h * 0.80),
                           spot_size)
        if n == 2 or n == 3 or n == 4 or n == 5 or n == 6:
            pg.draw.circle(self.MWO.display, spot_col, (left + self.board_x, bottom + self.full_h * 0.80),
                           spot_size)  # left bottom
            pg.draw.circle(self.MWO.display, spot_col, (right + self.board_x, top + self.full_h * 0.80),
                           spot_size)  # right top
        if n == 4 or n == 5 or n == 6:
            pg.draw.circle(self.MWO.display, spot_col, (left + self.board_x, top + self.full_h * 0.80),
                           spot_size)  # left top
            pg.draw.circle(self.MWO.display, spot_col, (right + self.board_x, bottom + self.full_h * 0.80),
                           spot_size)  # right bottom
        if n == 6:
            pg.draw.circle(self.MWO.display, spot_col, (midpoint + self.board_x, bottom + self.full_h * 0.80),
                           spot_size)  # middle bottom
            pg.draw.circle(self.MWO.display, spot_col, (midpoint + self.board_x, top + self.full_h * 0.80),
                           spot_size)  # middle top

    def draw_instructions(self):
        """
        Draw all the text inside the text box
        """
        text_offset = 10
        text_color = (255, 110, 0)
        text1 = "Welcome to a Game of Escape the Fire."
        text2 = "The first player to reach the last square Wins, to their risks and perils."
        text3 = "May the roll of the dice decide your fate"

        self.MWO.draw_textwrapped(self.text_box_x + text_offset, self.text_box_y + text_offset,
                                  self.TB_size_w - text_offset, self.GB_size_h - text_offset,
                                  text1, self.text_size, text_color)

        self.MWO.draw_textwrapped(self.text_box_x + text_offset,
                                  self.text_box_y + (self.GB_size_h * (1 / 4)) + text_offset,
                                  self.TB_size_w - text_offset, self.GB_size_h - text_offset,
                                  text2, self.text_size, text_color)

        self.MWO.draw_textwrapped(self.text_box_x + text_offset,
                                  self.text_box_y + (self.GB_size_h * (2 / 4)) + text_offset,
                                  self.TB_size_w - text_offset, self.GB_size_h - text_offset,
                                  text3, self.text_size, text_color)

    def check_input(self):
        """
        Check the user input and carry out the appropriate selection
        on the UI
        """
        # CAUTION:
        # self.game_State (Uppercase S) refers to the map items of escape the fire
        # self.game_state refers to something idk about in the super class
        self.move_cursor()

        # user selects input with enter
        if self.MWO.ENTER_KEY:

            if self.window_state == "Exit":
                self.exit_action()
            elif self.window_state == "ROLL":
                # play the player who selected ROLL
                self.roll_action()

        if self.MWO.LEFT_CLICK:
            if self.exit_x < self.MWO.mx < self.exit_x + self.SB_size_w and self.exit_y < self.MWO.my < self.exit_y + self.SB_size_h:
                self.exit_action()

            elif self.roll_x < self.MWO.mx < self.roll_x + self.SB_size_w and self.roll_y < self.MWO.my < self.roll_y + self.SB_size_h:
                self.roll_action()

    def exit_action(self):
        """
        closes the game and saves to the database
        :return: None
        """
        self.is_displaying = False
        self.MWO.playing = False
        self.save_to_db()
        self.save_stats()
        self.db.close_connection()
        self.MWO.current_screen = self.MWO.main_menu

    def roll_action(self):
        """
        starts the current players turn
        :return:None
        """
        # play the player who selected ROLL
        self.play_game()
        self.game_State.switch_player()
        self.display_info()
        # AI's play moves,
        if self.AI_playing:
            for player in range(self.nPlayers - 1):
                # update piece GUI objects, quick short cut.
                self.draw_background()
                self.draw_cursor()
                self.draw_buttons()
                self.draw_pieces()
                self.draw_grid(self.N_ROWS, self.N_COLS, self.GB_size_w / self.N_COLS,
                               self.GB_size_h / self.N_ROWS,
                               self.GB_size_w, self.GB_size_h, self.board_x, self.board_y)
                self.display_info()
                self.draw_instructions()
                self.draw_die(self.roll_die)
                self.blit_game()

                time.sleep(0.35)
                self.play_game()
                self.game_State.switch_player()


    def move_cursor(self):
        """
        It defines the cursor controlled with the arrow keys, allows UI elements
        """
        # Left key
        if self.MWO.LEFT_KEY:
            if self.window_state == "Exit":
                self.cursor_pos_x = self.roll_x + self.cursor_offset_x
                self.cursor_pos_y = self.roll_y + self.cursor_offset_y
                self.cursor_size_x = self.SB_size_w - (2 * self.cursor_offset_x)
                self.cursor_size_y = self.SB_size_h - (2 * self.cursor_offset_y)
                self.window_state = "ROLL"

        # Right key
        elif self.MWO.RIGHT_KEY:

            if self.window_state == "ROLL":
                self.cursor_pos_x = self.exit_x + self.cursor_offset_x
                self.cursor_pos_y = self.exit_y + self.cursor_offset_y
                self.cursor_size_x = self.SB_size_w - (2 * self.cursor_offset_x)
                self.cursor_size_y = self.SB_size_h - (2 * self.cursor_offset_y)
                self.window_state = "Exit"

        elif self.exit_x < self.MWO.mx < self.exit_x + self.SB_size_w and self.exit_y < self.MWO.my < self.exit_y + self.SB_size_h:
                self.cursor_pos_x = self.exit_x + self.cursor_offset_x
                self.cursor_pos_y = self.exit_y + self.cursor_offset_y
                self.cursor_size_x = self.SB_size_w - (2 * self.cursor_offset_x)
                self.cursor_size_y = self.SB_size_h - (2 * self.cursor_offset_y)
                self.state = "Exit"
        elif self.roll_x < self.MWO.mx < self.roll_x + self.SB_size_w and self.roll_y < self.MWO.my < self.roll_y + self.SB_size_h:
            self.cursor_pos_x = self.roll_x + self.cursor_offset_x
            self.cursor_pos_y = self.roll_y + self.cursor_offset_y
            self.cursor_size_x = self.SB_size_w - (2 * self.cursor_offset_x)
            self.cursor_size_y = self.SB_size_h - (2 * self.cursor_offset_y)
            self.state = "ROLL"

    def score_move(self, player, roll, curr, dest):
        """
        Score the current move.
        :param player: A Integer representing A player ID
        :param roll: A Integer representing A The number roll from the dice
        :param curr: A Integer representing the players current position
        :param dest: A Integer representing The players final position
        :return: None
        """
        if player == -1:
            if dest >= curr:
                self.score += roll * dest
            else:
                self.score -= (roll * 10) * curr

    def play_game(self):
        """
        Control for Escape the Fire game
        plays 1 turn
        """
        self.MWO.play_sound("Assets/move2.mp3")
        roll = dice.roll_dice()
        self.roll_die = roll
        current_player = self.game_State.get_current_player_int()
        curr = self.game_State.get_current_player().get_curr_pos()
        dest = curr + roll
        self.score_move(current_player, roll, curr, dest)
        end = self.game_State.validate_update_move(curr, dest, current_player)
        self.curr = curr

        if dest == end:
            self.dest = dest
        else:
            self.dest = end

        if end - curr > 6:
            self.MWO.play_sound("Assets/ladder.mp3")
        elif end - curr < 0:
            self.MWO.play_sound("Assets/Bone Crack.mp3")
        self.game_State.update_player(end)

        # score the move
        self.score_move(current_player, roll, curr, end)
        if self.game_State.win_condition(end):
            self.MWO.play_sound("Assets/Cartoon Win Sound Effect.mp3")
            self.winner = current_player
            if self.winner == -1:
                self.score *= 2
            self.is_displaying = False
            self.MWO.playing = False
            self.save_stats()
            self.db.close_connection()
            self.MWO.current_screen = HiscoreScreen(self.MWO, self.score, "etf")

