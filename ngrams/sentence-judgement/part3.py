import sys
import argparse
import textwrap
import os
from multiprocessing import Process

from ngram.preprocess_text import make_sentences
from ngram.sentence_structure import Sentence
from ngram import Model


def chunks(array, chunk_size):
    """
    Split an array into a number of chunks

    Borrowed from:
        http://stackoverflow.com/a/312464/2250435
    """
    for i in range(0, len(array), chunk_size):
        yield array[i:i + chunk_size]


def replace_unknown_words_in_sentences(*args):
    for sentence in args:
        sentence.replace_words()


def format_for_output(sentence):
    return ' '.join(sentence.words)


def train(model, path):
    """
    Reads in a bunch of text data and trains the model from it
    """
    training_sentences = list()
    number_of_files = 1
    for filename in os.listdir(path):
        filename = '{}/{}'.format(path, filename)

        print('Reading file #{}'.format(number_of_files), file=sys.stderr)
        number_of_files += 1

        with open(filename, encoding='utf-8', errors='ignore') as f:
            text = f.read()
        training_sentences += make_sentences(text, full_tokenizer=True)

    print('Finished reading training data', file=sys.stderr)
    Sentence.replaced_words = True

    # Replace unknown words in the training sentences
    # Splits the task across 4 threads to speed things up
    threads = list()
    number_of_threads = 0
    for sentences in chunks(training_sentences, 1000):
        print('Starting thread #{} to replace {} sentences'
              .format(number_of_threads, len(sentences)),
              file=sys.stderr)
        number_of_threads += 1
        thread = Process(
            target=replace_unknown_words_in_sentences,
            args=(sentences)
        )
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()

    print('Finished doing word replacement on training data', file=sys.stderr)

    print('Staring model training...', file=sys.stderr)
    model.train(training_sentences)
    print('Finished training model', file=sys.stderr)

    return model


def develop(model, sentences):
    """
    Given some data, tune the model
    """
    print('Started tuning model', file=sys.stderr)
    model.tune(sentences)
    print('Finished tuning model', file=sys.stderr)
    return model


def test(model, sentences):
    """
    Given some data, test the model
    """
    print('Started testing model', file=sys.stderr)
    return model.evaluate(sentences)


def main(training_data_directory, test_file_path):
    model = Model('3s')
    model = train(model, training_data_directory)

    with open(test_file_path) as f:
        text = f.read()
    sentences = make_sentences(text)

    development_sentences = list(chunks(sentences, 520 * 5))[0]

    model = develop(model, development_sentences)
    test_results = test(model, sentences)
    print('Finished testing model', file=sys.stderr)
    for sentence, perplexity in test_results:
        print('{}\t{}'.format(format_for_output(sentence), perplexity))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='ngram',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
            Generate the perplexities for some real sentences
        '''))
    parser.add_argument('training_data_path', type=str,
                        help='Path to the directory containing training data')
    parser.add_argument('test_file_path', type=str,
                        help='Path to the file to test')
    args = parser.parse_args()

    main(args.training_data_path, args.test_file_path)
