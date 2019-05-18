"""
Realization of game tree data structure
"""


class GameTree:
    """
    Games tree to represent chess positions
    """
    def __init__(self, current_move=None):
        self.root = Root(current_move)
        self.children = {}

    def insert_child(self, key, value):
        """
        Inserts a child to a current root
        :param key: move to cause child position
        :param value: game position
        :return None
        """
        if key not in self.children:
            self.children[key] = GameTree(value)
        self.refresh(value)

    def get_child(self, move):
        """
        Returns child by move
        :param move: move as a key to a dictionary to access a child
        :return: child or -1 if there is no such a child
        """
        if move in self.children:
            return self.children[move]
        return -1

    def refresh(self, child):
        """
        Refresh staistics for current root
        :param child: game which result should effect statistics
        :return: None
        """
        self.root.stat.add_game(child.get_result(), child.get_ratings())


class Root:
    """
    Root node for games tree
    """
    def __init__(self, current_move=None):
        self.current_move = current_move
        self.number_of_games = 0
        self.stat = Statistics()

    def get_cur_move(self):
        """
        Returns move for current node
        :return: move
        """
        return self.current_move

    def get_stat(self):
        """
        Returns statistics in current node
        :return: statistics
        """
        return self.stat


class Statistics:
    """
    Represents statistics for chess games
    """
    def __init__(self, games_num=0, w_victories=0, b_victories=0, med_rat=0):
        self.games_num = games_num
        self.w_victories = w_victories
        self.b_victories = b_victories
        self.med_rat = med_rat

    def add_game(self, result, ratings):
        """
        Changes statistics by adding one game results
        :param result: result of game
        :param ratings: ratings of opponents
        :return: None
        """
        self.med_rat = (sum(ratings) + self.med_rat * self.games_num) / \
                       (self.games_num + len(ratings))
        self.w_victories += result[0]
        self.b_victories += result[1]
        self.games_num += 1

    def odds_for(self, w_b):
        """
        Returns odds for white or black to win
        :param w_b: parametr to set side to check
        :return: odds
        """
        if w_b == 'b':
            return self.b_victories / self.games_num
        return self.w_victories / self.games_num
