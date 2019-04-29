#!/usr/bin/env python3

import os
import pickle

from os.path import isfile

import nltk

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# set the comment char that's used in the corpus
COMMENT_CHAR = '*'

def tokenize_corpus(filename):
    """
    Tokenize the corpus and return a list of all sentences and a list
    of all words. Returns a list of the sentences, a word list and a tuple
    with the tagged words. Also dumps the tagged words to {filename}.tags.
    """
    script_path = os.path.abspath(os.path.dirname(__file__))

    # check if file is in directory of the script, else check current dir
    if isfile(f'{script_path}/{filename}'):
        corpus_file = f'{script_path}/{filename}'
    elif isfile(filename):
        corpus_file = filename
    else:
        # raise error if file can't be found
        raise FileNotFoundError

    with open(corpus_file) as f:
        content = ''
        # first strip the comments from the corpus
        for line in f.readlines():
            if COMMENT_CHAR not in line:
                content += line

        # create a list with all sentences and remove the newline chars
        sentences = [l.replace('\n', ' ') for l in nltk.sent_tokenize(content)]
        # create a list of all words
        words = [w.lower() for w in nltk.word_tokenize(content)]
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
    script_path = os.path.abspath(os.path.dirname(__file__))

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
        print('One or more datafiles missing, creating them')
        sentences, words, tags = tokenize_corpus(txt_file)
    else:
        # raise error if file can't be found
        raise FileNotFoundError

    return sentences, words, tags


def analyze():
    """
    Print information about the corpus. The information contains:
    - 5 most used words;
    - Total word count;
    - Word count without duplicates (size vocab);
    - Sentence count.
    """
    word_count = {}

    for word in words:
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1

    top_words = sorted(word_count, key=word_count.get, reverse=True)[:5]

    print('Top 5 most used words:')
    for tw in top_words:
        print(f'{tw}: {word_count[tw]}')

    print(f'Word count: {len(words)}')
    print(f'Vocabulary size: {len(vocab)}')
    print(f'Sentence count: {len(sentences)}')

    #[wt[0] for (wt, _) in word_tag_fd.most_common() if wt[1] == 'VERB']


if __name__ == '__main__':
    # sentences, words, tagged_words = tokenize_corpus('corpus.txt')
    load_tokenized_corpus('data/corpus')
    # vocab = set(words)
    # analyze()

    word_dict = {}

    # for word, tag in tagged_words:
    #     if word not in word_dict:
    #         word_dict[word] = set(tag)
    #     else:
    #         word_dict[word].add(tag)
