import argparse
import textwrap

from ngram.sentence_structure import Sentence
from ngram.preprocess_text import make_sentences
from ngram import Model


def train_model(model, train_file_name):
    """
    Train the model with some test data

    Arguuments:
        model (Model): the model to train
        train_file_name (str): the training file to read data from

    Returns:
        (Model): the trained model
    """
    with open(train_file_name) as f:
        raw_training_data = f.read()
    training_sentences = make_sentences(raw_training_data)

    # Run word replacement once the training data has been gathered
    Sentence.replaced_words = True

    # Apply replacement to the words that we just trained
    for sentence in training_sentences:
        sentence.replace_words()
    model.train(training_sentences)
    return model


def develop_model(model, dev_file_name):
    """
    Develop the model, training the lambda values to optimize perplexity

    If the model is not smoothed (anything other than `2s` or `3s`), this
    method skips over the tuning since it is time consuming and unnecessary.

    Tuning will be done only when a smoothed model is specified

    Arguments:
        model (Model): the model to train
        dev_file_name (str): the file to read dev data from

    Returns:
        (Model): the newly trained model
    """
    # No need to tune lambda if we're not using a smoothed model
    if not model.is_smoothed_bigram and not model.is_smoothed_trigram:
        print('Unsmoothed model; skipping tuning')
        return model

    print('Smoothed model; tuning with development data...')
    with open(dev_file_name) as f:
        raw_dev_data = f.read()
    dev_sentences = make_sentences(raw_dev_data)
    model.tune(dev_sentences)
    return model


def test_model(model, test_file_name):
    with open(test_file_name) as f:
        raw_test_data = f.read()
    test_sentences = make_sentences(raw_test_data)

    perplexities = model.evaluate(test_sentences)
    for sentence, perplexity in perplexities:
        print('{} : {}'.format(sentence, perplexity))


def main(model, train_file_name, dev_file_name, test_file_name):
    model = Model(model)  # Convert the model identifier into a Model object
    model = train_model(model, train_file_name)
    model = develop_model(model, dev_file_name)
    test_model(model, test_file_name)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='ngram',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent('''\
            NGram Model Builder

            Given some training, development, and test data, build a model
            that accurately determines the perplexity of the test sentences.

            ===================================================================

            Training data is used to determine the vocabulary for the rest
            of the data to be processed.

            Development data is used to tune the values for `lambda` and `k`,
            to get the lowest perplexity values possible.

            Test data is what the model is actually run against once
            development is complete.

            ===================================================================

            The model options map to the following models:
              1  : Unigram
              2  : Bigram
              2s : Bigram (smoothed with Unigram)
              3  : Trigram
              3s : Trigram (smoothed with Unigram and Bigram)

            ===================================================================
        '''))
    parser.add_argument('model', type=str,
                        choices=['1', '2', '2s', '3', '3s'],
                        help='The type of model to build')
    parser.add_argument('trainfile', type=str,
                        help='Path to the training file to use')
    parser.add_argument('devfile', type=str,
                        help='Path to the development file to use')
    parser.add_argument('testfile', type=str,
                        help='Path to the test file to use')
    args = parser.parse_args()

    main(args.model, args.trainfile, args.devfile, args.testfile)
