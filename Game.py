import pygame as pg
import copy


class Game:
    def __init__(self, window):
        """
        Game superclass; constructor
        :param window: a Window() object
        """
        # set the Widow object ("MWO = Main Window Object")
        self.MWO = window

        # initialize display flags
        self.is_displaying = False
        self.is_replaying = False

        # initialize player and AI flags
        self.player1_turn = True
        self.AI_playing = True
        self.undos_left = 3

        # initialize game state list and legal move dictionary
        self.legal_move_dict = {}
        self.game_state_list = []
        self.GSL_ptr = 0

        # set up general cords
        self.full_w, self.full_h = self.MWO.DISPLAY_W, self.MWO.DISPLAY_H
        self.half_w, self.half_h = self.MWO.DISPLAY_W / 2, self.MWO.DISPLAY_H / 2
        self.quarter_w, self.quarter_h = self.MWO.DISPLAY_W / 4, self.MWO.DISPLAY_H / 4
        self.sixteenth_w, self.sixteenth_h = self.MWO.DISPLAY_W / 16, self.MWO.DISPLAY_H / 16
        self.thirtytwo_w, self.thirtytwo_h = self.MWO.DISPLAY_W / 32, self.MWO.DISPLAY_H / 32



    def save_to_db(self):
       """
       ABSTRACT CLASS
       """
       pass

    def load_from_db(self):
        """
        ABSTRACT CLASS
        """
        pass

    def change_ai(self, bool):
        """
        Sets the AI to a given boolean
        :return: None
        """
        self.AI_playing = bool

    def add_state(self, state):
        """
        deep copy the state to the game state list.
        :param state: a Data type that represents a game's current state.
        :return: None
        """
        self.game_state_list.append(copy.deepcopy(state))
        # update pointer size and location
        self.GSL_ptr = len(self.game_state_list) - 1

    def undo_move(self):
        """
        ABSTRACT FUNCTION
        """
        pass

    def prev_move(self):
        """
        decrements the game state list pointer (GSL_ptr) -1, and returns
        the state at game_state_list[GSL_ptr].

        If the pointer is At the start of the list, return -1
        :return: A game_state object
        """
        if self.GSL_ptr > 0:
            self.is_replaying = True
            self.GSL_ptr -= 1
            return copy.deepcopy(self.game_state_list[self.GSL_ptr])
        else:
            return -1

    def next_move(self):
        """
        increments the game state list pointer (GSL_ptr) +1, and returns
        the state at game_state_list[GSL_ptr].
        If the pointer is At the end of the list, return the most recent move and turn off "replay mode"
        If something went wrong return -1 (for now)
        :return: A game_state object
        """
        if self.GSL_ptr < len(self.game_state_list) - 1:
            self.is_replaying = True
            self.GSL_ptr += 1
            if self.GSL_ptr == len(self.game_state_list) - 1:
                self.is_replaying = False
            return copy.deepcopy(self.game_state_list[self.GSL_ptr])

        else:
            return -1

    def clear_move_dict(self):
        """
        clears the move dictionary.
        :return: None
        """
        self.legal_move_dict = {}

    def blit_game(self):
        """
        displays the drawn objects and then resets flags.
        :return: None
        """
        # (0, 0) is the top left of the screen
        self.MWO.window.blit(self.MWO.display, (0, 0))
        pg.display.update()
        self.MWO.reset_key_inputs()
