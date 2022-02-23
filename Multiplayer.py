from Player import Player

"""
sets up multiplayer aspect of escape the fire and 
assigns player turn to given player
"""


class Multiplayer:
    """
    Player objects for any given player in the game
    """
    _current_player = int
    _player1 = Player
    _player2 = Player
    _player3 = Player
    _player4 = Player
    _players = list
    _nPlayers = int

    def __init__(self):
        self.__init_current()
        pass

    def __init_current(self):
        """
        initialize the current player
        :return:
        """
        # self._player1.set_turn(True)
        self._current_player = -1

    def _init_n_players(self):
        """
        Chose the number of players based on n_players
        used by the constructor method
        """
        if self._nPlayers == 1:
            self._player1 = Player("Player 1", -1)
            self._player2 = Player("Player 2", -2)
            self._players = self._player1, self._player2

        elif self._nPlayers == 2:
            self._player1 = Player("Player 1", -1)
            self._player2 = Player("Player 2", -2)
            self._player3 = None
            self._players = self._player1, self._player2, self._player3

        elif self._nPlayers == 3:
            self._player1 = Player("Player 1", -1)
            self._player2 = Player("Player 2", -2)
            self._player3 = Player("Player 3", -3)
            self._player4 = None
            self._players = self._player1, self._player2, self._player3, self._player4

        elif self._nPlayers == 4:
            self._player1 = Player("Player 1", -1)
            self._player2 = Player("Player 2", -2)
            self._player3 = Player("Player 3", -3)
            self._player4 = Player("Player 4", -4)
            self._players = self._player1, self._player2, self._player3, self._player4

        else:
            print("Error --wrong n for number of players")

    def get_player_by_number(self, number):
        """
        given a ID, fetch that player if it exists
        :param number: A Integer which represents a player ID
        :return: a reference to the player object
        """
        if number == self._player1.get_identifier():
            return self._player1
        elif number == self._player2.get_identifier():
            return self._player2
        elif number == self._player3.get_identifier():
            return self._player3
        elif number == self._player4.get_identifier():
            return self._player4

    def set_current_player(self, ID):
        """
        Set's the current player to a given player ID
        :param ID: A Integer which represents a player ID
        :return: None
        """
        self._current_player = ID

    def switch_player(self):
        """
        change the current playing player
        :return:
        """
        # 1p
        if self._nPlayers == 1:
            # AI element in the game
            if self._current_player == -1:
                self._current_player = -2
            else:
                self._current_player = -1
            pass
        # 2p
        elif self._nPlayers == 2:
            if self._current_player == -1:
                self._current_player = -2
            else:
                self._current_player = -1
        # 3p
        elif self._nPlayers == 3:
            if self._current_player == -3:
                self._current_player = -1
            else:
                self._current_player -= 1
        # 4p
        elif self._nPlayers == 4:
            if self._current_player == -4:
                self._current_player = -1
            else:
                self._current_player -= 1

        current_player_index = abs(self._current_player) - 1
        self._players[current_player_index].set_turn(True)

    def get_current_player_int(self):
        """
        get current playing player
        :return:
        """
        return self._current_player

    def get_player1(self):
        return self._player1

    def get_player2(self):
        return self._player2

    def get_player3(self):
        return self._player3

    def get_player4(self):
        return self._player4

    def get_n_players(self):
        return self._nPlayers

    def set_n_players(self, n):
        """
        set the number of players playing the game
        """
        if n > 4:
            raise (ValueError(" 1<n_players<4 is expected.. Here n is out of range"))
        self._nPlayers = n
        self._init_n_players()


def test():
    multi = Multiplayer()
    multi.switch_player()
    multi.switch_player()
    multi.switch_player()
    multi.switch_player()
    multi.switch_player()
    print("Current ")
    print(multi.get_current_player_int())
    assert multi.get_current_player_int() == -2, "Error turn switched wrong"
