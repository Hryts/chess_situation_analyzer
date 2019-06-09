"""
Module for game tree realisation
"""
import pickle
import gt_node


class GameTree:
    """
    Represents game tree data structure
    """

    def __init__(self):
        self.root = gt_node.GTNode()

    def add(self, game):
        """
        Adds a game to a tree by changing statistics in every node on path
        :param game: game to add
        :return: None
        """
        moves = game.get_moves()
        current_node = self.root

        for move in moves:
            if move in current_node.children:
                current_node.data.add_game(game)
            else:
                new_node = gt_node.GTNode(move)
                current_node.add_child(new_node)

            current_node = current_node.children[move]
            current_node.data.add_game(game)

    def find_game(self, game):
        """
        Finds game in tree by it's moves and returns a node with it
        :param game: game to find or moves of game to find
        :return: node
        """
        # noinspection Pylint
        if type(game) != list:
            moves = game.get_moves()
        else:
            moves = game

        print('looking for game:\t', moves)
        current_node = self.root

        for move in moves:
            if move not in current_node.children:
                # print(current_node)
                return None
            current_node = current_node.children[move]

        return current_node

    def to_file(self, file_name='games_tree.pickle', clear_tree=False):
        """
        Saves an object to a tree
        :return: None
        """
        pickle_out = open(file_name, 'wb')
        pickle.dump(self, pickle_out)
        pickle_out.close()
        if clear_tree:
            self.root = gt_node.GTNode()

    @staticmethod
    # noinspection Pylint
    def from_file(file_name='games_tree.pickle'):
        """
        Reads tree object from a file
        :param file_name: name of file
        :return: object of tree
        """
        file = open(file_name, 'rb')
        res = pickle.load(file)
        file.close()
        return res

    def __str__(self):
        return '{}'.format(self.root)
