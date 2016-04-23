import sys
from number_processing.parse_file_lines import parse_file_lines


if __name__ == '__main__':
    try:
        file_path = sys.argv[1]
        result = parse_file_lines(file_path)
        for sentence in result:
            print(sentence)
    except IndexError:
        print('Missing file name')
