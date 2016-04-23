from ngram.sentence_structure import Sentence
from nltk.tokenize import sent_tokenize, TreebankWordTokenizer
import re


class CustomTokenizer(TreebankWordTokenizer):

    def tokenize(self, text):
        """
        Custom tokenizer

        Disables splitting up contractions.  Original implementation:

            http://www.nltk.org/_modules/nltk/tokenize/treebank.html#TreebankWordTokenizer.tokenize
        """
        # starting quotes
        text = re.sub(r'^\"', r'``', text)
        text = re.sub(r'(``)', r' \1 ', text)
        text = re.sub(r'([ (\[{<])"', r'\1 `` ', text)

        # punctuation
        text = re.sub(r'([:,])([^\d])', r' \1 \2', text)
        text = re.sub(r'([:,])$', r' \1 ', text)
        text = re.sub(r'\.\.\.', r' ... ', text)
        text = re.sub(r'[;@#$%&]', r' \g<0> ', text)
        text = re.sub(r'([^\.])(\.)([\]\)}>"\']*)\s*$', r'\1 \2\3 ', text)
        text = re.sub(r'[?!]', r' \g<0> ', text)

        text = re.sub(r"([^'])' ", r"\1 ' ", text)

        # parens, brackets, etc.
        text = re.sub(r'[\]\[\(\)\{\}\<\>]', r' \g<0> ', text)
        text = re.sub(r'--', r' -- ', text)

        # add extra space to make things easier
        text = " " + text + " "

        # ending quotes
        text = re.sub(r'"', " '' ", text)
        text = re.sub(r'(\S)(\'\')', r'\1 \2 ', text)

        for regexp in self.CONTRACTIONS2:
            text = regexp.sub(r' \1 \2 ', text)
        for regexp in self.CONTRACTIONS3:
            text = regexp.sub(r' \1 \2 ', text)

        return text.split()


def split_preprocessed_text(text):
    """
    Split preprocessed text into lists of lines, contains lists of words

    Arguments:
        text (str): the text to process

    Returns:
        (list(list(str))): the split-up text
    """
    lines = text.split('\n')
    return list(map(lambda l: l.split(), lines))


def make_sentences(text, full_tokenizer=False):
    """
    Make sentences from input text

    Determines whether the input text has been processed already or needs to
    be processed.

    If the text needs to be processed, it passes the text off to the tokenizer.

    If the text is preprocessed, then it can simply split by lines, and then
    by spaces between the words.

    Arguments:
        text (str): the text to process

    Returns:
        (list(Sentence)): the processed Sentences
    """
    if text.startswith('<s>'):
        tokenized_sentences = split_preprocessed_text(text)
    else:
        if full_tokenizer:
            tokenized_sentences = tokenize_real_text(text)
        else:
            tokenized_sentences = tokenize_text(text)
    tokenized_sentences = filter(lambda a: len(a) != 0, tokenized_sentences)
    return list(map(lambda s: Sentence(s), tokenized_sentences))


def tokenize_text(text):
    """
    Break unprocessed text into the required format

    Arguments:
        text(str): the unprocessed text

    Returns:
        (list(list(str))): the processed text
    """
    def tokenize_sentences(text):
        sentences = map(lambda s: s.strip(), text.split('.'))
        return list(filter(lambda s: len(s) > 0, sentences))

    sentences = tokenize_sentences(text)
    return list(map(tokenize_sentence, sentences))


def tokenize_sentence(sentence):
    """
    Splits a sentence into the right format

    Adds the proper sentence start and end tokens, as well as adding spaces
    around commas

    Arguments:
        text (str): the unprocessed sentence

    Returns:
        (list(str)): the processed sentence
    """
    sentence = sentence \
        .replace('.', '') \
        .replace(',', ' ,')
    sentence = '<s> {} </s>'.format(sentence)
    return sentence.split()


def tokenize_real_text(text):
    def split_up_sentence(string):
        string = string.replace('.', '')
        words = CustomTokenizer().tokenize(string)
        words.insert(0, '<s>')
        words.append('</s>')
        return words

    sentence_strings = sent_tokenize(text)
    return list(map(lambda a: split_up_sentence(a), sentence_strings))
