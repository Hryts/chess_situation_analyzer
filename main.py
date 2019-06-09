"""
main module
"""

import sys
import psutil
import read_pgn
import games_tree

from gt_node import Statistics

sys.setrecursionlimit(10000)

# init constants
FILENAMES = ['ficsgamesdb_201801_blitz_nomovetimes_68966.pgn']
MY_FILENAME = '__vs_______.__.__.pgn'
MY_MOVES = None
MY_STAT = Statistics()
TOTAL_MEMORY = psutil.virtual_memory().total
TREE_FILES = []
# Maximum percentage of ram to use for keeping tree
MAX_RAM = 0.40

# Creat a game tree
GAMES_TREE = games_tree.GameTree()


def pgn_to_tree(filename, max_trees_num=-1):
    """
        Reads one pgn file given
        Transforms it to a tree
        Saves tree to binary file
        :return: None
        """
    print('collecting data...')

    counter = 0
    for game in read_pgn.read_game(filename):
        if 0 <= max_trees_num <= counter:
            break
        available_memory = psutil.virtual_memory().available
        used_memory = 1 - (available_memory / TOTAL_MEMORY)
        GAMES_TREE.add(game)
        if used_memory > MAX_RAM:
            # print(GAMES_TREE)
            print('RAM is {}% full'.format(MAX_RAM * 100))
            print('start saving to file no.{}'.format(counter+1))
            new_filename = 'games_tree{}.pickle'.format(counter)
            TREE_FILES.append(new_filename)
            print('saving to file...')
            GAMES_TREE.to_file(file_name=new_filename, clear_tree=True)
            print('saved')
            counter += 1
    else:
        print('EOF')
        print('start saving to file no.{}'.format(counter + 1))
        new_filename = 'games_tree{}.pickle'.format(counter)
        TREE_FILES.append(new_filename)
        print('saving to file...')
        GAMES_TREE.to_file(file_name=new_filename, clear_tree=True)
        print('saved')


def read_tree(filename):
    """
    Reads a file with a tree and converts it to a python object
    :param filename: name of binary file
    :return: game tree
    """
    print('Reading and converting {}'.format(filename))
    # my_game_tree = games_tree.GameTree()
    my_game_tree = games_tree.GameTree.from_file(filename)
    return my_game_tree


def save_tree_files(new_files, filename='tree_files.txt'):
    """
    Saves names of binary files with trees
    :param new_files: files to save
    :param filename: name of file to save to
    :return: None
    """
    saved_files = get_tree_files(filename)
    trees_file = open(filename, 'a')
    for file in new_files:
        if file not in saved_files:
            print(file, file=trees_file)
    trees_file.close()


def get_tree_files(filename='tree_files.txt'):
    """
    Reads names of binary files with trees from a given file
    :param filename: name of file to read from
    :return: set of names of files
    """
    res = set()
    trees_file = open(filename)
    for line in trees_file.readlines():
        res.add(line.strip())
    trees_file.close()
    return res


if __name__ == '__main__':
    TREE_FILES = get_tree_files()

    if not TREE_FILES:
        # Convert all the pgn files into trees and save them
        for pgn_file in FILENAMES:
            pgn_to_tree(pgn_file)

    # save_tree_files(TREE_FILES)

    MY_MOVES = read_pgn.read_my_moves(MY_FILENAME)

    for tree_file in TREE_FILES:
        current_tree = read_tree(tree_file)
        current_node = current_tree.find_game(MY_MOVES)
        if current_node:
            current_stat = current_node.data
            current_tree = None
            MY_STAT += current_stat

    print(MY_STAT)

###########################################################################
# Testing
###########################################################################
# for game in read_pgn.read_games(FILENAMES[0], 1000):
#     GAMES_TREE.add(game)
#
# print(GAMES_TREE.find_game(MY_MOVES))
