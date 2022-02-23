import random as r
import time as t
import copy

class Ai:
    """
    Given a game IE. connectFour
    """
    def __init__(self, game):
        self.cur_game = game

    def random_search(self, move_dict):
        """
        Easy Difficulty
        pick a random index in the move list
        :param move_dict: a dictionary of all legal moves
        :return: A Integer representing the move column
        """
        # sleep for 0.3 secs
        t.sleep(0.2)
        return r.randint(0, len(move_dict)-1)

    def minimax(self, depth=2):
        """
        runs minimax search up to depth, on a given initial state.
        :return: A Integer representing the best Column to play searching
        """
        # sleep 0.2 secs
        t.sleep(0.2)
        # copy this copy that screw pass by reference
        state_copy = copy.deepcopy(self.cur_game.game_state)

        move = self.minimax_helper(self.cur_game.PLAYER_TWO_PIECE, state_copy, depth)
        return move[0]

    def minimax_helper(self, turn, initial_state, depth):
        """
        Minimax recursive helper used to bottom-up evalutate states given a depth limit.
        :param turn: A Integer represent whos turn it is. (1 = player 1)(2 = player 2)
        :param initial_state: A 2D array of Integers representing a Connect Four Game state.
        :param depth: A Integer which represents the depth limit.
        :return: A Integer which represents the current players best evaluation from its children (branch case)
                 Or The evaluation of its state to pass forward (leaf case)
        """
        # column is key; evaluation result is the value
        results = {}

        # create a state_copy
        state_copy = copy.deepcopy(initial_state)

        # save the state and gen moves()
        self.cur_game.game_state = state_copy
        self.cur_game.generate_legal_moves()

        # save the legal move dict
        move_dict_copy = copy.deepcopy(self.cur_game.legal_move_dict)

        if depth == 0:
            # evaluate the state in terms of the AI player,
            return [0, self.heuristic_evaluation_CF(self.cur_game.game_state, self.cur_game.PLAYER_TWO_PIECE)]

        elif depth > 0:
            # loop through all legal moves
            for move in move_dict_copy:

                # set it to Ai's turn
                if turn == self.cur_game.PLAYER_ONE_PIECE:
                    self.cur_game.player1_turn = True
                else:
                    self.cur_game.player1_turn = False

                # switch back to the state_copy
                self.cur_game.legal_move_dict = copy.deepcopy(move_dict_copy)
                self.cur_game.game_state = copy.deepcopy(state_copy)

                # apply the move to the state_cop
                self.cur_game.set_move(move)

                # if its players 1's turn swap to player 2's
                if turn == self.cur_game.PLAYER_ONE_PIECE:
                    eval_list = self.minimax_helper(self.cur_game.PLAYER_TWO_PIECE, self.cur_game.game_state, depth - 1)
                    eval_list[0] = move
                    results[move] = eval_list
                else:
                    eval_list = self.minimax_helper(self.cur_game.PLAYER_ONE_PIECE, self.cur_game.game_state, depth-1)
                    eval_list[0] = move
                    results[move] = eval_list

        # return this players best pick, (highest = P2; lowest = P1,).
        if turn == self.cur_game.PLAYER_TWO_PIECE:
            current_best = [0, float("-inf")]
            for this in results.values():
                if this[1] > current_best[1]:
                    current_best = this
            return current_best
        else:
            current_worst = [0, float("inf")]
            for this in results.values():
                if this[1] < current_worst[1]:
                    current_worst = this
            return current_worst


    def heuristic_helper(self, piece, slot1, slot2, slot3, slot4):
        """
        checks if the given four slots form a connected line segment
        :param piece: A Integer represent what piece to check
        :param slot1: a Integer that can be any piece or a empty space
        :param slot2: a Integer that can be any piece or a empty space
        :param slot3: a Integer that can be any piece or a empty space
        :param slot4: a Integer that can be any piece or a empty space
        :return: A Integer representing the multiplication factor of a line segment
        """
        my_p = piece
        open_slot = 0

        # check if ANY 4 in a row
        if slot1 == my_p and slot2 == my_p and slot3 == my_p and slot4 == my_p:
            return 1000

        # check if ANY 3 in a row last open
        elif slot1 == my_p and slot2 == my_p and slot3 == my_p and slot4 == open_slot:
            #print("FOUND three IN A ROW")
            return 9
        elif slot1 == open_slot and slot2 == my_p and slot3 == my_p and slot4 == my_p:
            #print("FOUND three IN A ROW")
            return 9
        elif slot1 == my_p and slot2 == open_slot and slot3 == my_p and slot4 == my_p:
            #print("FOUND three IN A ROW")
            return 9
        elif slot1 == my_p and slot2 == my_p and slot3 == open_slot and slot4 == my_p:
            #print("FOUND three IN A ROW")
            return 9

        # check if ANY 2 in a row last open
        elif slot1 == my_p and slot2 == my_p and slot3 == open_slot and slot4 == open_slot:
            #print("FOUND two IN A ROW")
            return 3
        elif slot1 == open_slot and slot2 == my_p and slot3 == my_p and slot4 == open_slot:
            #print("FOUND two IN A ROW")
            return 3
        elif slot1 == open_slot and slot2 == open_slot and slot3 == my_p and slot4 == my_p:
            #print("FOUND two IN A ROW")
            return 3

        # no good line segments so return 1
        return 1


    def heuristic_evaluation_CF(self, state, piece):
        """
        Checks all 4-length line combination and calculates a value
        :param piece: a Integer representing which player's turn it is
        :param state: A 2D array of integers representing a CF board
        :return: A Integer representing the value calculated from the given state
        """
        # get local variables
        b = copy.deepcopy(state)
        num_rows = self.cur_game.ROW_SIZE
        num_cols = self.cur_game.COL_SIZE

        # get the current players piece
        my_p = piece
        if my_p == self.cur_game.PLAYER_TWO_PIECE:
            foe_p = self.cur_game.PLAYER_ONE_PIECE
        else:
            foe_p = self.cur_game.PLAYER_TWO_PIECE

        # evaluate both players positional value
        my_value = 1
        foe_value = 1

        # check horizontal lines.
        for col in range(num_cols - 3):
            for row in range(num_rows):
                # get the values from the horizontal line
                slot1, slot2, slot3, slot4 = b[row][col], b[row][col + 1], b[row][col + 2], b[row][col + 3]
                # run the heuristic for both players
                my_value *= self.heuristic_helper(my_p, slot1, slot2, slot3, slot4)
                foe_value *= self.heuristic_helper(foe_p, slot1, slot2, slot3, slot4)

        # check vertical lines
        for col in range(num_cols):
            for row in range(num_rows - 3):
                # get the values from the vertical line
                slot1, slot2, slot3, slot4 = b[row][col], b[row+1][col], b[row+2][col], b[row+3][col]
                # run the heuristic for both players
                my_value *= self.heuristic_helper(my_p, slot1, slot2, slot3, slot4)
                foe_value *= self.heuristic_helper(foe_p, slot1, slot2, slot3, slot4)

        # check Downward diagonal lines
        for col in range(num_cols - 3):
            for row in range(num_rows - 3):
                # get the values from the Downward diagonal line
                slot1, slot2, slot3, slot4 = b[row][col], b[row + 1][col + 1], b[row + 2][col + 2], b[row + 3][col + 3]
                # run the heuristic for both players
                my_value *= self.heuristic_helper(my_p, slot1, slot2, slot3, slot4)
                foe_value *= self.heuristic_helper(foe_p, slot1, slot2, slot3, slot4)

        # check upward diagonal lines
        for col in range(num_cols - 3):
            for row in range(3, num_rows):
                # get the values from the upward diagonal line
                slot1, slot2, slot3, slot4 = b[row][col], b[row - 1][col + 1], b[row - 2][col + 2], b[row - 3][col + 3]
                # run the heuristic for both players
                my_value *= self.heuristic_helper(my_p, slot1, slot2, slot3, slot4)
                foe_value *= self.heuristic_helper(foe_p, slot1, slot2, slot3, slot4)

        #print("\nplayer turn: ",piece,"\nMy value :", my_value, "\nfoes value: ", foe_value)
        #print("final eval : ", my_value - foe_value)
        #for each in self.cur_game.game_state: print(each)
        return my_value - foe_value
