"""
Course 1
module with class to represent chess game
"""
import re


class Game:
    """
    Represents game in chess
    """
    def __init__(self, moves, result, ratings=(2000, 2000)):
        """
        Initializes the chess game
        :param moves: moves made in game
        :param result: (1, 0)-white wins; (0, 1)-black wins; (1/2-1/2)-draw
        :param ratings: ratings of players in game
        :param game_type: type of game
        """
        self.moves = moves
        self.result = result
        self.ratings = ratings

    def __eq__(self, other):
        if self.moves == other.moves and self.result == other.result:
            return True
        return False

    def __hash__(self):
        return hash((self.moves, self.result, self.ratings))

    def __str__(self):
        return 'Moves:\t\t{}\n' \
               'Result:\t\t{}\n' \
               'Ratings:\t{}\n'.format(
                   self.moves,
                   self.result,
                   self.ratings)

    def get_result(self):
        """
        Returns the result of a game
        :return: result of game
        """
        return self.result

    def get_ratings(self):
        """
        Returns ratings of players
        :return: ratings of players
        """
        return self.ratings
