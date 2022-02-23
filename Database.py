import sqlite3
from sqlite3 import Error
import re


class Database:

    def __init__(self):
        self.__connection = None
        self.__cursor = None
        # create connection
        try:
            self.__connection = sqlite3.connect("UnderFire.sqlite3")
            self.__cursor = self.__connection.cursor()
            self.__connection.row_factory = sqlite3.Row

        except Error as err:
            print(err)

        # create leaderboard table
        c4_leaderboard_table = "CREATE TABLE IF NOT EXISTS c4_leaderboard (" \
                            "name text NOT NULL PRIMARY KEY," \
                            "score integer" \
                            ")"

        etf_leaderboard_table = "CREATE TABLE IF NOT EXISTS etf_leaderboard (" \
                                "name text NOT NULL PRIMARY KEY," \
                                "score integer" \
                                ")"

        self.__create_table(c4_leaderboard_table)
        self.__create_table(etf_leaderboard_table)

        # create stats table
        has_stats = False
        has_settings = False
        data = self.__get_tables()
        for i in range(len(data)):
            if data[i][0] == "stats":
                has_stats = True
            if data[i][0] == "settings":
                has_settings = True

        stats_table = "CREATE TABLE IF NOT EXISTS stats (" \
                      "games_played integer NOT NULL," \
                      "games_won integer NOT NULL," \
                      "win_percentage real NOT NULL," \
                      "c4_games integer NOT NULL," \
                      "c4_wins integer NOT NULL," \
                      "c4_percentage real NOT NULL," \
                      "etf_games integer NOT NULL," \
                      "etf_wins integer NOT NULL," \
                      "etf_percentage real NOT NULL," \
                      "total_score integer NOT NULL," \
                      "c4_pieces_placed integer NOT NULL," \
                      "c4_almost_wins," \
                      "etf_fire_paths integer NOT NULL," \
                      "etf_water_paths" \
                      ")" \

        self.__create_table(stats_table)
        # if the stats table has just been created, initialize it with default values
        if not has_stats:
            statement = "INSERT INTO stats (games_played, games_won, win_percentage," \
                        "c4_games, c4_wins, c4_percentage," \
                        "etf_games, etf_wins, etf_percentage," \
                        "total_score, c4_pieces_placed, c4_almost_wins," \
                        "etf_fire_paths, etf_water_paths)" \
                        "VALUES (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)"
            self.__cursor.execute(statement)
            self.__connection.commit()

        setting_table = "CREATE TABLE IF NOT EXISTS settings (" \
                        "res_height integer NOT NULL," \
                        "res_width integer NOT NULL," \
                        "difficulty text NOT NULL," \
                        "sound integer NOT NULL," \
                        "music integer NOT NULL" \
                        ")"

        self.__create_table(setting_table)
        if not has_settings:
            statement = "INSERT INTO settings (res_height, res_width, difficulty, sound, music)" \
                        "VALUES (720, 1280, 'Easy', 50, 50)"
            self.__cursor.execute(statement)
            self.__connection.commit()

        save_table = "CREATE TABLE IF NOT EXISTS saved_games (" \
                     "game text PRIMARY KEY," \
                     "state text" \
                     ")"

        self.__create_table(save_table)


    def close_connection(self):
        """
        Closes the database
        """
        if self.__connection:
            self.__connection.close()


    def __create_table(self, statement):
        """
        Creates a table for the database
        """
        try:
            self.__cursor.execute(statement)
        except Error as err:
            print(err)


    def update_leaderboard(self, game, name="---", score=-1):
        """
        Checks if the new score cracks the
        top 10 and will update the leaderboard if it does
        game --> 'c4' to update connect four leaderboard, 'etf' for escape the fire
        name --> the user given name for the high score, must not be the same as another in the leaderboard
        score --> the player's score
        Returns 0 if the update was successful, 1 if it was not
        """
        high_scores = self.get_leaderboard(game)
        if high_scores is not None:
            for i in range(len(high_scores)):
                if high_scores[i][0] == name:
                    return 1
        # if the leaderboard isn't full, just add the new score
        if high_scores is None:     # if there are no high scores
            try:
                if game == "c4":
                    self.__cursor.execute("INSERT INTO c4_leaderboard (name, score) VALUES (?, ?)", (name, score))
                else:
                    self.__cursor.execute("INSERT INTO etf_leaderboard (name, score) VALUES (?, ?)", (name, score))
                self.__connection.commit()
            except Error as err:
                print(err)

        elif len(high_scores) < 10:     # if there are less than 10 high scores
            try:
                if game == "c4":
                    self.__cursor.execute("INSERT INTO c4_leaderboard (name, score) VALUES (?, ?)", (name, score))
                else:
                    self.__cursor.execute("INSERT INTO etf_leaderboard (name, score) VALUES (?, ?)", (name, score))
                self.__connection.commit()
            except Error as err:
                print(err)
            # if the leaderboard is full and the new score is better than the 10th score, replace it
        else:
            if score > high_scores[9][1]:
                try:
                    if game == "c4":
                        self.__cursor.execute("DELETE FROM c4_leaderboard WHERE name=?", ([high_scores[9][0]]))
                        self.__cursor.execute("INSERT INTO c4_leaderboard (name, score) VALUES (?, ?)", (name, score))
                    else:
                        self.__cursor.execute("DELETE FROM etf_leaderboard WHERE name=?", ([high_scores[9][0]]))
                        self.__cursor.execute("INSERT INTO etf_leaderboard (name, score) VALUES (?, ?)", (name, score))
                    self.__connection.commit()
                except Error as err:
                    print(err)
        return 0


    def get_leaderboard(self, game):
        """
        Retrieves leaderboard data from highest score to lowest
        game --> 'c4' if you want the leaderboard for connect four, 'etf' for escape the fire
        Example output:
        if the leaderboard contains two rows --> name="aaa": score=50, name="bbb":score=100, the data will
        be returned like this:
            [('bbb', 100), ('aaa', 50)]
        (this is actual output printed to the console when testing)
        """
        if game == "c4":
            statement = "SELECT * FROM c4_leaderboard ORDER BY score DESC"
        else:
            statement = "SELECT * FROM etf_leaderboard ORDER BY score DESC"

        try:
            self.__cursor.execute(statement)
            leaderboard = self.__cursor.fetchall()
            if len(leaderboard) > 0:
                return leaderboard
            else:
                return None
        except Error as err:
            print(err)


    def get_stats(self):
        """
        Retrieves stats from the database as a dictionary
        """
        try:
            self.__cursor.execute("SELECT * FROM stats")
            data = self.__cursor.fetchall()[0]
            return {"games_played": data[0],
                    "games_won": data[1],
                    "win_percentage": data[2],
                    "c4_games": data[3],
                    "c4_wins": data[4],
                    "c4_percentage": data[5],
                    "etf_games": data[6],
                    "etf_wins": data[7],
                    "etf_percentage": data[8],
                    "total_score": data[9],
                    "c4_pieces_placed": data[10],
                    "c4_almost_wins": data[11],
                    "etf_fire_paths": data[12],
                    "etf_water_paths": data[13]
                    }
        except Error as err:
            print(err)


    def update_stats(self, game, outcome, new_data):
        """
        Updates stats in the db
        game --> 'c4' for connect four, or 'etf' for escape the fire
        outcome --> 0 if the game is a loss, 1 if it was a win
        new_data --> the new stats specific to the game that was just played
        allowable keys for new_data:
        connect four: "pieces_placed" --> how many pieces the player placed, "almost_wins" --> 3-in-a-rows in the game, "score"
        escape the fire: "fire_paths" --> fire paths taken in game, "water_paths" --> water paths taken in game, "score"
        """
        # update games played
        old_stats = self.get_stats()
        statement = "UPDATE stats SET " \
                    "games_played=games_played+1, " \
                    "total_score=total_score+" + str(new_data["score"]) + ", "
        if game == "c4":
            statement += "c4_games=c4_games+1,"
        else:
            statement += "etf_games=etf_games+1,"

        # update other stats
        if outcome == 1:    # if the game was won
            statement += "games_won=games_won+1, win_percentage=" + str((old_stats["games_won"] + 1) / (old_stats["games_played"] + 1)) + ","
            if game == "c4":
                statement += "c4_wins=c4_wins+1, c4_percentage=" + str((old_stats["c4_wins"] + 1) / (old_stats["c4_games"] + 1)) + ","
            else:
                statement += "etf_wins=etf_wins+1, etf_percentage=" + str((old_stats["etf_wins"] + 1) / (old_stats["etf_games"] + 1)) + ","
        else:   # if the game was lost
            statement += "win_percentage=" + str(old_stats["games_won"] / (old_stats["games_played"] + 1)) + ","
            if game == "c4":
                statement += "c4_percentage=" + str(old_stats["c4_wins"] / (old_stats["c4_games"] + 1)) + ", "

            else:
                statement += "etf_percentage=" + str(old_stats["etf_wins"] / (old_stats["etf_games"] + 1)) + ", "

        # update other stats
        if game == "c4":
            statement += "c4_pieces_placed=c4_pieces_placed+" + str(new_data["pieces_placed"]) + ","
            statement += "c4_almost_wins=c4_almost_wins+" + str(new_data["almost_wins"])
        else:
            statement += "etf_fire_paths=etf_fire_paths+" + str(new_data["fire_paths"]) + ", "
            statement += "etf_water_paths=etf_water_paths+" + str(new_data["water_paths"])

        self.__cursor.execute(statement)
        self.__connection.commit()


    def __get_tables(self):
        """
        Returns a list of the table names as a list of tuples
        """
        self.__cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        return self.__cursor.fetchall()


    def get_settings(self):
        """
        Returns the current saved settings as a dictionary
        example output:
            {'res_height': 400, 'res_width': 400, 'difficulty': 'easy', 'sound': 50, 'music': 50}
        """
        try:
            self.__cursor.execute("SELECT * FROM settings")
            data = self.__cursor.fetchall()[0]
            return {
                "res_height": data[0],
                "res_width": data[1],
                "difficulty": data[2],
                "sound": data[3],
                "music": data[4]
            }
        except Error as err:
            print(err)


    def update_settings(self, height=None, width=None, difficulty=None, sound=None, music=None):
        """
        Updates given settings in the database
        IMPORTANT: only give values for the settings that you want updated!
        example input:
            update_settings(difficulty="hard", sound=75, height=100)
            ^^ Only difficulty, sound, and res_height will be updated with the above call
        """
        statement = "UPDATE settings SET "
        # if input was given for an attribute, add it to the statement
        if height is not None:
            statement += "res_height = " + str(height) + ", "
        if width is not None:
            statement += "res_width = " + str(width) + ", "
        if difficulty is not None:
            statement += "difficulty = '" + difficulty + "', "
        if sound is not None:
            statement += "sound = " + str(sound) + ", "
        if music is not None:
            statement += "music = " + str(music) + ", "
        try:
            self.__cursor.execute(statement[:-2])
            self.__connection.commit()
        except Error as err:
            print(err)


    def save_game_state(self, game, state):
        """
        Saves game data and stores it in the db
        game --> 'c4' if you want to save a state for connect four, 'etf' for escape the fire
        state --> the state as a list
        """
        try:
            data = repr(state)  # convert the given list into a string
            self.__cursor.execute("INSERT or REPLACE INTO saved_games (game, state) VALUES (?, ?)", (game, data))
            self.__connection.commit()
        except Error as err:
            print(err)


    def get_game_state(self, game):
        """
        Returns a saved game of a given game if one exists
        game --> 'c4' if you want a state from connect four, 'etf' if you want escape the fire
        Returns the state as a list, or None if a state isn't found
        """
        # use data = eval(data from db)
        try:
            self.__cursor.execute("SELECT state FROM saved_games WHERE game=?", (game,))

            state = self.__cursor.fetchall()
            if len(state) > 0:
                return eval(state[0][0])
            else:
                return None
        except Error as err:
            print(err)


    def delete_game_state(self, game):
        """
        Deletes a given game state from the db
        game --> 'c4' if you want to delete a state for a connect four game, 'etf' for escape the fire
        """
        try:
            self.__cursor.execute("DELETE FROM saved_games WHERE game=?", (game,))
            self.__connection.commit()
        except Error as err:
            print(err)


    def __get_state_data(self):
        """
        A method to help with testing
        """
        try:
            self.__cursor.execute("SELECT * FROM saved_games")
            return self.__cursor.fetchall()
        except Error as err:
            print(err)
