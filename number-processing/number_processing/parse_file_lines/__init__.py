from ..convert_sentence import transform


def parse_file_lines(file_path):
    sentences = list()
    with open(file_path, 'r') as f:
        [sentences.append(transform(line.strip('\n'))) for line in f]
    return sentences
