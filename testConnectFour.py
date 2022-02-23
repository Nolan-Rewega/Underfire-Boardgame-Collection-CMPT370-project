from ConnectFour import *
from Window import *

w = Window()
CF = ConnectFour(w)


class TestConnectFour:
    """
    unit and integration test cases for the set_move, verify_move,
    end_condition, swap_turns, and Generate_legal_moves
    """
    def test_CF_set_move0(self):
        s1 = [[0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [1, 0, 0, 0, 0, 0, 0]]
        CF.game_state = s1
        CF.generate_legal_moves()
        CF.set_move(0)  # drop piece in first column
        result = CF.game_state
        assert result == s1, "CF_set_move0 -  "
        pass

    def test_CF_swap_turns0(self):
        CF.swap_turns()  # set swap turns
        result = False
        assert result == CF.player1_turn, "CF_swap_turns0 -  "
        pass

    def test_CF_set_move1(self):
        s2 = [[0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [1, 2, 0, 0, 0, 0, 0]]

        CF.game_state = s2
        CF.set_move(1)  # drop piece in Second column
        CF.generate_legal_moves()
        result = CF.game_state
        assert result == s2, "CF_set_move1 -  "
        pass

    def test_CF_swap_turns1(self):
        CF.swap_turns()  # set swap turns back
        result = True
        assert result == CF.player1_turn, "CF_swap_turns1-  "
        pass

    def test_CF_end_Condition0(self):
        s2 = [[0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 1, 0, 0, 0],
              [0, 0, 1, 2, 0, 0, 0],
              [0, 1, 2, 1, 0, 0, 0],
              [1, 2, 2, 2, 0, 0, 0]]

        CF.game_state = s2
        result = CF.end_condition(1)
        assert result is True, "CF_end_Condition0 -  "
        pass

    def test_CF_end_Condition1(self):
        s2 = [[0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 1, 0, 0, 0],
              [0, 0, 1, 2, 0, 0, 0],
              [0, 1, 2, 1, 0, 0, 0],
              [1, 2, 2, 2, 0, 0, 0]]

        CF.game_state = s2
        result = CF.end_condition(2)
        assert result is False, "CF_end_Condition1 -  "
        pass

    def test_CF_end_Condition2(self):
        s2 = [[0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 1, 2, 0, 0, 0],
              [0, 1, 2, 1, 0, 0, 0],
              [1, 2, 2, 2, 2, 0, 0]]

        CF.game_state = s2
        result = CF.end_condition(2)
        assert result is True, "CF_end_Condition2 -  "
        pass

    def test_CF_end_Condition3(self):
        s2 = [[0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [1, 0, 0, 0, 0, 0, 0],
              [1, 0, 0, 0, 0, 0, 0],
              [1, 0, 0, 0, 0, 0, 0],
              [1, 0, 0, 0, 0, 0, 0]]

        CF.game_state = s2
        result = CF.end_condition(1)
        assert result is True, "CF_end_Condition3 -  "
        pass

    def test_CF_generate_legal_moves0(self):
        CF2 = ConnectFour(w)
        s2 = [[1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1],
              [1, 1, 1, 1, 1, 1, 1]]

        CF2.game_state = s2
        CF2.generate_legal_moves()

        result = len(CF2.legal_move_dict)
        assert result == 0, "CF_generate_legal_moves0 -  "
        pass

    def test_CF_generate_legal_moves1(self):
        CF3 = ConnectFour(w)
        s2 = [[1, 0, 0, 0, 0, 0, 0],
              [1, 0, 0, 0, 0, 0, 0],
              [1, 0, 0, 0, 0, 0, 0],
              [1, 0, 0, 0, 0, 0, 0],
              [1, 0, 0, 0, 0, 0, 0],
              [1, 0, 0, 0, 0, 0, 0]]

        CF3.game_state = s2
        CF3.generate_legal_moves()

        result = len(CF3.legal_move_dict)
        assert result == 6, "CF_generate_legal_moves1 -  "
        pass

    def test_CF_generate_legal_moves2(self):
        s2 = [[0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0]]

        CF.game_state = s2
        CF.generate_legal_moves()

        result = len(CF.legal_move_dict)
        assert result == 7, "CF_generate_legal_moves2 -  "
        pass

    def test_CF_verify_move0(self):
        CF4 = ConnectFour(w)
        s2 = [[0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0]]

        CF4.game_state = s2
        CF4.generate_legal_moves()

        result = CF4.verify_move(0)
        assert result is True, "CF_verify_move0 -  "
        pass

    def test_CF_verify_move1(self):
        CF5 = ConnectFour(w)
        s2 = [[1, 0, 0, 0, 0, 0, 0],
              [1, 0, 0, 0, 0, 0, 0],
              [1, 0, 0, 0, 0, 0, 0],
              [1, 0, 0, 0, 0, 0, 0],
              [1, 0, 0, 0, 0, 0, 0],
              [1, 0, 0, 0, 0, 0, 0]]

        CF5.game_state = s2
        CF5.generate_legal_moves()

        result = CF5.verify_move(0)
        assert result is False, "CF_verify_move1 -  "
        pass

    def test_CF_move_cursor0(self):
        # manual manipulation
        CF.window_state = "Exit"
        w.LEFT_KEY = True
        CF.move_cursor()
        result = CF.window_state
        w.reset_key_inputs()
        assert result == "Undo", "CF_move_cursor0 -  "
        pass

    def test_CF_move_cursor1(self):
        # manual manipulation
        CF.window_state = "Undo"
        w.LEFT_KEY = True
        CF.move_cursor()
        result = CF.window_state
        w.reset_key_inputs()
        assert result == "Next", "CF_move_cursor1 -  "
        pass

    def test_CF_move_cursor2(self):
        # manual manipulation
        CF.window_state = "Next"
        w.LEFT_KEY = True
        CF.move_cursor()
        result = CF.window_state
        w.reset_key_inputs()
        assert result == "Prev", "CF_move_cursor2 -  "
        pass

    def test_CF_move_cursor3(self):
        # manual manipulation
        CF.window_state = "2"
        w.LEFT_KEY = True
        CF.move_cursor()
        result = CF.window_state
        w.reset_key_inputs()
        assert result == "1", "CF_move_cursor3 -  "
        pass

    def test_CF_move_cursor4(self):
        # manual manipulation
        CF.window_state = "Exit"
        w.UP_KEY = True
        CF.move_cursor()
        result = CF.window_state
        w.reset_key_inputs()
        assert result == "0", "CF_move_cursor4 -  "
        pass

    def test_CF_move_cursor5(self):
        # manual manipulation
        CF.window_state = "1"
        w.DOWN_KEY = True
        CF.move_cursor()
        result = CF.window_state
        w.reset_key_inputs()
        assert result == "Undo", "CF_move_cursor5 -  "
        pass

    def test_CF_move_cursor6(self):
        # manual manipulation
        CF.window_state = "Undo"
        w.RIGHT_KEY = True
        CF.move_cursor()
        result = CF.window_state
        w.reset_key_inputs()
        assert result == "Exit", "CF_move_cursor6 -  "
        pass

    def test_CF_move_cursor7(self):
        # manual manipulation
        CF.window_state = "Exit"
        w.RIGHT_KEY = True
        CF.move_cursor()
        result = CF.window_state
        w.reset_key_inputs()
        assert result == "Exit", "CF_move_cursor7 -  "
        pass

    def test_CF_check_input0(self):
        # manual manipulation
        CF.window_state = "Exit"
        CF.is_displaying = True
        w.ENTER_KEY = True
        CF.check_input()
        result = CF.is_displaying
        w.reset_key_inputs()
        assert result is False, "CF_check_input0 -  "
        pass
