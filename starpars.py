#!/usr/bin/env python3

import os

import nltk
nltk.download('punkt')

# set the comment char that's used in the corpus
COMMENT_CHAR = '*'

def tokenize_corpus(filename):
    """
    Tokenize the corpus and return a list of all sentences and a list
    of all words. Returns two lists as tuple: (sentence_list, word_list).
    """
    script_path = os.path.abspath(os.path.dirname(__file__))

    # check if file is in directory of the script, else check current dir
    if filename in os.listdir(script_path):
        corpus_file = script_path + '/corpus.txt'
    elif filename in os.listdir('.'):
        corpus_file = 'corpus.txt'
    else:
        # raise error if file can't be found
        raise FileNotFoundError

    with open(corpus_file) as f:
        content = ''
        for line in f.readlines():
            if COMMENT_CHAR not in line:
                content += line

        # create a list with all sentences and remove the newline chars
        sentences = [l.replace('\n', ' ') for l in nltk.sent_tokenize(content)]
        # create a list of all words and filter punctuation marks
        words = [w for w in nltk.word_tokenize(content) if w not in '!.,?']

        # TODO: currently, word is splits on '. (So, man's --> man & 's)

    return sentences, words


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


if __name__ == '__main__':
    sentences, words, tags = load_tokenized_corpus('data/corpus')

    word_dict = {}


    for word, tag in tags:
        if tag not in word_dict:
            word_dict[tag] = set(word)
        else:
            word_dict[tag].add(word)

    print(sentences)
