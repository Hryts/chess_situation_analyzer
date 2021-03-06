"""
Module for reading .pgn files
"""
import re

from game import Game


# def get_game(file_name):
#     """
#     Generates games from file
#     :param file_name: name of file with games
#     :return: string with games
#     """
#     games = open(file_name)
#     _game = ''
#     # counter = 0
#     for line in games.readline():
#         print(line)
#         # counter += 1
#         _game += line
#         # if counter >= 20:
#         if '{' in line:
#             # counter = 0
#             yield _game.strip()
#             _game = ''
#     games.close()
#

def get_game(file_name):
    """
    Generates games from file
    :param file_name: name of file with games
    :return: string with games
    """
    games = open(file_name)
    _game = ''
    line = games.readline()

    while line:
        _game += line
        if '{' in line:
            yield _game.strip()
            _game = ''
        line = games.readline()

    games.close()


def get_moves(_game):
    """
    Extracts moves from game given as lines from .pgn file
    :param _game: lines from .pgn file
    :return: list of moves
    """
    _game = _game.split('\n')
    _game = _game[_game.index('')+1:]

    moves = _game[0].split()
    counter = 0

    for move in moves:
        if '.' in move or '(' in move or ')' in move:
            moves.remove(move)
        if '{' in move:
            counter = moves.index(move)
            break

    moves = moves[:counter]
    return moves


def get_game_result(_game):
    """
    Function to extract game result
    (It always has the same position)
    :param _game: string of lies from .pgn file
    :return: tuple as a result
    """
    _game = _game.split('\n')
    res = ''

    for line in _game:
        if 'Result' in line:
            res = line

    pattern_w = r'\"(.*?)\-'
    pattern_b = r'\-(.*?)\"'
    white_res = re.search(pattern_w, res).group()[1:-1]
    black_res = re.search(pattern_b, res).group()[1:-1]

    return white_res, black_res


def get_ratings(_game):
    """
    Returns ratings of players in game
    :param _game: game in .pgn format
    :return: ratings of players
    """
    _game = _game.split('\n')
    white_rating = _game[5]
    black_rating = _game[6]

    for line in _game:
        if 'WhiteELO' in line:
            white_rating = line
        elif 'BlackELO' in line:
            black_rating = line

    rating_pattern = r'\"(.*?)\"'
    white_rating = int(re.search(rating_pattern, white_rating).group()[1:-1])
    black_rating = int(re.search(rating_pattern, black_rating).group()[1:-1])

    return white_rating, black_rating


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
    for _game in get_game(filename):
        counter += 1
        moves = get_moves(_game)
        result = get_game_result(_game)
        ratings = get_ratings(_game)
        _game = Game(moves, result, ratings)
        res.append(_game)
        if counter > num_of_games-1 and num_of_games != -1:
            return res

    if len(res) == 1:
        return res[0]
    return res


def read_game(filename):
    """
    Generator of games
    :param filename: name of file with games
    :return: yields games one by one
    """
    for _game in get_game(filename):
        moves = get_moves(_game)
        result = get_game_result(_game)
        ratings = get_ratings(_game)
        _game = Game(moves, result, ratings)
        yield _game


def read_my_moves(filename):
    """
    Reads file with one unfinished game
    :param filename: name of pgn file with game
    :return: game
    """
    game_file = open(filename)
    res = ''

    for line in game_file.readlines():
        # noinspection Pylint
        res += line

    game_file.close()

    moves = res.strip().split('\n')[-1].split()
    # print(res.strip().split('\n'))
    for _ in moves:
        if '.' in _ or \
                '*' in _ or \
                '(' in _ or \
                ')' in _ or \
                '{' in _:
            moves.remove(_)
    if '*' in moves:
        moves.remove('*')

    return moves


if __name__ == '__main__':
    FILENAME = 'ficsgamesdb_201801_blitz_nomovetimes_68966.pgn'
    GAMES = read_games(FILENAME)
    for game in GAMES:
        print(game)
