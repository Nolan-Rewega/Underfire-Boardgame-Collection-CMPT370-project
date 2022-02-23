from Multiplayer import Multiplayer

"""
Test for multiplayer class which controls
the number of players in Escape The Fire game
"""


class TestMultiplayer:
    players = Multiplayer()
    players._nPlayers = 1

    """
    regression tests for Multiplayer methods
    """
    def test_get_nPlayers(self):
        assert self.players.get_n_players() == 1, "n players not set correctly"

    def test_get_4nplayers(self):
        self.players._nPlayers = 4
        assert self.players.get_n_players() == 4, "n players not set correctly"

    def test_init1(self):
        self.players._nPlayers = 1
        self.players._init_n_players()
        assert self.players._player1 is not None and self.players._player2 is not None and \
            "init players not done properly"

    def test_init2(self):
        self.players._nPlayers = 2
        self.players._init_n_players()
        assert self.players._player1 is not None and self.players._player2 is not None and \
               self.players._player3 is None, "init players not done properly"

    def test_init3(self):
        self.players._nPlayers = 4
        self.players._init_n_players()
        assert self.players._player1 is not None and self.players._player2 is not None and \
               self.players._player3 is not None and self.players._player4 is not None, "init players not done properly"

    def test_switchPlayer1(self):
        self.players._current_player = -2
        self.players.switch_player()
        assert self.players._current_player == -3, "player not switched appropriately"

    def test_switchPlayer2(self):
        self.players._current_player = -4
        self.players.switch_player()
        assert self.players._current_player == -1, "player not switched appropriately"

    def test_set_n_player(self):
        self.players.set_n_players(4)
        self.players._init_n_players()
        assert self.players._nPlayers == 4, "set_n_players failed"

    def test_player_getter1(self):
        assert self.players.get_player1() == self.players._player1, "player object not returned properly"

    def test_player_getter2(self):
        assert self.players.get_player2() == self.players._player2, "player object not returned properly"

    def test_player_getter3(self):
        assert self.players.get_player3() == self.players._player3, "player object not returned properly"

    def test_player_getter4(self):
        assert self.players.get_player4() == self.players._player4, "player object not returned properly"
    """
    Integration tests for Multiplayer
    """
    def test_integration1(self):
        """
        create an instance of Multiplayer
        set the number of players
        init the player objects
        switch players
        check if the players exist
        """
        integration_player = Multiplayer()
        integration_player.set_n_players(2)
        integration_player._init_n_players()
        integration_player.switch_player()
        assert integration_player._player1 is not None and integration_player._player2 is not None and \
               integration_player._player3 is None, "integration test failed- players not done properly"
        assert integration_player.get_current_player_int() == -2, "integration test for curr Player failed"

