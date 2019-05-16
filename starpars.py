#!/usr/bin/env python3

import os
import pickle
import random
import sys
import time

from os.path import isfile

import nltk
from nltk import CFG
from nltk.parse import ViterbiParser
from nltk.parse.generate import generate

# download the needed nltk packages
nltk.download('punkt', download_dir=os.getenv('HOME') + '/.cache/nltk')
nltk.download('averaged_perceptron_tagger', download_dir=os.getenv('HOME') + '/.cache/nltk')

# set the comment char that's used in the corpus
COMMENT_CHAR = '*'
IGNR_CHARS = '.?!'

def tokenize_corpus(filename):
    """
    Tokenize the corpus and return a list of all sentences and a list
    of all words. Returns a list of the sentences, a word list and a tuple
    with the tagged words. Also dumps the tagged words to {filename}.tags.
    """
    try:
        script_path = os.path.abspath(os.path.dirname(__file__))
    except NameError:
        script_path = os.getcwd()

    # check if file is in directory of the script, else check current dir
    if isfile(f'{script_path}/{filename}'):
        corpus_file = f'{script_path}/{filename}'
    elif isfile(filename):
        corpus_file = filename
    else:
        # raise error if file can't be found
        raise FileNotFoundError(filename)

    with open(corpus_file) as f:
        cont = ''
        # first strip the comments from the corpus
        for line in f.readlines():
            if COMMENT_CHAR not in line:
                cont += line

    # create a list with all sentences and remove the newline chars
    sentences = [l.replace('\n', ' ') for l in nltk.sent_tokenize(cont)]
    # create a list of all words
    words = [w.lower() for w in nltk.word_tokenize(cont) if w not in IGNR_CHARS]
    # create a list of tuples of the words and it's tag
    tagged_words = nltk.pos_tag(words)

    # save the tagged words to a file for reuse with load_tokenized_corpus()
    basename = os.path.splitext(filename)[0]

    with open(f'{basename}.sentences', 'wb') as f:
        pickle.dump(sentences, f, -1)

    with open(f'{basename}.words', 'wb') as f:
        pickle.dump(words, f, -1)

    with open(f'{basename}.tags', 'wb') as f:
        pickle.dump(tagged_words, f, -1)


    return sentences, words, tagged_words


def load_tokenized_corpus(filename):
    """
    Load file generated with tokenize_corpus() and read the tags from it.
    Returns INFO.

    filename: filename or path to file without extension. E.g. 'data/corpus'
    will be extended to data/corpus.tags, data/corpus.words and
    data/corpus.sentences.
    """
    # the path of the script
    try:
        script_path = os.path.abspath(os.path.dirname(__file__))
    except NameError:
        script_path = os.getcwd()

    # search for the data files and the origin corpus
    txt_file = f'{script_path}/{filename}.txt'
    sentences_file = f'{script_path}/{filename}.sentences'
    words_file = f'{script_path}/{filename}.words'
    tags_file = f'{script_path}/{filename}.tags'


    # first check if the data files are present, else create them
    if isfile(sentences_file) and isfile(words_file) and isfile(tags_file):
        with open(sentences_file, 'rb') as f:
            sentences = pickle.load(f)

        with open(words_file, 'rb') as f:
            words = pickle.load(f)

        with open(tags_file, 'rb') as f:
            tags = pickle.load(f)
    elif isfile(txt_file):
        print('One or more datafiles missing, creating them', file=sys.stderr)
        sentences, words, tags = tokenize_corpus(txt_file)
    else:
        # raise error if file can't be found
        raise FileNotFoundError(filename)

    return sentences, words, tags


def cfg(filename):
    """
    Grammar rules are saved in _filename_. Load them and add the
    lexicon rules via create_lexicon() to it.
    """
    try:
        script_path = os.path.abspath(os.path.dirname(__file__))
    except NameError:
        script_path = os.getcwd()

    file_path = f'{script_path}/{filename}'
    if not isfile(file_path):
        raise FileNotFoundError(file_path)

    # open the file and read the grammar rules
    with open(file_path) as f:
        cfg = f.read()

    # add the lexicon to the grammar rules
    cfg += create_lexicon(tags)

    return CFG.fromstring(cfg)


def create_lexicon(word_tags):
    """
    Create a lexicon in the right format for nltk.CFG.fromString() from
    a list with tuples with words and their tag.
    """

    # dictionary to filter the double tags
    word_dict = {}
    for word, tag in word_tags:
        if tag not in word_dict:
            word_dict[tag] = {word}
        else:
            word_dict[tag].add(word)

    # PRO is the tag for 's, but the 's is not removed on nouns.
    word_dict['NN'] = [x.replace('\'s', '') for x in word_dict['NN']]
    word_dict['JJ'] = [x.replace('\'s', '') for x in word_dict['JJ']]
    del word_dict[',']
    word_dict['PRP'].update(word_dict['PRP$'])
    del word_dict['PRP$']
    word_dict['POS'] = ['"s']

    # convert the dictionary to the right NLTK format
    lexicon = ''
    for key, val in word_dict.items():
        lexicon += key + ' -> '
        # add ' ' around every word
        val = [f'\'{v}\'' for v in val]
        # the words are seperated by a pipe
        lexicon += ' | '.join(val) + '\n'

    return lexicon

def create_sentence(cfg, symbol):
    sentence = []

    prods = cfg.productions(lhs=symbol)
    print(prods)
    prod = random.choice(prods)

    for sym in prod.rhs():
        # if we've reached a terminal, add it to the sentence
        if isinstance(sym, str):
            sentence.append(sym)
        # # else go on going down the tree
        else:
            sentence.extend(create_sentence(cfg, sym))

    return sentence


def generate_sentences(cfg, num: int = 1000, sample_size: int = 20):
    """
    Generate sentences from a given CFG. Num is the number sentences
    generated and sample_size is the number of returned sentences.
    """
    parser = ViterbiParser(cfg)
    generator = parser.grammar()

    gen_sent = []
    for _ in range(num):
        sentence = []
        try:
            sentence = create_sentence(cfg, cfg.start())
        except:
            pass

        # add new sentence to the list
        gen_sent.append(sentence)

    # prevent recursive sentences and short sentences
    sentences = [s for s in gen_sent if len(s) > 4 and len(s) < 15]
    samples = random.sample(gen_sent, sample_size)

    for samp in samples:
        print(' '.join(samp))


if __name__ == '__main__':
    # load and tokenize the corpus
    sentences, words, tags = load_tokenized_corpus('data/corpus')

    # print(cfg('data/grammar.cfg'))
    # create the cfg with the grammar file
    # generate_sentences(cfg('data/grammar.cfg'))
    CFG = cfg('data/grammar.cfg')
    create_sentence(CFG, CFG.start())
