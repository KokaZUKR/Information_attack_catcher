import warnings

from code.parse_pravda import parse_pravda

warnings.filterwarnings("ignore")

STRING_TO_SEARCH = 'ато'  # to be more 'user-friendly': just type your word here

if __name__ == '__main__':
    parse_pravda(STRING_TO_SEARCH)
