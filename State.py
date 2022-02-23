from Multiplayer import Multiplayer
import random


# GAME MAP
class State:
    # game state contains the list of players at a given position
    _gameState = [0 for tiles in range(100)]
    # the events of the map
    __events = [0 for tiles in range(100)]
    # the destination for each event
    __destMap = dict
    _players = Multiplayer
    n_players = 0

    def __init__(self):
        self.__init_events()
        self._players = Multiplayer()
        self.__init_dest_map()

        # stats variables
        self.fire_paths = 0
        self.water_paths = 0

    def init_starting_position(self, Players_obj):
        """
        set the players in the grid
        :param Players_obj:
        :return:
        """
        if Players_obj._nPlayers == 1:
            self._gameState[0] = [Players_obj._player1.get_identifier(), Players_obj._player2.get_identifier()]
        elif Players_obj._player2 is None:
            self._gameState[0] = [Players_obj._player1.get_identifier()]
            print(Players_obj._player2)
        elif Players_obj._player3 is None:
            self._gameState[0] = [Players_obj._player1.get_identifier(), Players_obj._player2.get_identifier()]
        elif Players_obj._player4 is None:
            self._gameState[0] = [Players_obj._player1.get_identifier(), Players_obj._player2.get_identifier(),
                                  Players_obj._player3.get_identifier()]
        else:
            self._gameState[0] = [Players_obj._player1.get_identifier(),
                                  Players_obj._player2.get_identifier(),
                                  Players_obj._player3.get_identifier(),
                                  Players_obj._player4.get_identifier()]

    def __init_events(self):
        """
        mark the events with 1 in the __event array
        INDICES ARE RECORDED
        :return:
        """
        self.__events[3] = 1
        self.__events[8] = 1
        self.__events[16] = 1
        self.__events[20] = 1
        self.__events[27] = 1
        self.__events[50] = 1
        self.__events[53] = 1
        self.__events[61] = 1
        self.__events[63] = 1
        self.__events[71] = 1
        self.__events[79] = 1
        self.__events[86] = 1
        self.__events[91] = 1
        self.__events[94] = 1
        self.__events[97] = 1

    def __init_dest_map(self):
        """
        Key = source, val = destination, if key < val --> ladder
        store ACTUAL integers NOT indices
        :return:
        """
        self.__destMap = {
            4: 14,
            9: 31,
            17: 7,
            21: 42,
            28: 84,
            51: 67,
            54: 34,
            62: 19,
            64: 60,
            72: 91,
            80: 99,
            87: 36,
            92: 73,
            95: 75,
            98: 79,
        }

    def get_stats(self):
        """
        get all stats
        :return: Returns a list of stats
        """
        return [self.fire_paths, self.water_paths]

    def ETF_Init(self, new_game):
        """
        PURPOSE: The method initialises the States map with the appropriate number of players,
        and sets the starting position on the _gameState map.
        """
        # sets the number of players *inside* Multiplayer()
        self._players.set_n_players(self.n_players)
        if new_game:
            # updates the states map to display the number of players
            self.init_starting_position(self._players)
        else:
            self.update_every_players_pos()

    def update_every_players_pos(self):
        """
        this method breaks encapsulation,
        sets each play to the loaded board positions
        :return: None
        """
        # need to update the current turn
        for tile in range(0, len(self._gameState)):
            if self._gameState[tile] != 0:
                for player_number in self._gameState[tile]:
                    player_obj = self._players.get_player_by_number(player_number)
                    player_obj.set_curr_pos(tile + 1)

    def get_event_dest(self, event_pos):
        """
        Return the required destination for given event position
        :param event_pos: The event location on the map, ACTUAL coordinates
        :return: 0 if dest is not found
        """
        if event_pos in self.__destMap:
            return self.__destMap[event_pos]
        else:
            return 0

    def __check_destination(self, destination):
        """
        Verify correctness of the destination
        :param destination: dest
        :return: true if destination valid
        """
        return destination < 100

    def is_event(self, pos):
        """
        check for map event
        :param pos: ACTUAL position of the event the check NOT index
        :return: True if the map has an event
        """
        return self.__events[pos - 1] == 1

    def __update_gameState(self, curr, dest, playerint):
        """
        update the game map for the player position
        :param curr: ACTUAL coordinate of the current position
        :param dest: ACTUAL coordinate of the destination position
        :param playerint:
        :return:
        """
        # if the new position is not occupied
        if self._gameState[dest - 1] == 0:
            self._gameState[dest - 1] = [playerint]
        else:
            # new position occupied, tuple all the players
            self._gameState[dest - 1].extend([playerint])
        # old position has other players
        if self._gameState[curr - 1] != 0 or self._gameState[curr - 1] != playerint:
            # set only moved player to zero
            self._gameState[curr - 1].remove(playerint)
            if len(self._gameState[curr - 1]) == 0:
                self._gameState[curr - 1] = 0
        # no other players old position
        else:
            self._gameState[curr - 1] = 0

    def validate_update_move(self, curr, destination, playerint):
        """
        :param destination: ACTUAL coordinates of the player
        :param playerint: the player to move in the given position
        :postCondition: _gameState is updated
        :return: message showing operation success
        """
        # check for bounds
        if self.__check_destination(destination):
            # if there is an event at the destination move to the event pos
            if self.is_event(destination):
                print("Event Triggered")
                destination = self.get_event_dest(destination)

                # set the stat vars
                if playerint == -1 and destination > curr:
                    self.water_paths += 1
                elif playerint == -1 and destination < curr:
                    self.fire_paths += 1

            # update the map for new position
            self.__update_gameState(curr, destination, playerint)
        else:
            # out of bounds
            destination = self.__move_back(destination)
            if self.is_event(destination):
                destination = self.get_event_dest(destination)

                # set the stat vars
                if playerint == -1 and destination > curr:
                    self.water_paths += 1
                elif playerint == -1 and destination < curr:
                    self.fire_paths += 1

            self.__update_gameState(curr, destination, playerint)
        print(str(playerint) + " moving on the map from " + str(curr) + " to " + str(destination))
        return destination

    def __move_back(self, dest):
        """
        if the destination is >100 move back the difference of the roll
        :preCondition: dest>100
        :postCondition: _gameState is updated
        :return: the ACTUAL position to move to
        """
        go_back = dest - 100
        return 100 - go_back

    def get_current_player(self):
        """
        The player objects for each player containing all player
        information
        :return: the player object
        """
        current = self.get_current_player_int()
        if current == -1:
            return self._players.get_player1()
        if current == -2:
            return self._players.get_player2()
        if current == -3:
            return self._players.get_player3()
        if current == -4:
            return self._players.get_player4()

    def get_current_player_int(self):
        """
        return the indentifier of the current player
        :return:
        """
        return self._players.get_current_player_int()

    def switch_player(self):
        """
        change the turn of the current player
        :return:
        """
        self._players.switch_player()

    def update_player(self, dest):
        """
        Update the statistics of the current player,
        and record the previous moves of the player
        :param dest:
        :return:
        """
        player = self.get_current_player()
        player.set_curr_pos(dest)

    def win_condition(self, curr):
        """
        determine if the given player has won the
        game
        :param curr:
        :return:
        """
        return curr == 100

    def clear_state(self):
        """
        resets the gameState for escape the fire for future play-through
        """
        for i in range(len(self._gameState)):
            self._gameState[i] = 0
        self.__init__()
        print("ETF gameState hard reset")

    def print_state(self):
        print("Gamestate:: \n")
        count = 0
        print("[")
        for i in range(len(self._gameState)):
            print(self._gameState[i], end=" ")
            count += 1
            if count == 10:
                count = 0
                print()
        print("]")

    def print_event(self):
        print("Events::\n")
        print(self.__events)

    def player_console_descrip(self, curr, dest, current_player):
        description = ""
        adjectives_good = ["Boom ", "Amazing ", "Impressive ", "Wow ", "Splendid ", "Spectacular "]
        adjective_bad = ["Oh NO! ", "HEHEHE ", "Down it goes, ", "-_- ", "Decrescendo ", "Courage, "]
        elements = [" Water Slide. ", " Infernal Fire. "]
        if dest - curr > 6:
            description += str(elements[0])
            description += adjectives_good[2]
        elif dest - curr < 0:
            description += str(elements[1])
            description += adjective_bad[0]
        if current_player == -1:
            description += "Red moved from " + str(curr) + " to " + str(dest)
        elif current_player == -2:
            description += "Blue moved from " + str(curr) + " to " + str(dest)
        elif current_player == -3:
            description += "Yellow moved from " + str(curr) + " to " + str(dest)
        elif current_player == -4:
            description += "Green moved from " + str(curr) + " to " + str(dest)

        return description

    def get_gamestate_position(self, pos):
        """
        Get the list item at the given pos on the board
        :param pos: the ACTUAL position on the Game board
        """
        return self._gameState[pos - 1]
