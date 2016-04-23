from number_processing.parse_file_lines import parse_file_lines


def test_main_iterates_over_lines():
    result = parse_file_lines('examples/simple.txt')
    assert type(result) is list
