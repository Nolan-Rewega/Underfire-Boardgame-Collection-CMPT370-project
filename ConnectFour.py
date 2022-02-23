import pygame as pg
import copy
from Ai import Ai
from Game import Game
from HiscoreScreen import HiscoreScreen
from Database import Database


class ConnectFour(Game):

    def __init__(self, window):
        # calling superclass constructor
        Game.__init__(self, window)

        # initialize database
        self.db = Database()

        # initialize the initial game state
        self.ROW_SIZE = 6
        self.COL_SIZE = 7
        self.PLAYER_ONE_PIECE = 1
        self.PLAYER_TWO_PIECE = 2

        self.DEFAULT_VAL = 0
        self.game_state = [[self.DEFAULT_VAL for col in range(self.COL_SIZE)] for row in range(self.ROW_SIZE)]
        self.add_state(self.game_state)
        self.draw = False
        self.winner = False

        # initialize statistic variables.
        self.pieces_play = 0
        self.stats_three_line = 0

        # Scores
        self.score_player1 = 0
        self.score_player2 = 0

        # initial state set on Game 1 (Connect Four)
        self.window_state = "Exit"

        # text size
        self.text_size = round(self.full_w // 60)

        # button offsets
        self.SB_offset = 50
        self.GB_offset = 50

        # box sizes (GB = game box) (SB = utility box's) (TB = text box)
        self.GB_size_w = self.full_w * (3/5)
        self.TB_size_w = self.quarter_w * (9/10)
        self.GB_size_h = self.full_h * (2/3)
        self.SB_size_w = self.quarter_w / 4
        self.SB_size_h = self.SB_size_w

        # cords of game rect's
        self.board_x, self.board_y = self.sixteenth_w, self.quarter_h / 2
        self.text_box_x, self.text_box_y = (self.board_x + self.GB_size_w + self.GB_offset), self.quarter_h / 2

        # cords of utility buttons
        self.exit_x, self.exit_y = (self.full_w / 1.15), self.full_h / 1.2
        self.undo_x, self.undo_y = (self.exit_x - self.SB_size_w - self.SB_offset), self.full_h / 1.2

        self.prev_x, self.prev_y = (self.board_x - self.SB_size_w + (self.GB_size_w * (1/3))), self.full_h / 1.2
        self.next_x, self.next_y = (self.board_x + (self.GB_size_w * (2/3))), self.full_h / 1.2

        # cursor offsets
        self.cursor_offset_x = -5
        self.cursor_offset_y = -5

        # cursor initial size
        self.cursor_size_x = self.SB_size_w - (2 * self.cursor_offset_x)
        self.cursor_size_y = self.SB_size_h - (2 * self.cursor_offset_y)

        # cursor initial position
        self.cursor_pos_x = self.exit_x + self.cursor_offset_x
        self.cursor_pos_y = self.exit_y + self.cursor_offset_y

    def load_from_db(self):
        """
        load save state from Database, and reconstruct it into a 2D array
        :return: None
        """
        # read the data from the database
        read_data = self.db.get_game_state("c4")
        # read in the data
        if read_data is not None:
            self.game_state = read_data[:-4]
            self.game_state_list = read_data[-3]
            self.score_player2 = read_data[-2]
            self.score_player1 = read_data[-1]

            self.undos_left = read_data[-4][0]
            self.GSL_ptr = read_data[-4][1]
            self.is_replaying = read_data[-4][2]

    def save_to_db(self):
        """
        Saves a given 2D array into the data base.
        :return:None
        """
        # deep copy important stuff
        save = copy.deepcopy(self.game_state)
        # saving externals
        undo_tuple = (self.undos_left, self.GSL_ptr, self.is_replaying)
        move_list = copy.deepcopy(self.game_state_list)
        save_score_p1 = copy.deepcopy(self.score_player1)
        save_score_p2 = copy.deepcopy(self.score_player2)

        save.append(undo_tuple)
        save.append(move_list)
        save.append(save_score_p2)
        save.append(save_score_p1)

        self.db.save_game_state("c4", save)

    def save_stats(self):
        """
        Saves the user Stats to the database
        :return: None
        """
        stats = self.db.get_stats()
        stats["pieces_placed"] = self.pieces_play
        stats["almost_wins"] = self.stats_three_line
        stats["score"] = self.score_player1

        outcome = 0
        if self.player1_turn:
            outcome = 1
        self.db.update_stats('c4', outcome, stats)


    def swap_turns(self):
        """
        swaps the players turn;
        If player 1 just played its now player 2's turn and visa versa
        :return: None
        """
        if self.player1_turn:
            self.player1_turn = False
        else:
            self.player1_turn = True


    # may have to change depending on AI
    def generate_legal_moves(self):
        """
        stores the "lowest" empty row position for each column in a dictionary where
        the column index is the key.

        If the column is full that column isn't added to the dictionary
        :return: None
        """
        # search column left to right
        for row in range(self.ROW_SIZE):
            for col in range(self.COL_SIZE):
                # lowest empty col overrides the previous one for that column
                # so the lowest one is always
                if self.game_state[row][col] == 0:
                    self.legal_move_dict[col] = row


    def verify_move(self, col):
        """
        Given a column number check to see if that column is in the legal move dict.

        :param col: a Integer representing a column index
        :return: a Boolean, True if that column has a empty spot, False otherwise
        """
        # if the column is full, col will be a key.
        return col in self.legal_move_dict


    # this is dumb but I couldn't think of a smarter way
    def end_condition(self, p):
        """
        checks in all directions if the current player has four in a row.
        :P: A player indicator, 2 for P2, 1 for P1
        :return: Boolean
        """
        # copy game state for safety
        b = self.game_state
        zeros = 42

        # check if draw
        for col in range(self.COL_SIZE):
            for row in range(self.ROW_SIZE):
                if b[row][col] != 0:
                    zeros -= 1

        # check if draw
        if zeros == 0:
            self.draw = True
            return True

        # check horizontally.
        for col in range(self.COL_SIZE - 3):
            for row in range(self.ROW_SIZE):
                if b[row][col] == p and b[row][col+1] == p and b[row][col+2] == p and b[row][col+3] == p:
                    return True

        # check vertically
        for col in range(self.COL_SIZE):
            for row in range(self.ROW_SIZE-3):
                if b[row][col] == p and b[row+1][col] == p and b[row+2][col] == p and b[row+3][col] == p:
                    return True

        # check Downward diagonal
        for col in range(self.COL_SIZE - 3):
            for row in range(self.ROW_SIZE - 3):
                if b[row][col] == p and b[row+1][col+1] == p and b[row+2][col+2] == p and b[row+3][col+3] == p:
                    return True

        # check upward diagonal
        for col in range(self.COL_SIZE - 3):
            for row in range(3, self.ROW_SIZE):
                if b[row][col] == p and b[row-1][col+1] == p and b[row-2][col+2] == p and b[row-3][col+3] == p:
                    return True
        return False

    def undo_move(self):
        """
        Undoes the last two moves
        :return: A state Object
        """
        # if not empty or not replaying then we can undo
        if not self.is_replaying and self.undos_left > 0:
            if len(self.game_state_list) > 2:
                # pop the last TWO items and return the new tail state
                self.game_state_list.pop()
                self.game_state_list.pop()
                # update pointer size and location
                self.GSL_ptr = len(self.game_state_list) - 2

            elif len(self.game_state_list) == 2:
                self.game_state_list.pop()
                self.GSL_ptr = len(self.game_state_list) - 1

            self.undos_left -= 1

            # update players turn for connect four no update is needed,
            return copy.deepcopy(self.game_state_list[-1])
        else:
            return -1

    def set_move(self, col):
        """
        given a valid column index, retrieve the legal move and set its
        row,col position to the current player's piece.
        :param col: a Integer representing a column index
        :return: None
        """
        row = self.legal_move_dict[col]
        if self.player1_turn:
            self.game_state[row][col] = self.PLAYER_ONE_PIECE
        else:
            self.game_state[row][col] = self.PLAYER_TWO_PIECE

    # first point of contact if AI class needs to modify change to deep copy's
    def ai_move(self):
        """
        A Ai picks a move then we play it
        :return: None
        """
        # create a new game
        game_copy = ConnectFour(self.MWO)
        # copy game state and gen moves
        state_copy = copy.deepcopy(self.game_state)
        game_copy.game_state = state_copy
        game_copy.generate_legal_moves()

        ai_search = Ai(game_copy)
        # normal
        if self.MWO.difficulty == "Normal":
            # send in the dictionary
            depth = 1
            move = ai_search.minimax(depth)
        # hard
        elif self.MWO.difficulty == "Hard":
            depth = 2
            move = ai_search.minimax(depth)
        # Easy
        else:
            move = ai_search.random_search(game_copy.legal_move_dict)

        # now that the AI has selected a move, play it
        self.play_move(move, self.PLAYER_TWO_PIECE)


    def play_move(self, col, player):
        """
        carryout a players move if it is legal.
        :param col: a Integer representing the chosen column
        :param player: a Integer representing a player
        :return: None
        """
        self.generate_legal_moves()

        if self.verify_move(col) and not self.is_replaying:
            # update pieces play
            if self.player1_turn:
                self.pieces_play += 1
            # set the move on the board
            self.set_move(col)
            # add state to the state list
            self.MWO.play_sound("Assets/move2.mp3")
            self.add_state(copy.deepcopy(self.game_state))
            # score move
            self.score_move()
            # check if game is won
            if self.end_condition(player):
                self.save_stats()
                self.winner = True
                self.is_displaying = False
                self.MWO.playing = False
                self.db.close_connection()
                # always set player 1's score
                self.MWO.current_screen = HiscoreScreen(self.MWO, self.score_player1, 'c4')
            else:
                # swap player turns
                self.swap_turns()
            # clear the move dictionary
            self.clear_move_dict()

    def score_move(self):
        """
        Score each move based on the number of pieces on the board
        :return: None
        """
        # +10 for every piece placed
        # 2 in a row + 100
        # 3 in a row + 1000
        # 4 in a row * 2

        # calculate player 1's score
        if self.player1_turn:
            self.score_player1 = self.score_loop(self.PLAYER_ONE_PIECE, self.score_player1)
            self.score_player1 += 10
            if self.winner:
                self.score_player1 *= 2

        # calculate player 2's score
        else:
            self.score_player2 = self.score_loop(self.PLAYER_TWO_PIECE, self.score_player2)
            self.score_player2 += 10
            if self.winner:
                self.score_player2 *= 2

    def score_loop(self, piece, score):
        """
        loop through all tiles to calculate the score
        :param score: A integer represent the given score
        :param piece: A integer represent the player piece
        :return: A Integer that represents the Total calculated score
        """
        b = self.game_state
        total = score

        # check horizontally.
        for col in range(self.COL_SIZE - 3):
            for row in range(self.ROW_SIZE):
                slot1, slot2, slot3, slot4 = b[row][col], b[row][col + 1], b[row][col + 2], b[row][col + 3]
                total += self.score_helper(piece, slot1, slot2, slot3, slot4)

        # check vertically
        for col in range(self.COL_SIZE):
            for row in range(self.ROW_SIZE - 3):
                slot1, slot2, slot3, slot4 = b[row][col], b[row + 1][col], b[row + 2][col], b[row + 3][col]
                total += self.score_helper(piece, slot1, slot2, slot3, slot4)

        # check Downward diagonal
        for col in range(self.COL_SIZE - 3):
            for row in range(self.ROW_SIZE - 3):
                slot1, slot2, slot3, slot4 = b[row][col], b[row + 1][col + 1], b[row + 2][col + 2], b[row + 3][col + 3]
                total += self.score_helper(piece, slot1, slot2, slot3, slot4)

        # check upward diagonal
        for col in range(self.COL_SIZE - 3):
            for row in range(3, self.ROW_SIZE):
                slot1, slot2, slot3, slot4 = b[row][col], b[row - 1][col + 1], b[row - 2][col + 2], b[row - 3][col + 3]
                total += self.score_helper(piece, slot1, slot2, slot3, slot4)
        return total

    def score_helper(self, piece, slot1, slot2, slot3, slot4):
        """
        Calculate the value of the given Four-line
        :param piece: A Integer representing the player's Piece
        :param slot1: A Integer representing the First Piece in the sequence
        :param slot2: A Integer representing the Second Piece in the sequence
        :param slot3: A Integer representing the Third Piece in the sequence
        :param slot4: A Integer representing the Fourth Piece in the sequence
        :return: The Largest Line segment value
        """
        open_slot = 0

        # check if ANY 3 in a row last open
        if slot1 == piece and slot2 == piece and slot3 == piece:
            if self.player1_turn:
                self.stats_three_line += 1
            return 1000
        elif slot2 == piece and slot3 == piece and slot4 == piece:
            if self.player1_turn:
                self.stats_three_line += 1
            return 1000

        # check if ANY 2 in a row last open
        elif slot1 == piece and slot2 == piece:
            return 100
        elif slot2 == piece and slot3 == piece:
            return 100
        elif slot3 == piece and slot4 == piece:
            return 100

        # no good line segments so return 1
        return 0

    def play(self):
        """
        main loop; runs the game.
        :return: none
        """
        # start game loop then launch the game
        self.is_displaying = True

        while self.is_displaying:
            # check user input
            if self.AI_playing and not self.player1_turn and self.window_state != "End":
                self.ai_move()
            else:
                self.MWO.set_user_input()
                self.check_input()

            # draw board unless there is a winner
            self.draw_board()
            # blit the board
            self.blit_game()

    def draw_score(self):
        """
        Draw the score on screen
        :return: None
        """
        score = "Score: " + str(self.score_player1)
        self.MWO.draw_text(score, self.text_size, self.board_x + (self.GB_size_w * (1 / 6)), self.board_y - 20, (110, 40, 110))

    def draw_board(self):
        """
        Draws the normal board and main screen
        :return: None
        """
        # draw background
        self.MWO.display.fill((225, 129, 38))
        self.MWO.draw_image("Assets/Bubbles.jpg", self.thirtytwo_w, self.thirtytwo_h,
                            round(self.full_w - 2 * self.thirtytwo_w),
                            round(self.full_h - 2 * self.thirtytwo_h))
        self.MWO.draw_rect((240,240,240), self.board_x, self.board_y, self.GB_size_w,self.GB_size_h)
        self.MWO.draw_text("Connect Four", self.text_size, self.full_w / 2, self.full_h / 16)

        # draw cursor replace method
        self.draw_cursor()

        # draw rectangles and text box
        self.MWO.draw_rect((20, 35, 50), self.text_box_x, self.text_box_y, self.TB_size_w, self.GB_size_h)
        self.MWO.draw_text("Instructions", self.text_size, self.text_box_x + self.TB_size_w / 2, self.sixteenth_h)

        # draw utility box's
        self.MWO.draw_image('Assets/undo.png', self.undo_x, self.undo_y, round(self.SB_size_w), round(self.SB_size_h))
        self.MWO.draw_image('Assets/exit.png', self.exit_x, self.exit_y, round(self.SB_size_w), round(self.SB_size_h))
        self.MWO.draw_text("Undo", self.text_size, self.undo_x + self.SB_size_w/2, self.undo_y)
        self.MWO.draw_text("Exit", self.text_size, self.exit_x + self.SB_size_w/2, self.exit_y)

        self.MWO.draw_image('Assets/next.png', self.next_x, self.next_y, round(self.SB_size_w), round(self.SB_size_h))
        self.MWO.draw_image('Assets/prev.png', self.prev_x, self.prev_y, round(self.SB_size_w), round(self.SB_size_h))
        self.MWO.draw_text("Next", self.text_size, self.next_x + self.SB_size_w/2, self.next_y)
        self.MWO.draw_text("Prev", self.text_size, self.prev_x + self.SB_size_w/2, self.prev_y)

        # draw instructions
        self.draw_instructions()
        # draw turn indicator
        self.draw_turn_indicator()
        # draw Score
        self.draw_score()
        # draw player pieces on the board
        self.draw_pieces()
        # draw board texture
        self.MWO.draw_image("Assets/CFboard.png", self.board_x, self.board_y, round(self.GB_size_w),
                            round(self.GB_size_h))
        # draw grid
        self.draw_grid(6, 7, self.GB_size_w / 7, self.GB_size_h / 6, self.GB_size_w, self.GB_size_h, self.board_x, self.board_y)

    def draw_cursor(self):
        """
        draws the cursor as a rectangle using Window's draw_rect
        :return: None
        """
        self.MWO.draw_rect((255, 100, 100),self.cursor_pos_x, self.cursor_pos_y, self.cursor_size_x, self.cursor_size_y)

    def draw_instructions(self):
        """
        Draws all instruction text on the screen.
        :return: None
        """
        text_offset = 10
        text_color = (200, 230, 230)

        text1 = "Select a column with the arrow keys and press ENTER to drop a piece. "
        text2 = "If you Connect Four YOU WIN! But, If your Opponent does so first, YOU LOSE!"
        text3 = "Good luck!"

        self.MWO.draw_textwrapped(self.text_box_x + text_offset, self.text_box_y + text_offset,
                                  self.TB_size_w - text_offset, self.GB_size_h - text_offset,
                                  text1, self.text_size, text_color)

        self.MWO.draw_textwrapped(self.text_box_x + text_offset, self.text_box_y + (self.GB_size_h * (1/4))+text_offset,
                                  self.TB_size_w - text_offset, self.GB_size_h - text_offset,
                                  text2, self.text_size, text_color)

        self.MWO.draw_textwrapped(self.text_box_x + text_offset, self.text_box_y + (self.GB_size_h * (3/4))+text_offset,
                                  self.TB_size_w - text_offset, self.GB_size_h - text_offset,
                                  text3, self.text_size, text_color)

    def draw_turn_indicator(self):
        """
        Draws a text box Indicating which player's turn it is.
        :return: None
        """
        if self.player1_turn:
            self.MWO.draw_text("Red's Turn", self.text_size,
                               self.board_x + (self.GB_size_w * (1/6)), self.sixteenth_h, (255, 0, 0))
        else:
            self.MWO.draw_text("Blue's Turn", self.text_size,
                               self.board_x + (self.GB_size_w * (1/6)), self.sixteenth_h, (0, 0, 255))

    def draw_pieces(self):
        """
        Draws the every piece on the board
        :return: None
        """
        # draw player pieces on the board
        size_x = self.GB_size_w / self.COL_SIZE
        size_y = self.GB_size_h / self.ROW_SIZE

        for r in range(self.ROW_SIZE):
            for c in range(self.COL_SIZE):
                # player 1's pieces
                if self.game_state[r][c] == 1:
                    self.MWO.draw_rect( (255, 0, 0),
                                        self.board_x + (size_x * c),
                                        self.board_y + (size_y * r), size_x, size_y)

                # player 2's pieces
                elif self.game_state[r][c] == 2:
                    self.MWO.draw_rect( (0, 0, 255),
                                        self.board_x + (size_x * c),
                                        self.board_y + (size_y * r), size_x, size_y)

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
            pg.draw.line(self.MWO.display, (200,200,200),
                         (start_x, start_y + offset_y*i),
                         (len_x+start_x, start_y + offset_y*i), 2)

        for j in range(1, num_lines_y):
            pg.draw.line(self.MWO.display, (200,200,200),
                         (offset_x*j + start_x, start_y),
                         (offset_x*j + start_x, len_y+start_y),2)

    def change_cursor_pos(self, cord_tuple, size_tuple):
        """
        Change the cursors current position and size.
        :param cord_tuple: A tuple of Integers which represent the new coordinates of the cursor
        :param size_tuple: A tuple of Integers which represent the new sizes of the cursor
        :return: None
        """
        cord_x, cord_y = cord_tuple[0], cord_tuple[1]
        size_w, size_h = size_tuple[0], size_tuple[1]

        self.cursor_pos_x = cord_x + self.cursor_offset_x
        self.cursor_pos_y = cord_y + self.cursor_offset_y
        self.cursor_size_x = size_w - (2 * self.cursor_offset_x)
        self.cursor_size_y = size_h - (2 * self.cursor_offset_y)

    def move_cursor(self):
        """
        change where the cursor is draw based on the current windows state
        :return: None
        """
        # Left key
        if self.MWO.LEFT_KEY:
            if self.window_state.isnumeric():
                # if col is bigger than 0
                if int(self.window_state) > 0:
                    # decrements the state
                    self.window_state = str(int(self.window_state) - 1)
                    self.cursor_pos_x = self.board_x + ((self.GB_size_w/7) * int(self.window_state))
                    self.cursor_pos_y = self.board_y + self.cursor_offset_y
                    self.cursor_size_x = self.GB_size_w / 7
                    self.cursor_size_y = self.cursor_size_y = self.GB_size_h / 32

            elif self.window_state == "Exit":
                self.change_cursor_pos((self.undo_x, self.undo_y), (self.SB_size_w, self.SB_size_h))
                self.window_state = "Undo"

            elif self.window_state == "Undo":
                self.change_cursor_pos((self.next_x, self.next_y), (self.SB_size_w, self.SB_size_h))
                self.window_state = "Next"

            elif self.window_state == "Next":
                self.change_cursor_pos((self.prev_x, self.prev_y), (self.SB_size_w, self.SB_size_h))
                self.window_state = "Prev"

        # Right key
        elif self.MWO.RIGHT_KEY:
            if self.window_state.isnumeric():
                # if col less than 6
                if int(self.window_state) < 6:
                    self.window_state = str(int(self.window_state) + 1)
                    self.cursor_pos_x = self.board_x + ((self.GB_size_w/7) * int(self.window_state))
                    self.cursor_pos_y = self.board_y + self.cursor_offset_y
                    self.cursor_size_x = self.GB_size_w / 7
                    self.cursor_size_y = self.GB_size_h / 32

            elif self.window_state == "Undo":
                self.change_cursor_pos((self.exit_x, self.exit_y), (self.SB_size_w, self.SB_size_h))
                self.window_state = "Exit"

            elif self.window_state == "Next":
                self.change_cursor_pos((self.undo_x, self.undo_y), (self.SB_size_w, self.SB_size_h))
                self.window_state = "Undo"

            elif self.window_state == "Prev":
                self.change_cursor_pos((self.next_x, self.next_y), (self.SB_size_w, self.SB_size_h))
                self.window_state = "Next"

        # down key
        elif self.MWO.DOWN_KEY:
            if self.window_state.isnumeric():
                self.change_cursor_pos((self.undo_x, self.undo_y), (self.SB_size_w, self.SB_size_h))
                self.window_state = "Undo"

        # up key
        elif self.MWO.UP_KEY:
            if not self.window_state.isnumeric():
                self.cursor_pos_x = self.board_x
                self.cursor_pos_y = self.board_y + self.cursor_offset_y
                self.cursor_size_x = self.GB_size_w / 7
                self.cursor_size_y = self.cursor_size_y = self.GB_size_h / 32
                self.window_state = "0"

        # mouse positions
        # over the board
        elif self.board_x < self.MWO.mx < self.board_x + self.GB_size_w and self.board_y < self.MWO.my < self.board_y + self.GB_size_h:
            local_x, local_y = self.MWO.mx, self.MWO.my
            col_lenth = (self.GB_size_w + 5) // self.COL_SIZE
            self.window_state = str(round((local_x - self.board_x) // col_lenth))

            self.cursor_pos_x = self.board_x + ((self.GB_size_w / 7) * int(self.window_state))
            self.cursor_pos_y = self.board_y + self.cursor_offset_y
            self.cursor_size_x = self.GB_size_w / 7
            self.cursor_size_y = self.cursor_size_y = self.GB_size_h / 32

        # over exit
        elif self.exit_x < self.MWO.mx < self.exit_x + self.SB_size_w and self.exit_y < self.MWO.my < self.exit_y + self.SB_size_h:
            self.change_cursor_pos((self.exit_x, self.exit_y), (self.SB_size_w, self.SB_size_h))
            self.state = "Exit"

        # over undo
        elif self.undo_x < self.MWO.mx < self.undo_x + self.SB_size_w and self.undo_y < self.MWO.my < self.undo_y + self.SB_size_h:
            self.change_cursor_pos((self.undo_x, self.undo_y), (self.SB_size_w, self.SB_size_h))
            self.state = "Undo"

        # over next
        elif self.next_x < self.MWO.mx < self.next_x + self.SB_size_w and self.next_y < self.MWO.my < self.next_y + self.SB_size_h:
            self.change_cursor_pos((self.next_x, self.next_y), (self.SB_size_w, self.SB_size_h))
            self.state = "Next"

        # over prev
        elif self.prev_x < self.MWO.mx < self.prev_x + self.SB_size_w and self.prev_y < self.MWO.my < self.prev_y + self.SB_size_h:
            self.change_cursor_pos((self.prev_x, self.prev_y), (self.SB_size_w, self.SB_size_h))
            self.state = "Prev"

    def check_input(self):
        """
        checks the user input and apply a action from the current state
        :return: None
        """
        # move the cursor
        self.move_cursor()

        # user selects input with enter
        if self.MWO.ENTER_KEY:

            if self.window_state == "Exit" or self.window_state == "End":
                self.is_displaying = False
                self.MWO.playing = False

                # save the game to the database then close the connection
                self.save_to_db()
                self.db.close_connection()

                self.MWO.current_screen = self.MWO.main_menu

            # undo the move and set it
            elif self.window_state == "Undo":
                undone_state = self.undo_move()
                if undone_state != -1:
                    self.game_state = undone_state

            # get the previous move
            elif self.window_state == "Prev":
                prev_state = self.prev_move()
                if prev_state != -1:
                    self.game_state = prev_state

            # get the next move.
            elif self.window_state == "Next":
                next_state = self.next_move()
                if next_state != -1:
                    self.game_state = next_state

            # operate on the user's selection
            elif self.window_state.isnumeric():
                # give the user selected column as input
                if self.player1_turn:
                    self.play_move(int(self.window_state), self.PLAYER_ONE_PIECE)
                else:
                    self.play_move(int(self.window_state), self.PLAYER_TWO_PIECE)

        # on left click input
        elif self.MWO.LEFT_CLICK:
            # exit
            if self.exit_x < self.MWO.mx < self.exit_x + self.SB_size_w and self.exit_y < self.MWO.my < self.exit_y + self.SB_size_h:
                self.is_displaying = False
                self.MWO.playing = False
                # save the game to the database then close the connection
                self.save_to_db()
                self.db.close_connection()
                self.MWO.current_screen = self.MWO.main_menu

            elif self.board_x < self.MWO.mx < self.board_x + self.GB_size_w and self.board_y < self.MWO.my < self.board_y + self.GB_size_h:
                # give the user selected column as input
                if self.player1_turn:
                    self.play_move(int(self.window_state), self.PLAYER_ONE_PIECE)
                else:
                    self.play_move(int(self.window_state), self.PLAYER_TWO_PIECE)

            # over undo
            elif self.undo_x < self.MWO.mx < self.undo_x + self.SB_size_w and self.undo_y < self.MWO.my < self.undo_y + self.SB_size_h:
                undone_state = self.undo_move()
                if undone_state != -1:
                    self.game_state = undone_state

            # over next
            elif self.next_x < self.MWO.mx < self.next_x + self.SB_size_w and self.next_y < self.MWO.my < self.next_y + self.SB_size_h:
                next_state = self.next_move()
                if next_state != -1:
                    self.game_state = next_state

            # over prev
            elif self.prev_x < self.MWO.mx < self.prev_x + self.SB_size_w and self.prev_y < self.MWO.my < self.prev_y + self.SB_size_h:
                prev_state = self.prev_move()
                if prev_state != -1:
                    self.game_state = prev_state

