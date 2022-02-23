class Player:
    __player_name = str
    #   ACTUAL coordinates of the player not INDEX
    __player_int = int
    _curr_pos = int
    _move_history = []
    __turn = bool

    def __init__(self, name, unique_identifier):
        """
        Constructor
        :param name: name of the player
        :param identifier: the unique int for the player
        """
        self.__player_name = name
        self.__player_int = unique_identifier
        # initial starting position for the player
        self._curr_pos = 1
        # record move
        self._move_history.append(1)
        self.__turn = False

    def get_identifier(self):
        """
        get the player's identifying number
        :return: A integer
        """
        return self.__player_int

    def check_destination(self, destination):
        """
        verify correctness of the destination
        :param destination: dest
        :return: true if destination valid
        """
        return destination < 100

    def set_curr_pos(self, destination):
        """
        move to a given dest location
        :param destination: dest to reach
        :return: none
        """
        if self.check_destination(destination):
            self._curr_pos = destination
            # update move history list
            self.__update_move_history(destination)

    def get_curr_pos(self):
        """
        ACTUAL coordinates of the player
        :return:
        """
        return self._curr_pos

    def get_player_name(self):
        """
        Get the player name
        :return:
        """
        return self.__player_name

    def __update_move_history(self, destination):
        """
        Record the move for the player
        :param destination: dest to record
        :return:
        """
        self._move_history.append(destination)

    def set_turn(self, boolean):
        """
        sets the current players turn value
        :param boolean: A boolean representing if its this players turn
        :return: None
        """
        self.__turn = boolean

    def is_player_turn(self):
        """
        returns a boolean indicating if it the current players turn
        :return: A boolean
        """
        return self.__turn

    def print_player(self):
        """
        DEBUG
        :return:
        """
        print("player name: " + str(self.__player_name + " \nplayer int: " + str(self.__player_int)))
        print(self._move_history)
