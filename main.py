"""
main module
"""

import sys
import psutil
import read_pgn
import games_tree

sys.setrecursionlimit(10000)

# init constants
FILENAMES = ['ficsgamesdb_201801_blitz_nomovetimes_68966.pgn']
MY_FILENAME = '__vs_______.__.__.pgn'
TOTAL_MEMORY = psutil.virtual_memory().total
FILES = []
COUNTER = 0
MAX_RAM = 0.5

# Creat a game tree
GAMES_TREE = games_tree.GameTree()


# Convert all the pgn files into trees and save them
def pgn_to_tree(filename):
    """
        Reads one pgn file given
        Transforms it to a tree
        Saves tree to binary file
        :return: None
        """
    print('collecting data...')

    counter = 0
    for game in read_pgn.read_game(filename):
        available_memory = psutil.virtual_memory().available
        used_memory = 1 - (available_memory / TOTAL_MEMORY)
        GAMES_TREE.add(game)
        if used_memory > MAX_RAM:
            print(GAMES_TREE.root)
            print('RAM is {}% full'.format(MAX_RAM * 100))
            print('start saving to file no.{}'.format(counter+1))
            new_filename = 'games_tree{}.pickle'.format(counter)
            FILES.append(new_filename)
            print('saving to file...')
            GAMES_TREE.to_file(file_name=new_filename, clear_tree=True)
            print('saved')
            counter += 1

    print('EOF')
    print('start saving to file no.{}'.format(counter + 1))
    new_filename = 'games_tree{}.pickle'.format(counter)
    FILES.append(new_filename)
    print('saving to file...')
    GAMES_TREE.to_file(file_name=new_filename, clear_tree=True)
    print('saved')


for pgn_file in FILENAMES:
    pgn_to_tree(pgn_file)
