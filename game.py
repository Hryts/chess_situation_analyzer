"""
Course 1
module with class to represent chess game
"""


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
        """
        self.moves = moves
        self.result = Game.convert_result(result)
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

    def get_moves(self):
        """
        Returns list of moves made in game
        :return: moves
        """
        return self.moves

    @staticmethod
    def convert_result(result):
        """
        Converts results in pgn format to a tuple of numbers
        :param result: tuple of strings to describe result of game
        :return: tuple of numbers
        """
        if result == '*':
            return 0, 0
        if result[0] == '1/2':
            return 0.5, 0.5
        return int(result[0]), int(result[1])
