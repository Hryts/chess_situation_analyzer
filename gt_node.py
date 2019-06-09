"""
Module with node for games tree
"""

# import stat


class GTNode:
    """
    A node for the game tree
    """
    def __init__(self, move=None, data=None, children=None):
        self.move = move
        self.data = data
        if not data:
            self.data = Statistics()
        self.children = dict()
        if children:
            self.children = children

    def add_child(self, child):
        """
        Adds a child to the node
        :param child: node to add as a child
        :return: None
        """
        move = child.move
        self.children[move] = child

    def __str__(self):
        return 'Move:\t\t{}\n' \
               'Data:\t\t{}\n' \
               'Children:\t{}'.format(
                   self.move,
                   self.data,
                   self.children
                   )


class Statistics:
    """
    Represents statistics for chess games
    """
    def __init__(self, games_num=0, w_victories=0, b_victories=0, med_rat=0):
        self.games_num = int(games_num)
        self.w_victories = int(w_victories)
        self.b_victories = int(b_victories)
        self.med_rat = int(med_rat)

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

    def __add__(self, other):
        """
        Adds two objects of Statistics
        :param other: Statistics object
        :return: None
        """
        if not other.games_num:
            return self
        self.med_rat = (self.med_rat * self.games_num +
                        other.med_rat * other.games_num) / \
                       (self.games_num + other.games_num)
        self.w_victories += other.w_victories
        self.b_victories += other.b_victories
        self.games_num += other.games_num
        return self

    def odds_for(self, w_b):
        """
        Returns odds for white or black to win
        :param w_b: parameter to set side to check
        :return: odds
        """
        if w_b == 'b':
            return self.b_victories / self.games_num
        return self.w_victories / self.games_num

    def __str__(self):
        return 'games num:\t {0}\n' \
               '\t\twhite victories\t{1}\n' \
               '\t\tblack victories\t{2}\n' \
               '\t\tmedium rating\t{3}'.format(
                   self.games_num,
                   self.w_victories,
                   self.b_victories,
                   self.med_rat
                   )
