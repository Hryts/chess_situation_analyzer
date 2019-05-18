"""
Module for reading .pgn files
"""
import re

from game import Game


def get_game(file_name):
    """
    Generates games from file
    :param file_name: name of file with games
    :return: string with games
    """
    games = open(file_name)
    game = ''
    # counter = 0
    for line in games.readlines():
        # counter += 1
        game += line
        # if counter >= 20:
        if '{' in line:
            # counter = 0
            yield game.strip()
            game = ''
    games.close()


def get_moves(game):
    """
    Extracts moves from game given as lines from .pgn file
    :param game: lines from .pgn file
    :return: list of moves
    """
    game = game.split('\n')
    game = game[game.index('')+1:]

    moves = game[0].split()
    counter = 0

    for move in moves:
        if '.' in move:
            moves.remove(move)
        if '{' in move:
            counter = moves.index(move)
            break

    moves = moves[:counter]
    return moves


def get_game_result(game):
    """
    Function to extract game result
    (It always has the same position)
    :param game: string of lies from .pgn file
    :return: tuple as a result
    """
    game = game.split('\n')
    res = ''

    for line in game:
        if 'Result' in line:
            res = line

    pattern_w = r'\"(.*?)\-'
    pattern_b = r'\-(.*?)\"'
    white_res = re.search(pattern_w, res).group()[1:-1]
    black_res = re.search(pattern_b, res).group()[1:-1]

    return white_res, black_res


def get_ratings(game):
    """
    Returns ratings of players in game
    :param game:
    :return:
    """
    game = game.split('\n')
    white_rating = game[5]
    black_rating = game[6]

    for line in game:
        if 'WhiteELO' in line:
            white_rating = line
        elif 'BlackELO' in line:
            black_rating = line

    rating_pattern = r'\"(.*?)\"'
    white_rating = re.search(rating_pattern, white_rating).group()[1:-1]
    black_rating = re.search(rating_pattern, black_rating).group()[1:-1]

    return white_rating, black_rating


# def get_game_type(game):
#     """
#     Returns the type of a game
#     :param game: game in .pgn format
#     :return: string
#     """
#     game = game.split('/n')


def count_shit(game):
    """
    Temporary function for file exploring
    :param game: game as string from .png file
    :return: bool
    """
    game = game.split('\n')
    game = game[:game.index('') + 1]
    normal_result = 18
    return len(game) == normal_result


# noinspection Pylint
def read_games(filename, num_of_games=-1):
    """
    Reads given amount of games from file
    :param filename: name of file with games
    :param num_of_games: number of games to read
    :return: list of games
    """
    counter = 0
    res = []
    for game in get_game(filename):
        counter += 1
        moves = get_moves(game)
        result = get_game_result(game)
        ratings = get_ratings(game)
        game = Game(moves, result, ratings)
        res.append(game)
        if counter > num_of_games-1 and num_of_games != -1:
            return res
    return res


if __name__ == '__main__':
    FILENAME = 'ficsgamesdb_201801_blitz_nomovetimes_68966.pgn'
    games = read_games(FILENAME)
    for game in games:
        print(game)
