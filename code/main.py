import warnings

from code.parse_gordon import parse_gordon
from code.parse_obozrevatel import parse_obozrevatel
from code.parse_pravda import parse_pravda

warnings.filterwarnings("ignore")

STRING_TO_SEARCH = 'нато'  # to be more 'user-friendly': just type your word here

if __name__ == '__main__':
    parse_pravda(STRING_TO_SEARCH)
    parse_obozrevatel(STRING_TO_SEARCH)
    parse_gordon(STRING_TO_SEARCH)
