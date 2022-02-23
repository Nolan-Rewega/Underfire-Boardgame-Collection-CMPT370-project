from ConnectFour import *
from Window import *
from DecisionScreen import DecisionScreen
w = Window()
MM = MainMenu(w)


class TestConnectFour:
    """
    unit and integration test cases for the set_move, verify_move,
    end_condition, swap_turns, and Generate_legal_moves
    """
    def test_CF_move_cursor0(self):
        # manual manipulation
        MM.state = "Exit"
        w.LEFT_KEY = True
        MM.move_cursor()
        result = MM.state
        w.reset_key_inputs()
        assert result == "Exit", "CF_move_cursor0 -  "
        pass

    def test_CF_move_cursor1(self):
        # manual manipulation
        MM.state = "Options"
        w.LEFT_KEY = True
        MM.move_cursor()
        result = MM.state
        w.reset_key_inputs()
        assert result == "Exit", "CF_move_cursor1 -  "
        pass

    def test_CF_move_cursor2(self):
        # manual manipulation
        MM.state = "ETF"
        w.LEFT_KEY = True
        MM.move_cursor()
        result = MM.state
        w.reset_key_inputs()
        assert result == "CF", "CF_move_cursor2 -  "
        pass

    def test_CF_move_cursor3(self):
        # manual manipulation
        MM.state = "Profile"
        w.LEFT_KEY = True
        MM.move_cursor()
        result = MM.state
        w.reset_key_inputs()
        assert result == "Options", "CF_move_cursor3 -  "
        pass

    def test_CF_move_cursor4(self):
        # manual manipulation
        MM.state = "Exit"
        w.UP_KEY = True
        MM.move_cursor()
        result = MM.state
        w.reset_key_inputs()
        assert result == "ETF", "CF_move_cursor4 -  "
        pass

    def test_CF_move_cursor5(self):
        # manual manipulation
        MM.state = "ETF"
        w.DOWN_KEY = True
        MM.move_cursor()
        result = MM.state
        w.reset_key_inputs()
        assert result == "Exit", "CF_move_cursor5 -  "
        pass


    def test_CF_check_input0(self):
        # manual manipulation
        MM.state = "Exit"
        MM.is_displaying = True
        w.ENTER_KEY = True
        MM.check_input()
        result = MM.is_displaying
        w.reset_key_inputs()
        assert result == False, "CF_check_input0 -  "
        pass

    def test_CF_check_input1(self):
        # manual manipulation
        MM.state = "CF"
        w.playing = False
        w.ENTER_KEY = True
        MM.check_input()
        result = w.current_screen
        w.reset_key_inputs()
        assert type(result) is DecisionScreen, "CF_check_input1 -  "
        pass

    def test_CF_check_input2(self):
        # manual manipulation
        MM.state = "Options"
        w.ENTER_KEY = True
        MM.check_input()
        result = w.current_screen
        w.reset_key_inputs()
        assert type(result) is OptionMenu, "CF_check_input2 -  "
        pass

    def test_CF_check_input3(self):
        # manual manipulation
        MM.state = "Profile"
        w.ENTER_KEY = True
        MM.check_input()
        result = w.current_screen
        w.reset_key_inputs()
        assert type(result) is Profile, "CF_check_input3 -  "
        pass

