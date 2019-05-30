"""
Module with class to represent statistics for game tree
"""


class Statistics:
    """
    Represents statistics for chess games
    """
    def __init__(self, games_num=0, w_victories=0, b_victories=0, med_rat=0):
        self.games_num = games_num
        self.w_victories = w_victories
        self.b_victories = b_victories
        self.med_rat = med_rat

    def add_game(self, game):
        """
        Changes statistics by adding one game results
        :param game: game to add
        :return: None
        """
        result = game.get_result()
        ratings = game.get_ratings()
        self.med_rat = (sum(ratings) + self.med_rat * self.games_num) / \
                       (self.games_num + len(ratings))
        self.w_victories += result[0]
        self.b_victories += result[1]
        self.games_num += 1

    def odds_for(self, w_b):
        """
        Returns odds for white or black to win
        :param w_b: parameter to set side to check
        :return: odds
        """
        if w_b == 'b':
            return self.b_victories / self.games_num
        return self.w_victories / self.games_num
