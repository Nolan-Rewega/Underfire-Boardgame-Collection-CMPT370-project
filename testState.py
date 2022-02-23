from State import State

game = State()


class TestState:
    """
    unit test cases for the get_event_dest
    """

    def test0_get_event_dest0(self):
        result = State.get_event_dest(game, 4)
        assert result == 14, "test_get_event_dest0 -  "
        pass

    def test1_get_event_dest1(self):
        result = State.get_event_dest(game, 9)
        assert result == 31, "test_get_event_dest1 -  "
        pass

    def test2_get_event_dest2(self):
        result = State.get_event_dest(game, 17)
        assert result == 7, "test_get_event_dest2 -  "
        pass

    def test3_get_event_dest3(self):
        result = State.get_event_dest(game, 21)
        assert result == 42, "test_get_event_dest3 -  "
        pass

    def test4_get_event_dest4(self):
        result = State.get_event_dest(game, 28)
        assert result == 84, "test_get_event_dest4 -  "
        pass

    def test5_get_event_dest5(self):
        result = State.get_event_dest(game, 51)
        assert result == 67, "test_get_event_dest5 -  "
        pass

    def test6_get_event_dest6(self):
        result = State.get_event_dest(game, 54)
        assert result == 34, "test_get_event_dest6 -  "
        pass

    def test7_get_event_dest7(self):
        result = State.get_event_dest(game, 100)
        assert result == 0, "test_get_event_dest7 -  "
        pass

    def test8_init_starting_position0(self):
        g = State()
        g.n_players = 4
        g.ETF_Init(True)

        players = g.get_gamestate_position(1)
        assert players[0] == -1, "test_init_starting_position- "
        pass

    def test9_init_starting_position1(self):
        g = State()
        g.n_players = 4
        g.ETF_Init(True)
        players = game.get_gamestate_position(1)
        assert players[1] == -2, "test_init_starting_position- "
        pass

    def test10_init_starting_position2(self):
        g = State()
        g.n_players = 4
        g.ETF_Init(True)
        players = game.get_gamestate_position(1)
        assert players[2] == -3, "test_init_starting_position- "
        pass

    def test11_init_starting_position3(self):
        g = State()
        g.n_players = 4
        g.ETF_Init(True)
        players = game.get_gamestate_position(1)
        assert players[-4] == -1, "test_init_starting_position- "
        pass

    def test12_init_starting_position_count(self):
        g = State()
        g.n_players = 4
        g.ETF_Init(True)
        players = game.get_gamestate_position(1)
        assert len(players) == 4, "test_init_starting_position(), -- count players"
        pass

    def test13_init_state_count(self):
        assert game.get_gamestate_position(100) == 0, "Correct number of squares t13"

    def test14_init_state_count(self):
        try:
            game.get_gamestate_position(101)
        except:
            IndexError("Error expected")

    def test15_get_currentplayer0(self):
        player = State()
        assert player.get_current_player_int() == -1, "test15_get_currentplayer0 --"

    def test16_get_currentplayer1_switch_player(self):
        g = State()
        g.n_players = 4
        g.ETF_Init(True)
        g.switch_player()
        assert g.get_current_player_int() == -2, "test16_get_currentplayer1_switch_player--"

    def test17_get_currentplayer2(self):
        g = State()
        g.n_players = 4
        g.ETF_Init(True)
        g.switch_player()
        g.switch_player()
        g.switch_player()
        assert g.get_current_player_int() == -4, "test17_get_currentplayer2_switch_player--"

    def test18_is_event0(self):
        result = game.is_event(4)
        assert result, " test18_is_event0"
        pass

    def test19_is_event1(self):
        result = game.is_event(98)
        assert result, "test19_is_event1"
        pass

    def test20_is_event_non_event(self):
        try:
            game.is_event(12)
        except:
            IndexError("Error is expected")

    def test21_validate_update_move0(self):
        # move player -1 from 1 to 5
        game.validate_update_move(1, 5, -1)
        result = game.get_gamestate_position(5)
        assert -1 in result, "test21_validate_update_move0"


    def test22_validate_update_move1(self):
        # move player -2 from 15 to 21
        try:
           game.validate_update_move(1, 2, -1)
        except:
            TypeError()
        result = game.get_gamestate_position(2)
        assert -1 in result, "test21_validate_update_move0"

    def test23_validate_update_move2(self):
        game.validate_update_move(1, 16, -2)
        result = game.get_gamestate_position(16)
        assert -2 in result, "test23_validate_update_move2"

        # edge case
    def test24_validate_update_move3(self):
        game.validate_update_move(16, 100, -2)
        result = game.get_gamestate_position(100)
        assert -2 in result

        # edge case
    def test25_validate_update_move4(self):
        # should move back to 99, by wrapping back
        game.validate_update_move(100, 101, -2)
        # position 99 should have person
        result = game.get_gamestate_position(99)
        assert -2 in result

    # descend ladder
    def test26_validate_update_move5(self):
        # should move back to 78, by wrapping back
        game.validate_update_move(99, 98, -2)
        # position 79 should have person
        result = game.get_gamestate_position(79)
        assert -2 in result
        pass

    def test27_validate_update_move6(self):
        game.validate_update_move(79, 76, -2)
        game.validate_update_move(76, 85, -2)
        result = game.get_gamestate_position(85)
        assert -2 in result

    """
    toss player around ladders
    """
    def test28_validate_update_move7(self):
        game.validate_update_move(1, 4, -4)
        result = game.get_gamestate_position(14)
        assert -4 in result

    """
    integration test
    toss multiple players in same spot, 
    extreme and impossible but shows the code is robust
    """
    def test29_validate_update_move8(self):
        # descend to 36 at 87
        game.validate_update_move(1, 87, -3)
        game.validate_update_move(14, 87, -4)
        result = game.get_gamestate_position(36)
        assert -3 in result and -4 in result
        pass
    """
    toss around 
    extreme integration test edge case
    move all 4 players from different paths to end at the same spot
    almost zero probability
    """
    def test30_validate_update_move9(self):
        g = State()
        g.n_players = 4
        g.ETF_Init(True)
        g.validate_update_move(1, 101, -1)    # player 1 #99
        g.validate_update_move(1, 80, -2)   # player 2 #99
        g.validate_update_move(1, 64, -3)   # player 3 #60
        g.validate_update_move(60, 80, -3)  # player 3 #99
        g.validate_update_move(1, 98, -4)   # player 4 #79
        g.validate_update_move(79, 99, -4)  # player 4 #99
        result = g.get_gamestate_position(99)
        assert -1 in result and -2 in result and -3 in result and -4 in result

